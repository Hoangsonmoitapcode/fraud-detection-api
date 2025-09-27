# Test Railway API Script
param(
    [Parameter(Mandatory=$true)]
    [string]$RailwayUrl
)

Write-Host "🧪 Testing Railway API" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green
Write-Host "URL: $RailwayUrl" -ForegroundColor Yellow

# Test Health Check
Write-Host "`n1️⃣ Testing Health Check..." -ForegroundColor Cyan
try {
    $healthResponse = Invoke-RestMethod -Uri "$RailwayUrl/health" -Method GET
    Write-Host "✅ Health Check: $($healthResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test SMS Prediction
Write-Host "`n2️⃣ Testing SMS Prediction..." -ForegroundColor Cyan
$testMessage = @{
    message = "Chào bạn, đây là tin nhắn test từ PowerShell"
} | ConvertTo-Json

try {
    $predictionResponse = Invoke-RestMethod -Uri "$RailwayUrl/predict/sms" -Method POST -Body $testMessage -ContentType "application/json"
    Write-Host "✅ SMS Prediction:" -ForegroundColor Green
    Write-Host "   Message: $($predictionResponse.message)" -ForegroundColor White
    Write-Host "   Prediction: $($predictionResponse.prediction)" -ForegroundColor White
    Write-Host "   Confidence: $($predictionResponse.confidence)" -ForegroundColor White
} catch {
    Write-Host "❌ SMS Prediction Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test API Documentation
Write-Host "`n3️⃣ Testing API Documentation..." -ForegroundColor Cyan
try {
    $docsResponse = Invoke-WebRequest -Uri "$RailwayUrl/docs" -Method GET
    if ($docsResponse.StatusCode -eq 200) {
        Write-Host "✅ API Documentation accessible" -ForegroundColor Green
        Write-Host "   URL: $RailwayUrl/docs" -ForegroundColor White
    }
} catch {
    Write-Host "❌ API Documentation not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Testing completed!" -ForegroundColor Green
Write-Host "📊 Check Railway dashboard for detailed logs and metrics." -ForegroundColor Yellow
