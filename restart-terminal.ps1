# Simple script to help with PowerShell terminal issues
# Run this if you're experiencing terminal connectivity problems

Write-Host "🔄 PowerShell Terminal Troubleshooting" -ForegroundColor Cyan
Write-Host ""

# Check PowerShell version
Write-Host "📋 PowerShell Version:" -ForegroundColor Yellow
$PSVersionTable.PSVersion
Write-Host ""

# Check execution policy
Write-Host "🔒 Execution Policy:" -ForegroundColor Yellow
Get-ExecutionPolicy
Write-Host ""

# Basic connectivity test
Write-Host "🧪 Testing basic commands:" -ForegroundColor Yellow
try {
    Get-Location
    Write-Host "✅ Get-Location works" -ForegroundColor Green
} catch {
    Write-Host "❌ Get-Location failed: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    Get-ChildItem | Select-Object -First 3 | Format-Table Name, Length
    Write-Host "✅ File listing works" -ForegroundColor Green
} catch {
    Write-Host "❌ File listing failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Check if Docker is available
Write-Host "🐳 Docker availability:" -ForegroundColor Yellow
try {
    docker --version
    Write-Host "✅ Docker is available" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Docker not found or not running" -ForegroundColor Yellow
}

# Check if Git is available
Write-Host "📂 Git availability:" -ForegroundColor Yellow
try {
    git --version
    Write-Host "✅ Git is available" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Git not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 If you're still having issues:" -ForegroundColor Cyan
Write-Host "1. Restart VS Code" -ForegroundColor Gray
Write-Host "2. Try Windows Terminal instead of VS Code terminal" -ForegroundColor Gray  
Write-Host "3. Run PowerShell as Administrator" -ForegroundColor Gray
Write-Host "4. Check Windows Updates" -ForegroundColor Gray
