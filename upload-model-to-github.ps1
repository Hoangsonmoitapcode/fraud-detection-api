# Upload model to GitHub Releases for fast Docker builds
# This allows us to download model during build instead of including in source

param(
    [string]$ModelFile = "phobert_sms_classifier.pkl",
    [string]$Tag = "v1.0",
    [string]$ReleaseName = "AI Model Release v1.0"
)

Write-Host "Uploading AI model to GitHub Releases..." -ForegroundColor Cyan

# Check if model file exists
if (-not (Test-Path $ModelFile)) {
    Write-Host "Error: Model file $ModelFile not found!" -ForegroundColor Red
    exit 1
}

$FileSize = (Get-Item $ModelFile).Length / 1MB
Write-Host "Model file size: $($FileSize.ToString('F1')) MB" -ForegroundColor Yellow

# Check if GitHub CLI is available
try {
    gh --version | Out-Null
} catch {
    Write-Host "GitHub CLI not found. Please install: https://cli.github.com/" -ForegroundColor Red
    Write-Host "Alternative: Upload manually via GitHub web interface" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/hoangsonmoitapcode/fraud-detection-api/releases" -ForegroundColor Blue
    Write-Host "2. Click 'Create a new release'" -ForegroundColor Blue
    Write-Host "3. Tag: $Tag" -ForegroundColor Blue
    Write-Host "4. Upload file: $ModelFile" -ForegroundColor Blue
    exit 1
}

Write-Host "Creating GitHub release..." -ForegroundColor Yellow

# Create release and upload file
try {
    gh release create $Tag $ModelFile --title "$ReleaseName" --notes "AI model for fraud detection API

This release contains the PhoBERT SMS classifier model (518MB).
Used by Docker builds to include AI functionality while keeping build times reasonable.

Download URL will be:
https://github.com/hoangsonmoitapcode/fraud-detection-api/releases/download/$Tag/$ModelFile

Usage in Dockerfile:
RUN wget -O $ModelFile https://github.com/hoangsonmoitapcode/fraud-detection-api/releases/download/$Tag/$ModelFile"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Model uploaded successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔗 Download URL:" -ForegroundColor Cyan
        Write-Host "https://github.com/hoangsonmoitapcode/fraud-detection-api/releases/download/$Tag/$ModelFile" -ForegroundColor Blue
        Write-Host ""
        Write-Host "🐳 Now you can use Dockerfile.ai-optimized for builds with AI model!" -ForegroundColor Green
        Write-Host "   Build time: ~8-12 minutes (download + build)" -ForegroundColor Yellow
        Write-Host "   Result: Full AI functionality in production" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Upload failed!" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Update GitHub Actions to use Dockerfile.ai-optimized" -ForegroundColor White
Write-Host "2. Test build time (should be 8-12 minutes)" -ForegroundColor White
Write-Host "3. Deploy and test AI functionality" -ForegroundColor White
