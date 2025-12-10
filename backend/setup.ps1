# NutriScan Backend Quick Setup Script for PowerShell
# Run with: .\setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NutriScan Backend Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Navigate to backend directory
Write-Host "[1/5] Navigating to backend directory..." -ForegroundColor Yellow
if (-not (Test-Path "backend")) {
    Write-Host "[✗] ERROR: Could not find backend directory" -ForegroundColor Red
    exit 1
}
Set-Location backend

# Create virtual environment
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[✗] ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "[✓] Virtual environment created" -ForegroundColor Green
}
else {
    Write-Host "[✓] Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "[✓] Dependencies installed" -ForegroundColor Green

# Run database migrations
Write-Host "[4/5] Running database migrations..." -ForegroundColor Yellow
python manage.py migrate --noinput 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[⚠] WARNING: Migrations may need manual setup" -ForegroundColor Yellow
}
else {
    Write-Host "[✓] Database initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✓ Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Create a superuser (admin account):" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver 0.0.0.0:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "Then open your frontend in another terminal:" -ForegroundColor White
Write-Host "   - Open index.html in VS Code with Live Server" -ForegroundColor Gray
Write-Host "   - Or visit: http://localhost:5500/" -ForegroundColor Gray
Write-Host ""
Write-Host "Backend will be available at:" -ForegroundColor White
Write-Host "   http://localhost:8000/api/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Admin panel:" -ForegroundColor White
Write-Host "   http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host ""
Write-Host "For more information, see:" -ForegroundColor White
Write-Host "   - backend/README.md" -ForegroundColor Gray
Write-Host "   - SETUP.md" -ForegroundColor Gray
Write-Host "   - INTEGRATION_SUMMARY.md" -ForegroundColor Gray
Write-Host ""
