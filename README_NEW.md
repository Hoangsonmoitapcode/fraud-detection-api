# Fraud Detection API

A comprehensive fraud detection API built with FastAPI, featuring phone number analysis, SMS spam detection, banking account verification, and website scam checking.

## Features

- **Phone Number Fraud Detection**: Analyze Vietnamese phone numbers for fraud risk
- **SMS Spam Detection**: AI-powered SMS spam classification using PhoBERT
- **Banking Account Verification**: Check if banking accounts are reported as scam
- **Website Scam Detection**: Verify if websites are flagged as scam/phishing
- **Batch Processing**: Support for analyzing multiple items at once
- **RESTful API**: Clean, documented API endpoints

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL (for production)
- Git LFS (for model files)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/fraud-detection-api.git
cd fraud-detection-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp config/env.example .env
# Edit .env with your database URL and other settings
```

4. Run database migrations:
```bash
cd database
python manage_db.py upgrade
```

5. Start the API:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## Project Structure

```
fraud-detection-api/
├── src/                    # Source code
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database configuration
│   ├── phone_service.py   # Phone number analysis
│   └── sms_prediction_service.py  # SMS spam detection
├── models/                 # Model files
│   ├── trained/           # Trained model files
│   ├── backups/           # Model backups
│   └── exports/           # Deployment-ready models
├── scripts/               # Utility scripts
│   └── load_trained_model.py
├── tests/                 # Test files
│   └── test_api.py
├── deployment/            # Deployment configurations
│   ├── railway/           # Railway deployment files
│   └── Dockerfile         # Docker configuration
├── database/              # Database migrations
├── config/                # Configuration files
└── requirements.txt       # Dependencies
```

## Model Management

### Loading Trained Models

1. Place your trained model files in `models/trained/`:
   - `config.json`
   - `model.safetensors` (or `pytorch_model.bin`)
   - `tokenizer_config.json`
   - `vocab.txt`
   - `bpe.codes`

2. Run the model loading script:
```bash
python scripts/load_trained_model.py
```

3. Test the model:
```bash
python tests/test_api.py
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Usage Examples

### Phone Number Analysis
```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"phone_numbers": ["0123456789"]}'
```

### SMS Spam Detection
```bash
curl -X POST "http://localhost:8000/predict-sms/" \
  -H "Content-Type: application/json" \
  -d '{"sms_content": "Congratulations! You won $10000!"}'
```

### Banking Account Check
```bash
curl -X GET "http://localhost:8000/check-banking/?account_number=123456789&bank_name=Vietcombank"
```

### Website Scam Check
```bash
curl -X GET "http://localhost:8000/check-website/?website_url=https://example.com"
```

## Deployment

### Railway Deployment

1. Follow the Railway deployment guide: `deployment/railway/RAILWAY_DEPLOYMENT_GUIDE.md`
2. Set up environment variables in Railway dashboard
3. Deploy using the provided configuration

### Docker Deployment

```bash
docker build -f deployment/Dockerfile -t fraud-detection-api .
docker run -p 8000:8000 fraud-detection-api
```

## Testing

Run the test suite:
```bash
python tests/test_api.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub.
