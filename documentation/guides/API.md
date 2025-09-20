# API Documentation

## Authentication
Currently, the API does not require authentication. This may be added in future versions.

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Add Phone Number to Database
**POST** `/users/`

Add a phone number to the database with automatic fraud detection and region analysis.

**Request Body:**
```json
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
  "heading_id": 1
}
```

### 2. Analyze Phone Number
**POST** `/analyze/`

Analyze a phone number for fraud detection without saving it to the database.

**Request Body:** (form data)
```
phone_number: 0965842855
```

**Response:**
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

### 3. Confirm Risky Number
**POST** `/confirm-risky/`

Confirm that a number is risky/scam/spam and add it to the database.

**Request Body:**
```json
{
  "phone_number": "0123456789",
  "confirmation_type": "scam"
}
```

**Response:**
```json
{
  "id": 2,
  "phone_number": "0123456789",
  "phone_head": "012",
  "phone_region": "Unknown",
  "label": "unsafe",
  "heading_id": null
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting
Currently, there are no rate limits implemented. Consider implementing rate limiting for production use.

## Data Models

### User
- `id`: Integer (Primary Key)
- `phone_number`: String (Unique)
- `phone_head`: String (Phone prefix)
- `phone_region`: String (Detected region)
- `label`: String ("safe" or "unsafe")
- `heading_id`: Integer (Foreign Key to phone_headings)

### PhoneHeading
- `id`: Integer (Primary Key)
- `heading`: String (Phone prefix)
- `region`: String (Region name)
- `status`: String ("safe" or "unsafe")
