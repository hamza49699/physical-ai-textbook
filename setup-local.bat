@echo off
REM Quick Local Testing Script for Physical AI Textbook
REM Run this to quickly test the project locally

echo.
echo ============================================
echo Physical AI Textbook - Local Testing Setup
echo ============================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install from https://www.python.org/
    exit /b 1
)
python --version
echo ✓ Python found

REM Check Node.js
echo.
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found. Install from https://nodejs.org/
    exit /b 1
)
node --version
echo ✓ Node.js found

REM Create virtual environment
echo.
echo [3/5] Setting up Python virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
echo.
echo [4/5] Installing backend dependencies...
pip install -q -r backend/requirements.txt
echo ✓ Backend dependencies installed

REM Install frontend dependencies
echo.
echo [5/5] Installing frontend dependencies...
call npm install --silent
echo ✓ Frontend dependencies installed

echo.
echo ============================================
echo ✓ LOCAL SETUP COMPLETE!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Start Backend:
echo    cd backend
echo    python main.py
echo.
echo 2. In another terminal, start Frontend:
echo    npm start
echo.
echo 3. Test Backend:
echo    http://localhost:8000/docs (API docs)
echo    http://localhost:8000/health (health check)
echo.
echo 4. Test Frontend:
echo    http://localhost:3000 (Docusaurus)
echo.
echo For detailed testing guide, see: LOCAL-TESTING-GUIDE.md
echo.
pause
