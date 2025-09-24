# Deploy directly from GitHub to Railway (no Docker registry needed)
Write-Host "Deploying directly from GitHub to Railway..." -ForegroundColor Cyan
Write-Host ""

# Commit the GitHub direct config
git add .
git commit -m "feat: Railway deploy directly from GitHub (bypass registry issues)"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "Config updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "RAILWAY SETUP - GitHub Direct Deploy:" -ForegroundColor Yellow
    Write-Host "====================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "1. Go to Railway Dashboard:" -ForegroundColor White
    Write-Host "   https://railway.app/dashboard" -ForegroundColor Blue
    Write-Host ""
    Write-Host "2. Create New Project:" -ForegroundColor White
    Write-Host "   • Click 'New Project'" -ForegroundColor Gray
    Write-Host "   • Select 'Deploy from GitHub Repo'" -ForegroundColor Gray
    Write-Host "   • Choose: hoangsonmoitapcode/fraud-detection-api" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Railway will automatically:" -ForegroundColor White
    Write-Host "   • Detect Dockerfile.github" -ForegroundColor Gray
    Write-Host "   • Use railway-github-direct.json config" -ForegroundColor Gray
    Write-Host "   • Build lightweight image (no 518MB file)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. Set Environment Variables:" -ForegroundColor White
    Write-Host "   DATABASE_URL=postgresql://user:pass@host:port/db" -ForegroundColor Gray
    Write-Host "   PORT=8000" -ForegroundColor Gray
    Write-Host "   ENVIRONMENT=production" -ForegroundColor Gray
    Write-Host ""
    Write-Host "5. Deploy:" -ForegroundColor White
    Write-Host "   • Click 'Deploy'" -ForegroundColor Gray
    Write-Host "   • Build time: 3-5 minutes (first time)" -ForegroundColor Gray
    Write-Host "   • Future deploys: 2-3 minutes" -ForegroundColor Gray
    Write-Host ""
    Write-Host "BENEFITS:" -ForegroundColor Green
    Write-Host "• No Docker registry issues" -ForegroundColor Gray
    Write-Host "• Railway builds directly from source" -ForegroundColor Gray
    Write-Host "• Automatic deploys on git push" -ForegroundColor Gray
    Write-Host "• Uses optimized Dockerfile.github" -ForegroundColor Gray
    Write-Host "• Excludes large files (fast build)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Ready to create Railway project from GitHub!" -ForegroundColor Green
} else {
    Write-Host "Push failed!" -ForegroundColor Red
    exit 1
}
