# 🛡️ Automated Fraud Detection System

## Overview
Your fraud detection system now automatically analyzes phone numbers and detects potential fraud based on international phone headings. The system treats **Vietnam (+84) phone numbers as SAFE** and **all other international numbers as potentially UNSAFE**.

## 🚀 Key Features

### 1. **Automatic Phone Number Parsing**
- Extracts phone headings from any format
- Supports both international (+84, +1) and domestic (096, 097) formats
- Automatically detects region and safety status

### 2. **International Phone Headings Database**
- Pre-populated with 94+ international country codes
- Vietnam numbers marked as "safe" (including new carriers)
- All other countries marked as "unsafe" (potential fraud)
- Easy to manage and update
- **NEW**: Added support for iTel, Vietnamobile, Wintel, VNPAY Sky

### 3. **Real-time Fraud Detection**
- Instant analysis of phone numbers
- Risk assessment (HIGH/LOW)
- Automatic classification

## 📊 API Endpoints

### Phone Number Analysis
```http
POST /analyze/?phone_number=0965842855
```
**Response:**
```json
{
  "phone_number": "0965842855",
  "analysis": {
    "phone_head": "096",
    "phone_region": "Vietnam", 
    "label": "safe",
    "heading_id": 86
  },
  "fraud_risk": "LOW"
}
```

### User Creation with Auto-Detection
```http
POST /users/
Content-Type: application/json

{
  "phone_number": "0965842855"
}
```
**Response:**
```json
{
  "id": 1,
  "phone_number": "0965842855",
  "phone_head": "096",
  "phone_region": "Vietnam",
  "label": "safe",
  "heading_id": 86
}
```

### Phone Headings Management
```http
GET /headings/          # Get all headings
POST /headings/         # Create new heading
GET /headings/{id}      # Get specific heading
```

## 🔍 Fraud Detection Logic

### Safe Numbers (Vietnam)
- **Country Code:** +84
- **Traditional Carriers:** 096, 097, 098, 032-039, 070, 076-079, 081-085, 088, 091, 094
- **New Carriers:**
  - **iTel:** 087
  - **Vietnamobile:** 092, 056, 058
  - **Wintel:** 099
  - **VNPAY Sky:** 089
- **Additional Prefixes:** 059, 090, 093, 095
- **Status:** SAFE
- **Fraud Risk:** LOW

### Unsafe Numbers (International)
- **Examples:** +1 (USA), +44 (UK), +86 (China), +91 (India)
- **Status:** UNSAFE  
- **Fraud Risk:** HIGH

### Unknown Numbers
- Numbers not in database
- **Status:** UNSAFE (by default)
- **Fraud Risk:** HIGH

## 🛠️ Database Management

### Populate Phone Headings Database
```bash
# Using manage_db.py
.venv\Scripts\python.exe manage_db.py populate

# Or directly
.venv\Scripts\python.exe -c "from src.populate_headings import populate_phone_headings; populate_phone_headings()"
```

### Database Commands
```bash
.venv\Scripts\python.exe manage_db.py status    # Check migration status
.venv\Scripts\python.exe manage_db.py migrate   # Apply migrations
.venv\Scripts\python.exe manage_db.py populate  # Populate headings
```

## 📱 Phone Number Examples

### Vietnamese Numbers (SAFE)
- `0965842855` → 096, Vietnam, SAFE (Traditional)
- `+84965842855` → +84, Vietnam, SAFE (International format)
- `0328123456` → 032, Vietnam, SAFE (Traditional)
- `0870123456` → 087, Vietnam, SAFE (iTel)
- `0920123456` → 092, Vietnam, SAFE (Vietnamobile)
- `0560123456` → 056, Vietnam, SAFE (Vietnamobile)
- `0990123456` → 099, Vietnam, SAFE (Wintel)
- `0890123456` → 089, Vietnam, SAFE (VNPAY Sky)

### International Numbers (UNSAFE)
- `+1234567890` → +1, USA/Canada, UNSAFE
- `+447123456789` → +44, United Kingdom, UNSAFE
- `+8613812345678` → +86, China, UNSAFE

## 🔧 Customization

### Adding New Safe Headings
```http
POST /headings/
Content-Type: application/json

{
  "heading": "070",
  "region": "Vietnam", 
  "status": "safe"
}
```

### Marking International Numbers as Safe
```http
POST /headings/
Content-Type: application/json

{
  "heading": "+65",
  "region": "Singapore",
  "status": "safe"
}
```

## 📈 Usage Statistics

After population, your database contains:
- **35 Vietnamese headings** (SAFE) - Including new carriers
- **59 International headings** (UNSAFE)
- **Total: 94 phone headings**

### New Carriers Added (2025)
- **iTel (Indochina Telecom)**: 087
- **Vietnamobile**: 092, 056, 058
- **Wintel (VNPT)**: 099
- **VNPAY Sky**: 089
- **Additional Vietnam prefixes**: 059, 090, 093, 095

## 🔐 Security Features

1. **Automatic Detection:** No manual input required
2. **Database-Driven:** Easy to update fraud patterns
3. **Real-time Analysis:** Instant fraud risk assessment
4. **Flexible Rules:** Easily modify safe/unsafe criteria
5. **Audit Trail:** All phone numbers stored with analysis results

## 🚨 Fraud Detection Workflow

1. **User submits phone number** → `POST /users/`
2. **System extracts phone heading** → `096` from `0965842855`
3. **System queries headings database** → Found: Vietnam, Safe
4. **System assigns fraud risk** → LOW risk
5. **User record created** with automatic classification

## 💡 Best Practices

1. **Regularly update** the headings database with new fraud patterns
2. **Monitor** phone numbers marked as UNSAFE for patterns
3. **Review** and adjust country-specific rules as needed
4. **Use the analyze endpoint** for real-time checks without storing data
5. **Backup** your database before major updates

Your fraud detection system is now fully automated and ready to protect against international phone fraud! 🛡️✨

