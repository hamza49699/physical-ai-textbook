#!/usr/bin/env pwsh
# Quick Local Testing Script for Physical AI Textbook (PowerShell)
# Run: .\setup-local.ps1

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Physical AI Textbook - Local Testing Setup" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python not found. Install from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "`n[2/5] Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Node.js not found. Install from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n[3/5] Setting up Python virtual environment..." -ForegroundColor Yellow
if (!(Test-Path "venv")) {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[4/5] Installing backend dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install -q -r backend/requirements.txt
Write-Host "✓ Backend dependencies installed" -ForegroundColor Green

# Install frontend dependencies
Write-Host "`n[5/5] Installing frontend dependencies..." -ForegroundColor Yellow
npm install --silent
Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "✓ LOCAL SETUP COMPLETE!" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Backend:" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. In another terminal, start Frontend:" -ForegroundColor Yellow
Write-Host "   npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test Backend:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/docs (API docs)" -ForegroundColor Gray
Write-Host "   http://localhost:8000/health (health check)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Test Frontend:" -ForegroundColor Yellow
Write-Host "   http://localhost:3000 (Docusaurus)" -ForegroundColor Gray
Write-Host ""
Write-Host "For detailed testing guide, see: LOCAL-TESTING-GUIDE.md" -ForegroundColor Cyan
Write-Host ""
