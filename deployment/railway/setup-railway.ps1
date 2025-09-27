# Railway Setup Script
# Hướng dẫn tự động setup Railway service

Write-Host "🚀 Railway Deployment Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

Write-Host "`n📋 Các bước cần thực hiện:" -ForegroundColor Yellow

Write-Host "`n1️⃣ Tạo Railway Project:" -ForegroundColor Cyan
Write-Host "   - Đăng nhập: https://railway.app" -ForegroundColor White
Write-Host "   - Click 'New Project'" -ForegroundColor White
Write-Host "   - Chọn 'Empty Project'" -ForegroundColor White

Write-Host "`n2️⃣ Thêm Service:" -ForegroundColor Cyan
Write-Host "   - Click 'New Service'" -ForegroundColor White
Write-Host "   - Chọn 'GitHub Repo'" -ForegroundColor White
Write-Host "   - Chọn: Hoangsonmoitapcode/fraud-detection-api" -ForegroundColor White

Write-Host "`n3️⃣ Thêm PostgreSQL Database:" -ForegroundColor Cyan
Write-Host "   - Click 'New Service'" -ForegroundColor White
Write-Host "   - Chọn 'Database' → 'PostgreSQL'" -ForegroundColor White

Write-Host "`n4️⃣ Cấu hình Environment Variables:" -ForegroundColor Cyan
Write-Host "   Vào Settings → Variables và thêm:" -ForegroundColor White
Write-Host "   - PORT=8000" -ForegroundColor Green
Write-Host "   - ENVIRONMENT=production" -ForegroundColor Green
Write-Host "   - DATABASE_URL (sẽ tự động tạo từ PostgreSQL)" -ForegroundColor Green

Write-Host "`n5️⃣ Cấu hình Deploy Settings:" -ForegroundColor Cyan
Write-Host "   Vào Settings → Deploy:" -ForegroundColor White
Write-Host "   - Build Command: (để trống)" -ForegroundColor Green
Write-Host "   - Start Command: (để trống)" -ForegroundColor Green
Write-Host "   - Dockerfile Path: deployment/Dockerfile" -ForegroundColor Green

Write-Host "`n🔗 URLs sau khi deploy:" -ForegroundColor Yellow
Write-Host "   - API: https://your-service-name.up.railway.app" -ForegroundColor White
Write-Host "   - Health: https://your-service-name.up.railway.app/health" -ForegroundColor White
Write-Host "   - Docs: https://your-service-name.up.railway.app/docs" -ForegroundColor White

Write-Host "`n🧪 Test Commands:" -ForegroundColor Yellow
Write-Host "   # Health Check" -ForegroundColor White
Write-Host "   curl https://your-service-name.up.railway.app/health" -ForegroundColor Green

Write-Host "`n   # SMS Prediction" -ForegroundColor White
Write-Host "   curl -X POST `"https://your-service-name.up.railway.app/predict/sms`" \" -ForegroundColor Green
Write-Host "        -H `"Content-Type: application/json`" \" -ForegroundColor Green
Write-Host "        -d `"{`"message`": `"Test message`"}`"" -ForegroundColor Green

Write-Host "`n✅ Hoàn thành! Railway service sẽ tự động deploy từ GitHub." -ForegroundColor Green
Write-Host "📊 Kiểm tra logs trong Railway dashboard để theo dõi quá trình deploy." -ForegroundColor Yellow
