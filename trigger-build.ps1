# Trigger GitHub Actions build manually
# Use this when you want to rebuild the Docker image

param(
    [string]$Message = "Manual Docker image rebuild"
)

Write-Host "Triggering GitHub Actions build..." -ForegroundColor Yellow

# Create empty commit to trigger build
git commit --allow-empty -m "build: $Message"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Empty commit created successfully" -ForegroundColor Green
    
    Write-Host "Pushing to trigger GitHub Actions..." -ForegroundColor Cyan
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "GitHub Actions build triggered:" -ForegroundColor White
        Write-Host "https://github.com/hoangsonmoitapcode/fraud-detection-api/actions" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Build will take 5-10 minutes..." -ForegroundColor Yellow
        Write-Host "Once complete, image will be available at:" -ForegroundColor White
        Write-Host "ghcr.io/hoangsonmoitapcode/fraud-detection-api:latest" -ForegroundColor Blue
    } else {
        Write-Host "Push failed!" -ForegroundColor Red
    }
} else {
    Write-Host "Failed to create commit!" -ForegroundColor Red
}
