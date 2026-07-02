# Fake News Detector - Server Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Fake News Detector Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Yellow
    pause
    exit 1
}

# Check for required files
Write-Host "Checking required files..." -ForegroundColor Yellow
$requiredFiles = @("app.py")
$missing = $false

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (MISSING)" -ForegroundColor Red
        $missing = $true
    }
}

if ($missing) {
    Write-Host "`nERROR: Missing required files!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Starting Flask server on http://localhost:5001" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the Flask app
python app.py

