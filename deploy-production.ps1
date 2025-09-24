# Complete production deployment script
# This will trigger GitHub Actions and guide Railway setup

param(
    [string]$Message = "Production deployment with pre-installed dependencies",
    [switch]$SkipBuild,
    [switch]$ForceRebuild
)

Write-Host "🚀 Starting Production Deployment Process..." -ForegroundColor Cyan
Write-Host ""

if (-not $SkipBuild) {
    Write-Host "📦 Step 1: Triggering GitHub Actions Build..." -ForegroundColor Yellow
    
    # Commit changes if any
    $hasChanges = git status --porcelain
    if ($hasChanges) {
        Write-Host "📝 Committing pending changes..." -ForegroundColor White
        git add .
        git commit -m "deploy: $Message"
    }
    
    # Create deployment commit
    git commit --allow-empty -m "build: $Message"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Deployment commit created" -ForegroundColor Green
        
        Write-Host "🔄 Pushing to trigger GitHub Actions..." -ForegroundColor Cyan
        git push origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Push successful!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🔗 Monitor build progress:" -ForegroundColor White
            Write-Host "   https://github.com/hoangsonmoitapcode/fraud-detection-api/actions" -ForegroundColor Blue
            Write-Host ""
            Write-Host "⏱️  Build will take 5-8 minutes (heavy but complete image)" -ForegroundColor Yellow
            Write-Host "📦 Image will be available at:" -ForegroundColor White
            Write-Host "   ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest" -ForegroundColor Blue
        } else {
            Write-Host "❌ Push failed!" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "❌ Failed to create deployment commit!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⏭️  Skipping build (using existing image)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🛤️  Step 2: Railway Deployment Guide" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Gray
Write-Host ""
Write-Host "1️⃣  Go to Railway Dashboard:" -ForegroundColor White
Write-Host "   https://railway.app/dashboard" -ForegroundColor Blue
Write-Host ""
Write-Host "2️⃣  Create New Project:" -ForegroundColor White
Write-Host "   • Click 'New Project'" -ForegroundColor Gray
Write-Host "   • Select 'Deploy from Docker Image'" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Configure Docker Image:" -ForegroundColor White
Write-Host "   • Image URL: ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest" -ForegroundColor Gray
Write-Host "   • Port: 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  Set Environment Variables:" -ForegroundColor White
Write-Host "   • DATABASE_URL=postgresql://user:pass@host:port/db" -ForegroundColor Gray
Write-Host "   • PORT=8000" -ForegroundColor Gray
Write-Host "   • ENVIRONMENT=production" -ForegroundColor Gray
Write-Host ""
Write-Host "5️⃣  Deploy!" -ForegroundColor White
Write-Host "   • Click 'Deploy'" -ForegroundColor Gray
Write-Host "   • Deployment should complete in 30-60 seconds" -ForegroundColor Gray
Write-Host ""
Write-Host "✨ Benefits of this approach:" -ForegroundColor Green
Write-Host "   ✅ All dependencies pre-installed" -ForegroundColor Gray
Write-Host "   ✅ ML models pre-cached" -ForegroundColor Gray
Write-Host "   ✅ Ultra-fast Railway deployments (30s)" -ForegroundColor Gray
Write-Host "   ✅ No build timeouts" -ForegroundColor Gray
Write-Host "   ✅ Consistent production environment" -ForegroundColor Gray
Write-Host ""

if (-not $SkipBuild) {
    Write-Host "⏳ Waiting for GitHub Actions to complete..." -ForegroundColor Yellow
    Write-Host "   Once build is done, follow the Railway setup steps above!" -ForegroundColor White
}
