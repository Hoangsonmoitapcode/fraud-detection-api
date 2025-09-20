# 🛡️ Comprehensive Fraud Detection System

A powerful FastAPI-based fraud detection system for analyzing multiple types of fraud: **phone numbers**, **SMS content**, **banking accounts**, and **websites**. Complete with automatic region detection and real-time risk assessment.

## ✨ Features

### 📱 **Phone Number Fraud Detection**
- **Automatic Region Detection**: Detect phone number regions and carriers
- **International Support**: Handle phone numbers from multiple countries
- **Risk Assessment**: Real-time fraud risk evaluation
- **Crowdsourced Reporting**: User-confirmed risky numbers
- **Batch Processing**: Analyze multiple phone numbers at once

### 💬 **SMS Scam Detection**
- **Content Analysis**: Analyze SMS content for spam/scam patterns
- **Fuzzy Matching**: Find similar SMS content with advanced matching
- **Pattern Recognition**: Detect common scam SMS patterns
- **Real-time Checking**: Instant SMS spam verification
- **Batch Reporting**: Report multiple SMS messages simultaneously

### 🏦 **Banking Scam Detection**
- **Account Monitoring**: Track reported scam banking accounts
- **Multi-bank Support**: Support for various banks
- **Real-time Verification**: Check accounts before money transfer
- **Fraud Prevention**: Prevent transfers to known scam accounts
- **Duplicate Detection**: Prevent duplicate scam reports

### 🌐 **Website Scam Detection**
- **URL Analysis**: Detect phishing and scam websites
- **Real-time Protection**: Check websites before access
- **Label Classification**: Categorize websites as safe/scam
- **Phishing Prevention**: Protect users from malicious sites
- **Batch URL Processing**: Check multiple websites at once

### 🔧 **System Monitoring & Health**
- **API Status Endpoint**: Real-time system status with metrics
- **Health Check**: Database connectivity and system health monitoring
- **System Metrics**: CPU and memory usage tracking
- **Uptime Monitoring**: Server uptime and performance metrics

## 🚀 Quick Start

### 📁 **Quick Navigation**
- 🆕 **New user?** → **[START_HERE.md](START_HERE.md)** ← Start here!
- 🗺️ **Lost in files?** → **[📁_DIRECTORY_GUIDE.md](📁_DIRECTORY_GUIDE.md)** ← Visual guide
- 📋 **Step-by-step setup?** → **[setup/SETUP_CHECKLIST.md](setup/SETUP_CHECKLIST.md)**
- 📚 **Detailed help?** → **[docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)**

### For New Users (No Python/PostgreSQL)
👥 **If you're sharing this with someone who doesn't have Python or PostgreSQL installed:**
1. See: **[START_HERE.md](START_HERE.md)** ← **Start here first!**
2. Use: **[setup/SETUP_CHECKLIST.md](setup/SETUP_CHECKLIST.md)**
3. Run: **`setup/FIRST_TIME_SETUP.bat`**

### Prerequisites (For Experienced Users)

- Python 3.11+ (tested with Python 3.13.7)
- PostgreSQL database
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd FraudDetection
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r config/requirements.txt
   ```

5. **Set up database**
   - Create a PostgreSQL database named `fastapi_db`
   - Update database credentials in `src/database.py` if needed

6. **Run database migrations**
   ```bash
   python database/manage_db.py migrate
   ```
   Or use: `database\manage_db.bat migrate`

7. **Start the server**
   ```bash
   python -m uvicorn src.main:app --reload
   ```
   Or use the batch file: `scripts\start_server.bat`

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| **System Endpoints** | | |
| GET | `/` | API status with system metrics and available endpoints |
| GET | `/health` | Health check endpoint for monitoring systems |
| **Phone Number Endpoints** | | |
| POST | `/users/` | Add phone number(s) to database with fraud analysis (batch support) |
| POST | `/analyze/` | Check if number(s) are risky without saving (batch support) |
| POST | `/confirm-risky/` | Confirm risky number and add to database |
| **SMS Scam Endpoints** | | |
| POST | `/sms-scam/` | Report SMS content as spam/scam (batch support) |
| GET | `/check-sms/` | Check if SMS content is spam (fuzzy matching) |
| **Banking Scam Endpoints** | | |
| POST | `/banking-scam/` | Report banking account as scam (batch support) |
| GET | `/check-banking/` | Check if banking account is reported as scam |
| **Website Scam Endpoints** | | |
| POST | `/website-scam/` | Report website as scam/phishing (batch support) |
| GET | `/check-website/` | Check if website is reported as scam |

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Status**: http://localhost:8000/ (shows all available endpoints)

## 🔧 Usage Examples

### 🔧 **System Status Examples**

#### 0. Check API Status
```bash
curl "http://localhost:8000/"
```

#### 0.1. Check System Health
```bash
curl "http://localhost:8000/health"
```

### 📱 **Phone Number Examples**

#### 1. Analyze Phone Number (without saving)
```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'
```

#### 2. Add Phone Number to Database
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855"]}'
```

#### 2.1. Batch Phone Number Analysis
```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0965842855", "0123456789", "+84987654321"]}'
```

#### 3. Confirm Risky Number
```bash
curl -X POST "http://localhost:8000/confirm-risky/" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0965842855",
    "confirmation_type": "scam"
  }'
```

### 💬 **SMS Scam Examples**

#### 4. Report SMS Spam (Single)
```bash
curl -X POST "http://localhost:8000/sms-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "sms_messages": [{
      "sms_content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng",
      "label": "spam"
    }]
  }'
```

#### 4.1. Report SMS Spam (Batch)
```bash
curl -X POST "http://localhost:8000/sms-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "sms_messages": [
      {
        "sms_content": "Chúc mừng! Bạn đã trúng thưởng 100 triệu đồng",
        "label": "spam"
      },
      {
        "sms_content": "Nhấn link để nhận tiền thưởng ngay",
        "label": "scam"
      }
    ]
  }'
```

#### 5. Check SMS Content
```bash
curl "http://localhost:8000/check-sms/?sms_content=Chúc mừng bạn trúng thưởng"
```

### 🏦 **Banking Scam Examples**

#### 6. Report Banking Scam (Single)
```bash
curl -X POST "http://localhost:8000/banking-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "banking_accounts": [{
      "account_number": "1234567890",
      "bank_name": "Vietcombank"
    }]
  }'
```

#### 6.1. Report Banking Scam (Batch)
```bash
curl -X POST "http://localhost:8000/banking-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "banking_accounts": [
      {
        "account_number": "1234567890",
        "bank_name": "Vietcombank"
      },
      {
        "account_number": "9876543210",
        "bank_name": "Techcombank"
      }
    ]
  }'
```

#### 7. Check Banking Account
```bash
curl "http://localhost:8000/check-banking/?account_number=1234567890&bank_name=Vietcombank"
```

### 🌐 **Website Scam Examples**

#### 8. Report Website Scam (Single)
```bash
curl -X POST "http://localhost:8000/website-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "websites": [{
      "website_url": "https://fake-bank-site.com",
      "label": "scam"
    }]
  }'
```

#### 8.1. Report Website Scam (Batch)
```bash
curl -X POST "http://localhost:8000/website-scam/" \
  -H "Content-Type: application/json" \
  -d '{
    "websites": [
      {
        "website_url": "https://fake-bank-site.com",
        "label": "scam"
      },
      {
        "website_url": "https://phishing-site.net",
        "label": "phishing"
      }
    ]
  }'
```

#### 9. Check Website Safety
```bash
curl "http://localhost:8000/check-website/?website_url=https://suspicious-site.com"
```

## 📁 Project Structure

```
FraudDetection/
├── src/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI application with all endpoints
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   └── phone_service.py   # Phone analysis logic
├── database/              # Database management
│   ├── alembic/           # Database migrations
│   ├── manage_db.py       # Database management script
│   ├── manage_db.bat      # Windows batch script
│   └── alembic.ini        # Alembic configuration
├── config/                # Configuration files
│   ├── requirements.txt   # Python dependencies
│   └── env.example        # Environment variables example
├── scripts/               # Utility scripts
│   ├── start_server.bat   # Start server script
│   └── setup.bat          # Setup script
├── setup/                 # Setup and installation
│   ├── FIRST_TIME_SETUP.bat
│   ├── quick-start.bat
│   └── SETUP_CHECKLIST.md
├── tests/                 # Test files
├── docs/                  # Documentation
├── test_api_status.py     # API status testing script
├── test_with_json_data.py # JSON data testing script
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🗄️ Database Schema

- **users**: Store phone numbers with analysis results
- **phone_headings**: Phone number prefixes and regions
- **sms_scams**: Store SMS content and spam classification
- **banking_scams**: Store reported scam banking accounts
- **website_scams**: Store reported scam/phishing websites
- **alembic_version**: Database migration tracking

## 🛠️ Development

### Running Tests
```bash
# Test phone number fraud detection
python tests/test_fraud_detection.py

# Test new scam features (SMS, Banking, Website)
python tests/test_new_scam_features.py

# Or use pytest
python -m pytest tests/
```

### Database Management
```bash
# Create new migration
cd database
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Or use the management script
python database/manage_db.py migrate

# Or use the batch file
database\manage_db.bat migrate
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and test
3. Commit: `git commit -m "Add new feature"`
4. Push: `git push origin feature/new-feature`
5. Create pull request

## 📊 API Response Examples

### Successful Analysis
```json
{
  "phone_number": "0965842855",
  "analysis": {
    "phone_head": "096",
    "phone_region": "Vietnam",
    "label": "safe",
    "heading_id": 1
  },
  "fraud_risk": "LOW"
}
```

### Risky Number Detection
```json
{
  "phone_number": "0123456789",
  "analysis": {
    "phone_head": "012",
    "phone_region": "Unknown",
    "label": "unsafe",
    "heading_id": null
  },
  "fraud_risk": "HIGH"
}
```

## 🔒 Security

- Input validation using Pydantic schemas
- SQL injection prevention with SQLAlchemy ORM
- Environment-based configuration
- Database connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Commit your changes
6. Push to your fork
7. Create a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

## 🔄 Version History

- **v3.1.0**: Added system monitoring, health checks, and enhanced API status
- **v3.0.0**: Added comprehensive fraud detection (SMS, Banking, Website scam detection)
- **v2.0.0**: Added confirm-risky endpoint, simplified API  
- **v1.0.0**: Initial release with basic phone number fraud detection

## 🎯 New Features in v3.1.0

### 🔧 **System Monitoring & Health**
- **API Status Endpoint**: Real-time system status with metrics
- **Health Check**: Database connectivity and system health monitoring
- **System Metrics**: CPU and memory usage tracking
- **Uptime Monitoring**: Server uptime and performance metrics
- **Enhanced Error Handling**: Better error handling and dependency management

### 📊 **Enhanced Batch Processing**
- All endpoints now support batch operations
- Improved performance for bulk operations
- Better response formatting with summaries

### 🛠️ **Improved Development Experience**
- Enhanced API documentation
- Better project structure organization
- Comprehensive testing scripts
- Improved setup and installation process

## 🎯 Features in v3.0.0

### 💬 **SMS Scam Detection**
- Report and check SMS spam content
- Fuzzy matching for similar SMS detection
- Risk level assessment (HIGH/MEDIUM/LOW)

### 🏦 **Banking Scam Detection**  
- Report scam banking accounts
- Real-time account verification
- Multi-bank support

### 🌐 **Website Scam Detection**
- Report phishing/scam websites
- URL safety checking
- Real-time protection

### 🧪 **Enhanced Testing**
- Comprehensive test suite for all features
- API endpoint testing
- Database integration testing
