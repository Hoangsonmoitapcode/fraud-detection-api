# PowerShell script to setup Railway CLI for Windows
# Run this script to install Railway CLI and configure authentication

Write-Host "🚀 Setting up Railway CLI for Fraud Detection API" -ForegroundColor Green
Write-Host ""

# Check if Railway CLI is installed
try {
    $railwayVersion = railway --version 2>$null
    Write-Host "✅ Railway CLI is already installed: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "📥 Installing Railway CLI..." -ForegroundColor Yellow
    
    # Download and install Railway CLI for Windows
    $railwayUrl = "https://github.com/railwayapp/cli/releases/latest/download/railway-windows-amd64.exe"
    $railwayPath = "$env:TEMP\railway.exe"
    
    try {
        Invoke-WebRequest -Uri $railwayUrl -OutFile $railwayPath
        Copy-Item $railwayPath "$env:ProgramFiles\Railway\railway.exe" -Force
        Remove-Item $railwayPath -Force
        
        # Add to PATH
        $env:PATH += ";$env:ProgramFiles\Railway"
        [Environment]::SetEnvironmentVariable("PATH", $env:PATH, [EnvironmentVariableTarget]::User)
        
        Write-Host "✅ Railway CLI installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install Railway CLI: $_" -ForegroundColor Red
        Write-Host "Please install manually from: https://docs.railway.app/cli/install" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "🔐 Authentication setup:" -ForegroundColor Cyan
Write-Host "1. Go to https://railway.app/account/tokens" -ForegroundColor White
Write-Host "2. Create a new token" -ForegroundColor White
Write-Host "3. Copy the token" -ForegroundColor White
Write-Host "4. Run: railway auth" -ForegroundColor White
Write-Host ""

# Prompt for token
$token = Read-Host "Enter your Railway token (or press Enter to skip)"
if ($token -and $token.Trim() -ne "") {
    try {
        railway auth $token
        Write-Host "✅ Authentication successful!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Authentication failed. Please run 'railway auth' manually." -ForegroundColor Red
    }
} else {
    Write-Host "⏭️ Skipping authentication. Please run 'railway auth' manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Cyan
Write-Host "1. Ensure HF_TOKEN is set in Railway dashboard" -ForegroundColor White
Write-Host "2. Connect your GitHub repository to Railway" -ForegroundColor White
Write-HOST "3. Deploy using: railway up" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
