# FINAL DEPLOYMENT SCRIPT - GitHub Actions + Railway Image Pull
# This is the FASTEST deployment method possible

Write-Host "🚀 FINAL DEPLOYMENT - Ultra Fast Method" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Gray
Write-Host ""

Write-Host "Step 1: Triggering GitHub Actions (lightweight build)..." -ForegroundColor Yellow

# Commit all changes
git add .
git commit -m "feat: Ultra-fast deployment - lightweight Docker image for GitHub Actions"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Changes committed" -ForegroundColor Green
    
    # Push to trigger GitHub Actions
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Push successful - GitHub Actions triggered!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 What's happening now:" -ForegroundColor White
        Write-Host "• GitHub Actions building LIGHTWEIGHT image (no 518MB file)" -ForegroundColor Gray
        Write-Host "• Build time: 2-3 minutes (much faster!)" -ForegroundColor Gray
        Write-Host "• Image size: ~1GB (vs 3GB before)" -ForegroundColor Gray
        Write-Host "• Models download at runtime (first start slower)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "🔗 Monitor build: https://github.com/hoangsonmoitapcode/fraud-detection-api/actions" -ForegroundColor Blue
        Write-Host ""
        Write-Host "⏳ Wait 2-3 minutes, then follow Railway setup below..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "RAILWAY SETUP (after GitHub Actions completes):" -ForegroundColor Green
        Write-Host "===============================================" -ForegroundColor Gray
        Write-Host ""
        Write-Host "METHOD 1 - Deploy from Docker Image (FASTEST):" -ForegroundColor White
        Write-Host "1. Go to: https://railway.app/dashboard" -ForegroundColor Blue
        Write-Host "2. Click 'New Project'" -ForegroundColor White
        Write-Host "3. Select 'Deploy from Docker Image'" -ForegroundColor White
        Write-Host "4. Image URL: ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest" -ForegroundColor Yellow
        Write-Host "5. Environment Variables:" -ForegroundColor White
        Write-Host "   DATABASE_URL=postgresql://user:pass@host:port/db" -ForegroundColor Gray
        Write-Host "   PORT=8000" -ForegroundColor Gray
        Write-Host "   ENVIRONMENT=production" -ForegroundColor Gray
        Write-Host "6. Deploy (30 seconds!)" -ForegroundColor Green
        Write-Host ""
        Write-Host "METHOD 2 - Use railway.final.json:" -ForegroundColor White
        Write-Host "1. Create project from GitHub repo" -ForegroundColor White
        Write-Host "2. Railway will use railway.final.json config" -ForegroundColor White
        Write-Host "3. Set environment variables as above" -ForegroundColor White
        Write-Host ""
        Write-Host "🎯 BENEFITS:" -ForegroundColor Green
        Write-Host "• GitHub build: 2-3 minutes (lightweight)" -ForegroundColor Gray
        Write-Host "• Railway deploy: 30 seconds (image pull)" -ForegroundColor Gray
        Write-Host "• Total time: 3-4 minutes first time" -ForegroundColor Gray
        Write-Host "• Future deploys: 30 seconds!" -ForegroundColor Gray
        Write-Host ""
        Write-Host "🔥 This is the FASTEST possible deployment method!" -ForegroundColor Red
        
    } else {
        Write-Host "❌ Push failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Commit failed!" -ForegroundColor Red
    exit 1
}
