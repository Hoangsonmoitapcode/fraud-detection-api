# Simple production deployment script
param(
    [string]$Message = "Production deployment with pre-installed dependencies"
)

Write-Host "Starting Production Deployment Process..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Triggering GitHub Actions Build..." -ForegroundColor Yellow

# Commit changes if any
$hasChanges = git status --porcelain
if ($hasChanges) {
    Write-Host "Committing pending changes..." -ForegroundColor White
    git add .
    git commit -m "deploy: $Message"
}

# Create deployment commit
git commit --allow-empty -m "build: $Message"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment commit created successfully" -ForegroundColor Green
    
    Write-Host "Pushing to trigger GitHub Actions..." -ForegroundColor Cyan
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Monitor build progress at:" -ForegroundColor White
        Write-Host "https://github.com/hoangsonmoitapcode/fraud-detection-api/actions" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Build will take 5-8 minutes (heavy but complete image)" -ForegroundColor Yellow
        Write-Host "Image will be available at:" -ForegroundColor White
        Write-Host "ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest" -ForegroundColor Blue
        Write-Host ""
        Write-Host "RAILWAY DEPLOYMENT STEPS:" -ForegroundColor Yellow
        Write-Host "=========================" -ForegroundColor Gray
        Write-Host "1. Go to: https://railway.app/dashboard" -ForegroundColor White
        Write-Host "2. Click 'New Project'" -ForegroundColor White
        Write-Host "3. Select 'Deploy from Docker Image'" -ForegroundColor White
        Write-Host "4. Image URL: ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest" -ForegroundColor White
        Write-Host "5. Set environment variables:" -ForegroundColor White
        Write-Host "   DATABASE_URL=postgresql://user:pass@host:port/db" -ForegroundColor Gray
        Write-Host "   PORT=8000" -ForegroundColor Gray
        Write-Host "   ENVIRONMENT=production" -ForegroundColor Gray
        Write-Host "6. Click Deploy (will take 30-60 seconds)" -ForegroundColor White
        Write-Host ""
        Write-Host "Wait for GitHub Actions to complete, then follow Railway steps above!" -ForegroundColor Green
    } else {
        Write-Host "Push failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Failed to create deployment commit!" -ForegroundColor Red
    exit 1
}
