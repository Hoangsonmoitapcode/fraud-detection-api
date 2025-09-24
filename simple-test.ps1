# Simple Docker build test
Write-Host "Testing Docker build..." -ForegroundColor Yellow

# Check if Docker is available
try {
    docker version | Out-Null
    Write-Host "Docker is available" -ForegroundColor Green
} catch {
    Write-Host "Docker not found. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Simple build test
Write-Host "Building test image..." -ForegroundColor Cyan
docker build -t fraud-detection-test .

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful!" -ForegroundColor Green
    
    # Show image info
    docker images fraud-detection-test --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
    
    Write-Host ""
    Write-Host "To test locally:" -ForegroundColor White
    Write-Host "docker run -p 8000:8000 fraud-detection-test" -ForegroundColor Gray
    
} else {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}
