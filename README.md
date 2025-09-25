# Fraud Detection API

A FastAPI-based fraud detection service with AI-powered SMS spam classification using PhoBERT model.

## Features

- **SMS Spam Detection**: AI-powered classification using PhoBERT model
- **FastAPI**: High-performance web framework
- **PostgreSQL**: Database integration
- **Docker**: Containerized deployment
- **Railway**: Cloud deployment ready
- **Git LFS**: Large model file management

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hoangsonmoitapcode/fraud-detection-api.git
   cd fraud-detection-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t fraud-detection-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 fraud-detection-api
   ```

### Railway Deployment

1. **Connect to Railway**
   - Import from GitHub repository
   - Set environment variables:
     - `DATABASE_URL`: PostgreSQL connection string
     - `PORT`: 8000 (auto-set by Railway)

2. **Deploy**
   - Railway will automatically build and deploy using the Dockerfile
   - The AI model (518MB) is included via Git LFS

## API Endpoints

### Health Check
```
GET /health
```

### SMS Spam Detection
```
POST /predict/sms
Content-Type: application/json

{
  "message": "Your SMS message here"
}
```

Response:
```json
{
  "prediction": "spam" | "ham",
  "confidence": 0.95,
  "message": "Your SMS message here"
}
```

## Project Structure

```
├── src/                    # Source code
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   ├── database.py        # Database configuration
│   └── sms_prediction_service.py  # AI prediction service
├── phobert_sms_classifier.pkl  # AI model (518MB, Git LFS)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── Procfile             # Railway deployment
└── .github/workflows/   # GitHub Actions CI/CD
```

## Technology Stack

- **Backend**: FastAPI, Python 3.11
- **AI Model**: PhoBERT (Vietnamese BERT)
- **Database**: PostgreSQL
- **Deployment**: Docker, Railway
- **CI/CD**: GitHub Actions
- **File Storage**: Git LFS

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `PORT`: Application port (default: 8000)

## Development

### Adding New Features

1. Create feature branch
2. Implement changes
3. Test locally
4. Submit pull request

### Testing

```bash
# Run tests
pytest

# Test SMS prediction
curl -X POST "http://localhost:8000/predict/sms" \
     -H "Content-Type: application/json" \
     -d '{"message": "Test message"}'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support, email support@example.com or create an issue in the repository.
