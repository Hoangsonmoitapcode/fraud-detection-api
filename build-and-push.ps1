# Build and push Docker image to GitHub Container Registry
# PowerShell version for Windows

$IMAGE_NAME = "ghcr.io/hoangsonmoitapcode/fraud-detection-api"
$TAG = "latest"

Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build -t "${IMAGE_NAME}:${TAG}" .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Pushing to GitHub Container Registry..." -ForegroundColor Yellow
docker push "${IMAGE_NAME}:${TAG}"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build and push completed!" -ForegroundColor Green
Write-Host "🚀 Image available at: ${IMAGE_NAME}:${TAG}" -ForegroundColor Cyan
Write-Host ""
Write-Host "To deploy on Railway:" -ForegroundColor White
Write-Host "1. Go to Railway dashboard" -ForegroundColor Gray
Write-Host "2. Create new service from Docker image" -ForegroundColor Gray
Write-Host "3. Use image: ${IMAGE_NAME}:${TAG}" -ForegroundColor Gray
