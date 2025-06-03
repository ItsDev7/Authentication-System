@echo off
REM =============================================
REM Authentication System - UI Startup Script
REM This script starts the frontend application
REM =============================================

echo Starting UI Application...
echo.

REM =============================================
REM Check Python Installation
REM =============================================
echo Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python and try again.
    pause
    exit /b 1
)
echo [OK] Python is installed.

REM =============================================
REM Setup Virtual Environment
REM =============================================
echo.
echo [INFO] Checking virtual environment...
if not exist "venv" (
    echo [INFO] Creating new virtual environment...
    python -m venv venv
    
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate
    
    echo [INFO] Installing requirements...
    pip install -r requirements.txt
) else (
    echo [INFO] Using existing virtual environment...
    call venv\Scripts\activate
)

REM =============================================
REM Start Application
REM =============================================
echo.
echo [INFO] Starting the application...
python main.py

pause 