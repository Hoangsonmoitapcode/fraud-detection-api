from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import PhoneNumber, SmsScam, BankingScam, WebsiteScam
from .schemas import (
    PhoneNumberCreate, PhoneNumberResponse, ConfirmRiskyRequest,
    SmsScamCreate, SmsScamResponse,
    BankingScamCreate, BankingScamResponse,
    WebsiteScamCreate, WebsiteScamResponse,
    BatchPhoneAnalyze, SMSPredictionRequest, SMSPredictionResponse
)
from .phone_service import PhoneService
from .sms_prediction_service import sms_prediction_service

# Tạo bảng (nếu chưa có)
Base.metadata.create_all(bind=engine)

# Auto-populate phone headings on startup (for Railway deployment)
def populate_phone_headings_if_empty():
    """Auto-populate phone headings if database is empty"""
    try:
        db = SessionLocal()
        from .models import PhoneHeading
        count = db.query(PhoneHeading).count()
        if count == 0:
            print("📱 Database empty - populating phone headings...")
            from .populate_headings import populate_phone_headings
            populate_phone_headings()
            print("✅ Phone headings populated successfully!")
        else:
            print(f"📊 Database already has {count} phone headings")
        db.close()
    except Exception as e:
        print(f"⚠️ Warning: Could not populate phone headings: {e}")

# Run on startup with error handling
try:
    populate_phone_headings_if_empty()
except Exception as e:
    print(f"⚠️ Startup warning: {e}")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="Fraud Detection API",
    description="Comprehensive fraud detection API for phone numbers, SMS, banking accounts, and websites",
    version="3.1.1"
)

# Add CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", summary="API Status")
def read_root():
    """Get API status and information"""
    import datetime
    import time
    
    try:
        import psutil
        cpu_usage = f"{psutil.cpu_percent()}%"
        memory_usage = f"{psutil.virtual_memory().percent}%"
        uptime_seconds = time.time() - psutil.boot_time()
    except ImportError:
        cpu_usage = "N/A"
        memory_usage = "N/A" 
        uptime_seconds = 0
    
    return {
        "message": "🛡️ Fraud Detection API",
        "version": "3.0.0",
        "status": "active",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime_seconds": uptime_seconds,
        "system_info": {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        },
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "phone_analysis": "/analyze/",
            "batch_analysis": "/analyze-batch/",
            "phone_numbers": "/phone-numbers/",
            "sms_scam": "/sms-scam/",
            "check_sms": "/check-sms/",
            "predict_sms_ai": "/predict-sms/",
            "banking_scam": "/banking-scam/",
            "website_scam": "/website-scam/"
        },
        "features": {
            "phone_fraud_detection": "✅ Active",
            "sms_spam_detection": "✅ Active",
            "sms_ai_prediction": "✅ Active (PhoBERT)", 
            "banking_scam_check": "✅ Active",
            "website_scam_check": "✅ Active"
        }
    }

# Essential API Endpoints

@app.post("/phone-numbers/", summary="Create phone number records with auto-detection (single or batch)")
def create_phone_numbers(phone_request: PhoneNumberCreate, db: Session = Depends(get_db)):
    """Create one or more phone number records with automatic phone number analysis and fraud detection"""
    
    results = []
    summary = {
        "total_submitted": len(phone_request.phone_numbers),
        "created_count": 0,
        "duplicate_count": 0,
        "error_count": 0,
        "processing_time": 0
    }
    
    import time
    start_time = time.time()
    
    for phone_number in phone_request.phone_numbers:
        try:
            # Check if phone number already exists
            existing_phone = db.query(PhoneNumber).filter(PhoneNumber.phone_number == phone_number).first()
            
            if existing_phone:
                summary["duplicate_count"] += 1
                results.append({
                    "phone_number": phone_number,
                    "status": "duplicate",
                    "message": "Phone number already exists",
                    "phone_number_id": existing_phone.id,
                    "analysis": {
                        "phone_head": existing_phone.phone_head,
                        "phone_region": existing_phone.phone_region,
                        "label": existing_phone.label
                    }
                })
                continue
            
            # Analyze phone number automatically
            analysis = PhoneService.analyze_phone_number(phone_number, db)
            
            # Create phone number record with auto-detected information
            db_phone_number = PhoneNumber(
                phone_number=phone_number,
                phone_head=analysis["phone_head"],
                phone_region=analysis["phone_region"],
                label=analysis["label"],
                heading_id=analysis["heading_id"]
            )
            
            db.add(db_phone_number)
            db.commit()
            db.refresh(db_phone_number)
            
            summary["created_count"] += 1
            results.append({
                "phone_number": phone_number,
                "status": "created",
                "phone_number_id": db_phone_number.id,
                "analysis": analysis,
                "fraud_risk": "HIGH" if analysis["label"] == "unsafe" else "LOW"
            })
            
        except Exception as e:
            db.rollback()
            summary["error_count"] += 1
            results.append({
                "phone_number": phone_number,
                "status": "error",
                "message": str(e)
            })
    
    summary["processing_time"] = round(time.time() - start_time, 2)
    
    # If only 1 phone number and it was created successfully, return PhoneNumberResponse format for backward compatibility
    if len(phone_request.phone_numbers) == 1 and summary["created_count"] == 1:
        created_result = next(r for r in results if r["status"] == "created")
        phone_number_record = db.query(PhoneNumber).filter(PhoneNumber.id == created_result["phone_number_id"]).first()
        return phone_number_record
    
    # Otherwise return batch format
    return {
        "summary": summary,
        "results": results
    }

@app.post("/analyze/", summary="Analyze phone numbers without saving (single or batch)")
def analyze_phone_numbers(analyze_request: BatchPhoneAnalyze, db: Session = Depends(get_db)):
    """Analyze one or more phone numbers for fraud detection without saving to database"""
    
    results = []
    summary = {
        "total_analyzed": len(analyze_request.phone_numbers),
        "high_risk_count": 0,
        "low_risk_count": 0,
        "error_count": 0,
        "processing_time": 0
    }
    
    import time
    start_time = time.time()
    
    for phone_number in analyze_request.phone_numbers:
        try:
            analysis = PhoneService.analyze_phone_number(phone_number, db)
            fraud_risk = "HIGH" if analysis["label"] == "unsafe" else "LOW"
            
            # Update summary counters
            if fraud_risk == "HIGH":
                summary["high_risk_count"] += 1
            else:
                summary["low_risk_count"] += 1
            
            result = {
                "phone_number": phone_number,
                "analysis": analysis,
                "fraud_risk": fraud_risk,
                "status": "success"
            }
            
        except Exception as e:
            summary["error_count"] += 1
            result = {
                "phone_number": phone_number,
                "error": str(e),
                "fraud_risk": "UNKNOWN",
                "status": "error"
            }
        
        results.append(result)
    
    summary["processing_time"] = round(time.time() - start_time, 2)
    
    # If only 1 phone number, return simple format for backward compatibility
    if len(analyze_request.phone_numbers) == 1 and summary["error_count"] == 0:
        result = results[0]
        return {
            "phone_number": result["phone_number"],
            "analysis": result["analysis"],
            "fraud_risk": result["fraud_risk"]
        }
    
    # Otherwise return batch format
    return {
        "summary": summary,
        "results": results
    }


@app.post("/confirm-risky/", response_model=PhoneNumberResponse, summary="Confirm risky number and add to database")
def confirm_risky_number(request: ConfirmRiskyRequest, db: Session = Depends(get_db)):
    """Confirm a risky/scam/spam number and add it to the database"""
    # Check if the number already exists in database
    existing_phone = db.query(PhoneNumber).filter(PhoneNumber.phone_number == request.phone_number).first()
    if existing_phone:
        # Update existing record with confirmed status
        existing_phone.label = "unsafe"
        db.commit()
        db.refresh(existing_phone)
        return existing_phone
    
    # Analyze phone number to get region and heading info
    analysis = PhoneService.analyze_phone_number(request.phone_number, db)
    
    # Create new phone number record with confirmed unsafe status
    db_phone_number = PhoneNumber(
        phone_number=request.phone_number,
        phone_head=analysis["phone_head"],
        phone_region=analysis["phone_region"],
        label="unsafe",  # Force label to unsafe since user confirmed it's risky
        heading_id=analysis["heading_id"]
    )
    
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    
    return db_phone_number


@app.get("/health", summary="Health Check Endpoint")
def health_check(db: Session = Depends(get_db)):
    """Simple health check endpoint for monitoring systems"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    import datetime
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.datetime.now().isoformat(),
        "checks": {
            "database": db_status,
            "api": "healthy"
        }
    }


# ============================================================================
# NEW SCAM DETECTION ENDPOINTS
# ============================================================================

@app.post("/banking-scam/", summary="Report banking scam accounts (single or batch)")
def report_banking_scam(banking_request: BankingScamCreate, db: Session = Depends(get_db)):
    """Report one or more banking accounts used for scam/fraud activities"""
    
    results = []
    summary = {
        "total_submitted": len(banking_request.banking_accounts),
        "created_count": 0,
        "duplicate_count": 0,
        "error_count": 0
    }
    
    for banking_item in banking_request.banking_accounts:
        try:
            # Check if the account already exists
            existing_account = db.query(BankingScam).filter(
                BankingScam.account_number == banking_item.account_number,
                BankingScam.bank_name == banking_item.bank_name
            ).first()
            
            if existing_account:
                summary["duplicate_count"] += 1
                results.append({
                    "account_number": banking_item.account_number,
                    "bank_name": banking_item.bank_name,
                    "status": "duplicate",
                    "id": existing_account.id,
                    "message": "Account already reported"
                })
                continue
            
            # Create new banking scam record
            db_banking_scam = BankingScam(
                account_number=banking_item.account_number,
                bank_name=banking_item.bank_name
            )
            
            db.add(db_banking_scam)
            db.commit()
            db.refresh(db_banking_scam)
            
            summary["created_count"] += 1
            results.append({
                "account_number": banking_item.account_number,
                "bank_name": banking_item.bank_name,
                "status": "created",
                "id": db_banking_scam.id
            })
            
        except Exception as e:
            db.rollback()
            summary["error_count"] += 1
            results.append({
                "account_number": banking_item.account_number,
                "bank_name": banking_item.bank_name,
                "status": "error",
                "message": str(e)
            })
    
    return {
        "summary": summary,
        "results": results
    }


@app.post("/website-scam/", summary="Report website scams (single or batch)")
def report_website_scam(website_request: WebsiteScamCreate, db: Session = Depends(get_db)):
    """Report one or more websites used for scam/phishing activities"""
    
    results = []
    summary = {
        "total_submitted": len(website_request.websites),
        "created_count": 0,
        "updated_count": 0,
        "duplicate_count": 0,
        "error_count": 0
    }
    
    for website_item in website_request.websites:
        try:
            # Check if the website already exists
            existing_website = db.query(WebsiteScam).filter(
                WebsiteScam.website_url == website_item.website_url
            ).first()
            
            if existing_website:
                # Update existing record with new label if different
                if existing_website.label != website_item.label:
                    existing_website.label = website_item.label
                    db.commit()
                    db.refresh(existing_website)
                    summary["updated_count"] += 1
                    results.append({
                        "website_url": website_item.website_url,
                        "label": website_item.label,
                        "status": "updated",
                        "id": existing_website.id,
                        "message": "Label updated"
                    })
                else:
                    summary["duplicate_count"] += 1
                    results.append({
                        "website_url": website_item.website_url,
                        "label": website_item.label,
                        "status": "duplicate",
                        "id": existing_website.id,
                        "message": "Website already reported with same label"
                    })
                continue
            
            # Create new website scam record
            db_website_scam = WebsiteScam(
                website_url=website_item.website_url,
                label=website_item.label
            )
            
            db.add(db_website_scam)
            db.commit()
            db.refresh(db_website_scam)
            
            summary["created_count"] += 1
            results.append({
                "website_url": website_item.website_url,
                "label": website_item.label,
                "status": "created",
                "id": db_website_scam.id
            })
            
        except Exception as e:
            db.rollback()
            summary["error_count"] += 1
            results.append({
                "website_url": website_item.website_url,
                "label": website_item.label,
                "status": "error",
                "message": str(e)
            })
    
    return {
        "summary": summary,
        "results": results
    }


@app.get("/check-banking/", summary="Check if banking account is reported as scam")
def check_banking_scam(account_number: str, bank_name: str, db: Session = Depends(get_db)):
    """Check if a banking account is reported as scam"""
    scam_account = db.query(BankingScam).filter(
        BankingScam.account_number == account_number,
        BankingScam.bank_name == bank_name
    ).first()
    
    return {
        "account_number": account_number,
        "bank_name": bank_name,
        "is_scam": scam_account is not None,
        "risk_level": "HIGH" if scam_account else "LOW"
    }


@app.get("/check-website/", summary="Check if website is reported as scam")
def check_website_scam(website_url: str, db: Session = Depends(get_db)):
    """Check if a website is reported as scam"""
    scam_website = db.query(WebsiteScam).filter(
        WebsiteScam.website_url == website_url
    ).first()
    
    return {
        "website_url": website_url,
        "is_scam": scam_website is not None,
        "label": scam_website.label if scam_website else "unknown",
        "risk_level": "HIGH" if scam_website and scam_website.label == "scam" else "LOW"
    }


@app.post("/sms-scam/", summary="Report SMS scams (single or batch)")
def report_sms_scam(sms_request: SmsScamCreate, db: Session = Depends(get_db)):
    """Report one or more SMS messages as scam/spam"""
    
    results = []
    summary = {
        "total_submitted": len(sms_request.sms_messages),
        "created_count": 0,
        "updated_count": 0,
        "duplicate_count": 0,
        "error_count": 0
    }
    
    for sms_item in sms_request.sms_messages:
        try:
            # Check if SMS content already exists (exact match)
            existing_sms = db.query(SmsScam).filter(
                SmsScam.sms_content == sms_item.sms_content
            ).first()
            
            if existing_sms:
                # Update label if different
                if existing_sms.label != sms_item.label:
                    existing_sms.label = sms_item.label
                    db.commit()
                    db.refresh(existing_sms)
                    summary["updated_count"] += 1
                    results.append({
                        "sms_content": sms_item.sms_content[:100] + "..." if len(sms_item.sms_content) > 100 else sms_item.sms_content,
                        "label": sms_item.label,
                        "status": "updated",
                        "id": existing_sms.id,
                        "message": "Label updated"
                    })
                else:
                    summary["duplicate_count"] += 1
                    results.append({
                        "sms_content": sms_item.sms_content[:100] + "..." if len(sms_item.sms_content) > 100 else sms_item.sms_content,
                        "label": sms_item.label,
                        "status": "duplicate",
                        "id": existing_sms.id,
                        "message": "SMS already reported with same label"
                    })
                continue
            
            # Create new SMS scam record
            db_sms_scam = SmsScam(
                sms_content=sms_item.sms_content,
                label=sms_item.label
            )
            
            db.add(db_sms_scam)
            db.commit()
            db.refresh(db_sms_scam)
            
            summary["created_count"] += 1
            results.append({
                "sms_content": sms_item.sms_content[:100] + "..." if len(sms_item.sms_content) > 100 else sms_item.sms_content,
                "label": sms_item.label,
                "status": "created",
                "id": db_sms_scam.id
            })
            
        except Exception as e:
            db.rollback()
            summary["error_count"] += 1
            results.append({
                "sms_content": sms_item.sms_content[:100] + "..." if len(sms_item.sms_content) > 100 else sms_item.sms_content,
                "label": sms_item.label,
                "status": "error",
                "message": str(e)
            })
    
    return {
        "summary": summary,
        "results": results
    }


@app.get("/check-sms/", summary="Check if SMS content is spam (Database + AI fallback)")
def check_sms_scam(sms_content: str, use_ai_fallback: bool = True, db: Session = Depends(get_db)):
    """
    Check if SMS content is reported as spam (supports fuzzy matching + AI fallback)
    
    This endpoint first checks the database for exact and fuzzy matches.
    If no matches are found and use_ai_fallback=True, it uses the AI model for prediction.
    """
    # First try exact match
    exact_match = db.query(SmsScam).filter(
        SmsScam.sms_content == sms_content
    ).first()
    
    if exact_match:
        return {
            "sms_content": sms_content,
            "is_spam": True,
            "label": exact_match.label,
            "risk_level": "HIGH" if exact_match.label == "spam" else "LOW",
            "match_type": "exact",
            "source": "database"
        }
    
    # Try fuzzy matching (contains keywords)
    fuzzy_matches = db.query(SmsScam).filter(
        SmsScam.sms_content.ilike(f"%{sms_content[:50]}%")  # Match first 50 chars
    ).all()
    
    if fuzzy_matches:
        spam_matches = [match for match in fuzzy_matches if match.label == "spam"]
        if spam_matches:
            return {
                "sms_content": sms_content,
                "is_spam": True,
                "label": "spam",
                "risk_level": "MEDIUM",  # Lower confidence for fuzzy match
                "match_type": "fuzzy",
                "similar_count": len(spam_matches),
                "source": "database"
            }
    
    # If no database matches found and AI fallback is enabled, use AI model
    if use_ai_fallback:
        try:
            ai_prediction = sms_prediction_service.predict(sms_content)
            is_spam = ai_prediction["prediction"] == "spam"
            
            # Determine risk level based on AI confidence
            if is_spam:
                if ai_prediction["confidence"] >= 0.8:
                    risk_level = "HIGH"
                elif ai_prediction["confidence"] >= 0.6:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
            else:
                risk_level = "LOW"
            
            return {
                "sms_content": sms_content,
                "is_spam": is_spam,
                "label": ai_prediction["prediction"],
                "risk_level": risk_level,
                "match_type": "ai_prediction",
                "confidence": ai_prediction["confidence"],
                "source": "ai_model"
            }
        except Exception as e:
            # AI model failed, fall back to unknown
            pass
    
    # No matches found (database or AI)
    return {
        "sms_content": sms_content,
        "is_spam": False,
        "label": "unknown",
        "risk_level": "LOW",
        "match_type": "none",
        "source": "none"
    }


@app.post("/predict-sms/", response_model=SMSPredictionResponse, summary="Predict SMS spam/ham using AI model")
def predict_sms_spam(request: SMSPredictionRequest):
    """
    Predict if SMS content is spam or ham using PhoBERT AI model
    
    This endpoint uses a trained PhoBERT model to classify SMS messages as spam or ham.
    It provides confidence scores and detailed prediction information.
    """
    try:
        # Get prediction from the AI model
        prediction_result = sms_prediction_service.predict(request.sms_content)
        
        # Determine risk level based on prediction and confidence
        if prediction_result["prediction"] == "spam":
            if prediction_result["confidence"] >= 0.8:
                risk_level = "HIGH"
            elif prediction_result["confidence"] >= 0.6:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
        else:  # ham
            risk_level = "LOW"
        
        # Get model information
        model_info = sms_prediction_service.get_model_info()
        
        return SMSPredictionResponse(
            sms_content=request.sms_content,
            prediction=prediction_result["prediction"],
            confidence=prediction_result["confidence"],
            risk_level=risk_level,
            model_info=model_info,
            processed_text=prediction_result.get("processed_text", request.sms_content)
        )
        
    except Exception as e:
        # Return error response in case of failure
        return SMSPredictionResponse(
            sms_content=request.sms_content,
            prediction="unknown",
            confidence=0.0,
            risk_level="UNKNOWN",
            model_info={"error": str(e), "is_loaded": False},
            processed_text=request.sms_content
        )


# ============================================================================
# ADMIN ENDPOINTS (for Railway database setup)
# ============================================================================

@app.post("/admin/setup-database", summary="Setup database tables and populate data")
def setup_database(db: Session = Depends(get_db)):
    """Setup database tables and populate initial data (run once after deployment)"""
    try:
        from .models import PhoneHeading
        
        # Check if tables exist and have data
        try:
            count = db.query(PhoneHeading).count()
            if count > 0:
                return {
                    "status": "already_setup",
                    "message": f"Database already has {count} phone headings",
                    "phone_headings_count": count
                }
        except Exception:
            # Tables might not exist yet, that's ok
            pass
        
        # Ensure tables are created
        Base.metadata.create_all(bind=engine)
        
        # Populate phone headings if empty
        from .populate_headings import populate_phone_headings
        populate_phone_headings()
        
        # Verify setup
        final_count = db.query(PhoneHeading).count()
        
        return {
            "status": "success",
            "message": "Database setup completed successfully",
            "phone_headings_count": final_count,
            "tables_created": ["phone_numbers", "phone_headings", "sms_scams", "banking_scams", "website_scams"]
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Database setup failed: {str(e)}"
        }

@app.get("/admin/database-status", summary="Check database status and table counts")
def database_status(db: Session = Depends(get_db)):
    """Check database status and get table counts"""
    try:
        from .models import PhoneHeading, PhoneNumber, SmsScam, BankingScam, WebsiteScam
        
        status = {
            "database_connection": "healthy",
            "tables": {
                "phone_headings": db.query(PhoneHeading).count(),
                "phone_numbers": db.query(PhoneNumber).count(),
                "sms_scams": db.query(SmsScam).count(),
                "banking_scams": db.query(BankingScam).count(),
                "website_scams": db.query(WebsiteScam).count()
            },
            "total_records": 0
        }
        
        status["total_records"] = sum(status["tables"].values())
        
        return status
        
    except Exception as e:
        return {
            "database_connection": "error",
            "error": str(e),
            "tables": {}
        }
