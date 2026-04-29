@echo off
REM AI Personalized Learning Platform - Setup Script for Windows
REM This script sets up both backend and frontend

echo.
echo ===================================
echo Starting AI Learning Platform Setup
echo ===================================
echo.

REM Step 1: Backend Setup
echo [Step 1] Setting up Backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

echo.
echo [✓] Backend setup complete!
echo.

REM Step 2: Frontend Setup
echo [Step 2] Setting up Frontend...
cd ..\frontend

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local file from .env.example...
    copy .env.example .env.local
)

REM Install dependencies
echo Installing dependencies with npm...
where /q pnpm
if errorlevel 1 (
    echo Using npm...
    call npm install
) else (
    echo Using pnpm...
    call pnpm install
)

echo.
echo [✓] Frontend setup complete!
echo.

REM Step 3: Summary
echo.
echo ==============================
echo Setup Complete!
echo ==============================
echo.
echo Next steps:
echo.
echo 1. Start Backend:
echo    cd backend
echo    python main.py
echo.
echo 2. Start Frontend (in another terminal):
echo    cd frontend
echo    pnpm dev
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
echo API Documentation: http://192.168.0.131:8001/api/docs
echo.
pause
