import pickle
import os
import logging
import time
from typing import Dict, Union, Optional
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SMSPredictionService:
    """Service for SMS spam/ham prediction using PhoBERT model"""
    
    def __init__(self, model_path: str = "phobert_sms_classifier.pkl"):
        # Try multiple possible model paths - Railway specific
        self.possible_paths = [
            "/app/phobert_sms_classifier.pkl",  # Primary path for Railway
            "phobert_sms_classifier.pkl",       # Local development
            "models/phobert_sms_classifier.pkl", # Models directory
            os.environ.get("MODEL_PATH", "/app/phobert_sms_classifier.pkl"),
            model_path,
            f"/app/{model_path}",
            f"/tmp/models/{model_path}",
        ]
        
        # Import model downloader
        try:
            from .model_downloader import model_downloader
            self.model_downloader = model_downloader
        except ImportError:
            self.model_downloader = None
        self.model_path = None
        self.model = None
        self.tokenizer = None
        self.vectorizer = None
        self.is_loaded = False
        self.load_attempts = 0
        self.max_load_attempts = 3
        self.last_load_attempt = None
        self.fallback_mode = False
        
    def _find_model_file(self) -> Optional[str]:
        """Find the model file from possible paths"""
        logger.info("🔍 Searching for model file in possible paths...")
        
        for i, path in enumerate(self.possible_paths):
            logger.info(f"  Path {i+1}: {path}")
            if path and os.path.exists(path):
                file_size = os.path.getsize(path)
                logger.info(f"✅ Found model at: {path} (size: {file_size / (1024*1024):.1f} MB)")
                
                # Check if file size is reasonable (at least 50MB for safety)
                if file_size >= 50 * 1024 * 1024:  
                    logger.info(f"✅ Model file size OK: {file_size} bytes")
                    return path
                else:
                    logger.warning(f"❌ Model file too small at {path}: {file_size} bytes")
            else:
                logger.info(f"❌ Path not found: {path}")
        
        logger.error("❌ No valid model file found in any path!")
        return None

    def _attempt_git_lfs_pull(self) -> bool:
        """Attempt to pull model file using Git LFS"""
        try:
            logger.info("Attempting Git LFS pull for model file...")
            import subprocess
            result = subprocess.run(['git', 'lfs', 'pull'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("Git LFS pull successful")
                return True
            else:
                logger.warning(f"Git LFS pull failed: {result.stderr}")
                return False
        except Exception as e:
            logger.warning(f"Git LFS pull failed with exception: {e}")
            return False

    def load_model(self) -> bool:
        """Load the PhoBERT SMS classifier model with robust error handling"""
        # Prevent too frequent reload attempts
        current_time = time.time()
        if (self.last_load_attempt and 
            current_time - self.last_load_attempt < 30 and 
            self.load_attempts >= self.max_load_attempts):
            logger.warning("Too many recent load attempts, skipping")
            return False
        
        self.load_attempts += 1
        self.last_load_attempt = current_time
        
        try:
            # Find model file
            self.model_path = self._find_model_file()
            
            if not self.model_path:
                logger.warning("Model file not found in local paths, attempting to download from HuggingFace...")
                
                # Try to download from HuggingFace Hub
                if self.model_downloader and self.model_downloader.download_model():
                    self.model_path = self.model_downloader.get_model_path()
                    logger.info(f"✅ Model downloaded from HuggingFace: {self.model_path}")
                else:
                    logger.error("❌ CRITICAL: Model file not found and download failed!")
                    logger.error("This means the AI model is not available - app cannot function properly")
                    return False
            
            # Verify file integrity
            file_size = os.path.getsize(self.model_path)
            logger.info(f"Loading model from: {self.model_path} (size: {file_size / (1024*1024):.1f} MB)")
            
            # Load the pickle model with comprehensive error handling
            try:
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                logger.info("Successfully loaded pickle data")
            except (pickle.UnpicklingError, EOFError, pickle.PickleError) as e:
                logger.error(f"Pickle file corrupt or incomplete: {e}")
                self._handle_corrupt_file()
                return False
            except Exception as e:
                logger.error(f"Unexpected error loading pickle file: {e}")
                return False
                
            # Extract model components safely
            if isinstance(model_data, dict):
                self.model = model_data.get('model')
                self.tokenizer = model_data.get('tokenizer')
                self.vectorizer = model_data.get('vectorizer')
                logger.info(f"Loaded model components: model={type(self.model).__name__}, "
                          f"tokenizer={self.tokenizer is not None}, vectorizer={self.vectorizer is not None}")
            else:
                # If it's just the model
                self.model = model_data
                logger.info(f"Loaded direct model: {type(self.model).__name__}")
            
            # Validate model object
            if self.model is None:
                logger.error("Model object is None after loading")
                return False
                
            # Initialize PhoBERT tokenizer if not included in pickle
            if self.tokenizer is None:
                try:
                    logger.info("Loading PhoBERT tokenizer from HuggingFace...")
                    self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
                    logger.info("Successfully loaded PhoBERT tokenizer")
                except Exception as e:
                    logger.warning(f"Could not load PhoBERT tokenizer: {e}")
                    
            self.is_loaded = True
            self.fallback_mode = False
            self.load_attempts = 0  # Reset on success
            logger.info(f"✅ Successfully loaded SMS prediction model from {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {str(e)}")
            if self.load_attempts >= self.max_load_attempts:
                self._enable_fallback_mode()
            return False

    def _handle_corrupt_file(self):
        """Handle corrupt model file"""
        if self.model_path and os.path.exists(self.model_path):
            logger.info("Attempting to remove corrupt file...")
            try:
                backup_path = f"{self.model_path}.corrupt.{int(time.time())}"
                os.rename(self.model_path, backup_path)
                logger.info(f"Corrupt file moved to: {backup_path}")
            except Exception as e:
                logger.warning(f"Could not move corrupt file: {e}")

    def _enable_fallback_mode(self):
        """Enable fallback mode with basic text classification"""
        logger.warning("⚠️ Enabling fallback mode - using basic heuristic classification")
        self.fallback_mode = True
        self.is_loaded = False
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess SMS text for prediction"""
        # Basic text cleaning
        text = text.strip().lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def _fallback_prediction(self, text: str) -> Dict[str, Union[str, float]]:
        """Enhanced heuristic-based spam detection with Vietnamese keywords"""
        spam_keywords = [
            # English keywords
            'free', 'winner', 'congratulations', 'prize', 'urgent', 'act now',
            'limited time', 'click here', 'offer expires', 'discount', '100%',
            'cash', 'money', 'earn', 'income', 'guaranteed', 'risk free',
            'no obligation', 'call now', 'don\'t delay', 'order now', 'claim',
            'bonus', 'reward', 'credit', 'loan', 'debt', 'investment',
            
            # Vietnamese keywords - enhanced spam patterns
            'chúc mừng', 'trúng thưởng', 'miễn phí', 'quà tặng', 'khuyến mãi',
            'giảm giá', 'click', 'nhấn link', 'liên hệ ngay', 'cơ hội duy nhất',
            'triệu đồng', 'tỷ đồng', 'thưởng lớn', 'may mắn', 'trúng số',
            'vay tiền', 'vay vốn', 'tín dụng', 'thẻ visa', 'bitcoin',
            'đầu tư', 'kiếm tiền', 'làm giàu', 'thu nhập', 'lợi nhuận',
            'ưu đãi', 'voucher', 'sale', 'rút tiền', 'chuyển khoản',
            'ngân hàng', 'atm', 'forex', 'crypto', '10000', '1000000',
            'triệu', 'tỷ', 'gọi ngay', 'bấm', 'nhấn', 'truy cập',
            'xổ số', 'cá cược', 'casino', 'lucky', 'win', 'won'
        ]
        
        text_lower = text.lower()
        spam_score = 0
        
        # Check for spam keywords
        for keyword in spam_keywords:
            if keyword in text_lower:
                spam_score += 1
        
        # Check for suspicious patterns
        if len([c for c in text if c.isupper()]) > len(text) * 0.3:  # Too many caps
            spam_score += 2
        
        if text.count('!') > 2:  # Too many exclamation marks
            spam_score += 1
            
        if any(char.isdigit() for char in text) and ('$' in text or 'đ' in text):  # Money mentions
            spam_score += 2
        
        # Calculate confidence based on score
        confidence = min(spam_score / 10.0, 0.9)  # Max 90% confidence for heuristics
        is_spam = spam_score >= 3
        
        return {
            "prediction": "spam" if is_spam else "ham",
            "confidence": confidence if is_spam else 1 - confidence,
            "processed_text": text,
            "fallback_score": spam_score,
            "method": "heuristic_fallback"
        }

    def predict(self, sms_content: str) -> Dict[str, Union[str, float]]:
        """
        Predict if SMS content is spam or ham
        
        Args:
            sms_content (str): SMS message content
            
        Returns:
            Dict containing prediction result
        """
        # Use fallback mode if enabled
        if self.fallback_mode:
            logger.info("Using fallback prediction method")
            return self._fallback_prediction(sms_content)
        
        # Try to load model if not loaded
        if not self.is_loaded:
            if not self.load_model():
                logger.warning("Model loading failed, using fallback")
                return self._fallback_prediction(sms_content)
        
        try:
            # Preprocess the input text
            processed_text = self.preprocess_text(sms_content)
            
            # Make prediction using the loaded model
            if hasattr(self.model, 'predict'):
                # For sklearn-like models
                prediction = self.model.predict([processed_text])[0]
                
                # Get prediction probability if available
                confidence = 0.6  # Default confidence
                if hasattr(self.model, 'predict_proba'):
                    proba = self.model.predict_proba([processed_text])[0]
                    confidence = max(proba)
                    
            elif hasattr(self.model, '__call__'):
                # For transformer models or callable models
                if self.tokenizer:
                    # Tokenize input with error handling
                    try:
                        inputs = self.tokenizer(processed_text, return_tensors="pt", 
                                              truncation=True, max_length=256, padding=True)
                        
                        with torch.no_grad():
                            outputs = self.model(**inputs)
                            
                        # Get prediction from logits
                        if hasattr(outputs, 'logits'):
                            logits = outputs.logits
                            probabilities = torch.softmax(logits, dim=-1)
                            prediction = torch.argmax(probabilities, dim=-1).item()
                            confidence = torch.max(probabilities).item()
                        else:
                            prediction = outputs[0] if isinstance(outputs, (list, tuple)) else outputs
                            confidence = 0.6
                    except Exception as tokenizer_error:
                        logger.error(f"Tokenizer error: {tokenizer_error}")
                        return self._fallback_prediction(sms_content)
                else:
                    # Fallback for models without tokenizer
                    try:
                        prediction = self.model([processed_text])[0]
                        confidence = 0.6
                    except Exception as model_error:
                        logger.error(f"Model prediction error: {model_error}")
                        return self._fallback_prediction(sms_content)
            else:
                logger.error("Model doesn't have predict method or __call__")
                return self._fallback_prediction(sms_content)
            
            # Convert prediction to spam/ham
            if isinstance(prediction, (int, np.integer)):
                result = "spam" if prediction == 1 else "ham"
            elif isinstance(prediction, str):
                result = prediction.lower()
            else:
                result = "spam" if float(prediction) > 0.5 else "ham"
                
            return {
                "prediction": result,
                "confidence": float(confidence),
                "processed_text": processed_text,
                "method": "ai_model"
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            logger.info("Falling back to heuristic prediction")
            return self._fallback_prediction(sms_content)
    
    def get_model_info(self) -> Dict[str, Union[str, bool, int]]:
        """Get comprehensive information about the model status"""
        info = {
            "model_path": self.model_path or "Not found",
            "is_loaded": self.is_loaded,
            "fallback_mode": self.fallback_mode,
            "model_type": type(self.model).__name__ if self.model else "None",
            "has_tokenizer": self.tokenizer is not None,
            "has_vectorizer": self.vectorizer is not None,
            "load_attempts": self.load_attempts,
            "last_load_attempt": self.last_load_attempt
        }
        
        # Add file size if model path exists
        if self.model_path and os.path.exists(self.model_path):
            try:
                file_size = os.path.getsize(self.model_path)
                info["model_file_size_mb"] = round(file_size / (1024 * 1024), 2)
            except:
                info["model_file_size_mb"] = "Unknown"
        
        return info

    def predict_without_lazy_loading(self, sms_content: str) -> Dict[str, Union[str, float]]:
        """
        Predict SMS classification WITHOUT lazy loading
        
        This method assumes the model is already loaded and will not attempt
        to load it automatically. Use load_model() first or POST /load-model endpoint.
        
        Args:
            sms_content: The SMS text to classify
            
        Returns:
            dict: Prediction result with confidence and method
            
        Raises:
            RuntimeError: If model is not loaded
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first or use POST /load-model endpoint")
        
        try:
            # Preprocess the input text
            processed_text = self.preprocess_text(sms_content)
            
            # Make prediction using the loaded model
            if hasattr(self.model, 'predict'):
                # For sklearn-like models
                prediction = self.model.predict([processed_text])[0]
                
                # Get prediction probability if available
                confidence = 0.6  # Default confidence
                if hasattr(self.model, 'predict_proba'):
                    proba = self.model.predict_proba([processed_text])[0]
                    confidence = max(proba)
                    
            elif hasattr(self.model, '__call__'):
                # For transformer models or callable models
                if self.tokenizer:
                    # Tokenize input with error handling
                    inputs = self.tokenizer(processed_text, return_tensors="pt", 
                                          truncation=True, max_length=256, padding=True)
                    
                    with torch.no_grad():
                        outputs = self.model(**inputs)
                        
                    # Get prediction from logits
                    if hasattr(outputs, 'logits'):
                        logits = outputs.logits
                        probabilities = torch.softmax(logits, dim=-1)
                        prediction = torch.argmax(probabilities, dim=-1).item()
                        confidence = torch.max(probabilities).item()
                    else:
                        prediction = outputs[0] if isinstance(outputs, (list, tuple)) else outputs
                        confidence = 0.6
                else:
                    # Fallback for models without tokenizer
                    prediction = self.model([processed_text])[0]
                    confidence = 0.6
            else:
                raise RuntimeError("Model doesn't have predict method or __call__")
            
            # Convert prediction to spam/ham
            if isinstance(prediction, (int, np.integer)):
                result = "spam" if prediction == 1 else "ham"
            elif isinstance(prediction, str):
                result = prediction.lower()
            else:
                result = "spam" if float(prediction) > 0.5 else "ham"
                
            return {
                "prediction": result,
                "confidence": float(confidence),
                "processed_text": processed_text,
                "method": "ai_model"
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")

    def health_check(self) -> Dict[str, Union[str, bool]]:
        """Perform a health check of the SMS prediction service"""
        try:
            # Test prediction
            test_result = self.predict("Test message for health check")
            
            return {
                "status": "healthy",
                "model_loaded": self.is_loaded,
                "fallback_mode": self.fallback_mode,
                "test_prediction": test_result.get("prediction", "unknown"),
                "test_confidence": test_result.get("confidence", 0.0),
                "prediction_method": test_result.get("method", "unknown")
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "model_loaded": self.is_loaded,
                "fallback_mode": self.fallback_mode
            }

# Global instance
sms_prediction_service = SMSPredictionService()
