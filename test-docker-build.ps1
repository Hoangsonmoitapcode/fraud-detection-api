# Test Docker build locally before pushing
# This helps identify issues early

param(
    [switch]$SkipCache,
    [switch]$Verbose
)

$IMAGE_NAME = "fraud-detection-api"
$TAG = "test"

Write-Host "Testing Docker build locally..." -ForegroundColor Yellow

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "Docker is running" -ForegroundColor Green
} catch {
    Write-Host "Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Build arguments
$BuildArgs = @("build", "-t", "${IMAGE_NAME}:${TAG}")

if ($SkipCache) {
    $BuildArgs += "--no-cache"
    Write-Host "🚫 Cache disabled" -ForegroundColor Yellow
}

if ($Verbose) {
    $BuildArgs += "--progress=plain"
}

$BuildArgs += "."

Write-Host "🔨 Building image: ${IMAGE_NAME}:${TAG}" -ForegroundColor Cyan
Write-Host "Command: docker $($BuildArgs -join ' ')" -ForegroundColor Gray

# Start build with timing
$StartTime = Get-Date
docker @BuildArgs

if ($LASTEXITCODE -eq 0) {
    $Duration = (Get-Date) - $StartTime
    Write-Host "✅ Build successful in $($Duration.TotalMinutes.ToString('F1')) minutes" -ForegroundColor Green
    
    # Show image size
    $ImageSize = docker images "${IMAGE_NAME}:${TAG}" --format "table {{.Size}}" | Select-Object -Skip 1
    Write-Host "📦 Image size: $ImageSize" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "🧪 To test the image locally:" -ForegroundColor White
    Write-Host "docker run -p 8000:8000 --env DATABASE_URL=sqlite:///./test.db ${IMAGE_NAME}:${TAG}" -ForegroundColor Gray
    
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Yellow
    Write-Host "- Check Dockerfile syntax" -ForegroundColor Gray
    Write-Host "- Ensure all files exist" -ForegroundColor Gray
    Write-Host "- Check requirements.txt" -ForegroundColor Gray
    Write-Host "- Run with -Verbose for detailed logs" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "🚀 Ready to push to production!" -ForegroundColor Green
