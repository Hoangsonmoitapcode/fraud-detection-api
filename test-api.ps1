# Quick API testing script
param(
    [string]$BaseUrl = ""
)

if (-not $BaseUrl) {
    Write-Host "Usage: ./test-api.ps1 -BaseUrl https://your-app.railway.app" -ForegroundColor Yellow
    Write-Host "Get your Railway URL from: Railway Dashboard → Service → Settings → Domains" -ForegroundColor Cyan
    exit 1
}

Write-Host "Testing Railway API: $BaseUrl" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Test 1: Health Check
Write-Host "1. Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method GET -TimeoutSec 30
    Write-Host "✅ Health: $($health.status)" -ForegroundColor Green
    Write-Host "   Database: $($health.checks.database)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Root endpoint
Write-Host "`n2. Root Endpoint..." -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "$BaseUrl/" -Method GET -TimeoutSec 30
    Write-Host "✅ API: $($root.message)" -ForegroundColor Green
    Write-Host "   Version: $($root.version)" -ForegroundColor Gray
    Write-Host "   Status: $($root.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Phone Analysis
Write-Host "`n3. Phone Analysis..." -ForegroundColor Yellow
try {
    $phoneData = @{
        phone_numbers = @("0123456789")
    }
    $phoneResult = Invoke-RestMethod -Uri "$BaseUrl/analyze/" -Method POST -Body ($phoneData | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 30
    Write-Host "✅ Phone analysis working" -ForegroundColor Green
    Write-Host "   Phone: $($phoneResult.phone_number)" -ForegroundColor Gray
    Write-Host "   Risk: $($phoneResult.fraud_risk)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Phone analysis failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: SMS Prediction (might be slow first time)
Write-Host "`n4. SMS Prediction..." -ForegroundColor Yellow
try {
    $smsData = @{
        sms_content = "Xin chao ban"
    }
    Write-Host "   (This might take 2-3 minutes on first call - downloading model)" -ForegroundColor Cyan
    $smsResult = Invoke-RestMethod -Uri "$BaseUrl/predict-sms/" -Method POST -Body ($smsData | ConvertTo-Json) -ContentType "application/json" -TimeoutSec 180
    Write-Host "✅ SMS prediction working" -ForegroundColor Green
    Write-Host "   Prediction: $($smsResult.prediction)" -ForegroundColor Gray
    Write-Host "   Confidence: $($smsResult.confidence)" -ForegroundColor Gray
} catch {
    Write-Host "❌ SMS prediction failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   (This is expected if model hasn't downloaded yet)" -ForegroundColor Yellow
}

Write-Host "`n🔗 Useful Links:" -ForegroundColor Cyan
Write-Host "   API Docs: $BaseUrl/docs" -ForegroundColor Blue
Write-Host "   ReDoc: $BaseUrl/redoc" -ForegroundColor Blue
Write-Host "   Health: $BaseUrl/health" -ForegroundColor Blue

Write-Host "`n✅ Testing completed!" -ForegroundColor Green
