# Setup Railway Environment Variables
# Run this script to set up environment variables in Railway

Write-Host "🚀 Setting up Railway Environment Variables..." -ForegroundColor Green

Write-Host ""
Write-Host "📋 Environment Variables to set in Railway Dashboard:" -ForegroundColor Yellow
Write-Host "1. Go to Railway Dashboard → Your Project → Fraud Detection Service" -ForegroundColor White
Write-Host "2. Click on 'Variables' tab" -ForegroundColor White
Write-Host "3. Add these variables:" -ForegroundColor White
Write-Host ""

Write-Host "   RAILWAY_ENVIRONMENT = production" -ForegroundColor Cyan
Write-Host "   MODEL_PATH = /app/phobert_sms_classifier.pkl" -ForegroundColor Cyan
Write-Host "   PORT = 8000" -ForegroundColor Cyan
Write-Host "   PYTHONUNBUFFERED = 1" -ForegroundColor Cyan
Write-Host "   PYTHONDONTWRITEBYTECODE = 1" -ForegroundColor Cyan
Write-Host "   TOKENIZERS_PARALLELISM = false" -ForegroundColor Cyan

Write-Host ""
Write-Host "4. Click 'Add' for each variable" -ForegroundColor White
Write-Host "5. Click 'Deploy' to restart the service" -ForegroundColor White

Write-Host ""
Write-Host "✅ After setting variables, test with:" -ForegroundColor Green
Write-Host "   curl -X POST https://your-railway-url.com/load-model" -ForegroundColor White

Write-Host ""
Write-Host "🔗 Railway Dashboard: https://railway.app/dashboard" -ForegroundColor Blue
