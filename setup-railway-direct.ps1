# Setup Railway to build directly from source (backup plan)
Write-Host "Setting up Railway Direct Build (Plan B)..." -ForegroundColor Cyan
Write-Host ""

# Commit the railway-direct config
Write-Host "Committing Railway direct build config..." -ForegroundColor Yellow
git add .
git commit -m "feat: Add Railway direct build config (Plan B)"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "Config pushed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "RAILWAY SETUP INSTRUCTIONS:" -ForegroundColor Yellow
    Write-Host "===========================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "1. Go to Railway Dashboard:" -ForegroundColor White
    Write-Host "   https://railway.app/dashboard" -ForegroundColor Blue
    Write-Host ""
    Write-Host "2. Create New Project:" -ForegroundColor White
    Write-Host "   • Click 'New Project'" -ForegroundColor Gray
    Write-Host "   • Select 'Deploy from GitHub Repo'" -ForegroundColor Gray
    Write-Host "   • Choose: hoangsonmoitapcode/fraud-detection-api" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Configure Build:" -ForegroundColor White
    Write-Host "   • Railway will auto-detect Dockerfile.simple" -ForegroundColor Gray
    Write-Host "   • Or manually set: Dockerfile.simple" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. Set Environment Variables:" -ForegroundColor White
    Write-Host "   DATABASE_URL=postgresql://user:pass@host:port/db" -ForegroundColor Gray
    Write-Host "   PORT=8000" -ForegroundColor Gray
    Write-Host "   ENVIRONMENT=production" -ForegroundColor Gray
    Write-Host ""
    Write-Host "5. Deploy:" -ForegroundColor White
    Write-Host "   • Click 'Deploy'" -ForegroundColor Gray
    Write-Host "   • Build time: 3-5 minutes (lighter build)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "BENEFITS of this approach:" -ForegroundColor Green
    Write-Host "• No GitHub Actions complexity" -ForegroundColor Gray
    Write-Host "• Railway builds directly from source" -ForegroundColor Gray
    Write-Host "• Excludes large files (518MB pkl file)" -ForegroundColor Gray
    Write-Host "• Models download at runtime (first startup slower)" -ForegroundColor Gray
    Write-Host "• Subsequent deploys are fast" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Ready to create Railway project!" -ForegroundColor Green
} else {
    Write-Host "Push failed!" -ForegroundColor Red
    exit 1
}
