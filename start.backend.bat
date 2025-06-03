@echo off
REM =============================================
REM Authentication System - Backend Startup Script
REM This script starts the backend services using Docker
REM =============================================

echo Starting Backend Services...
echo.

REM =============================================
REM Check Docker Status
REM =============================================
echo Checking Docker status...
docker info > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running.

REM =============================================
REM Start Docker Services
REM =============================================
echo.
echo [INFO] Building and starting containers...
echo [INFO] Stopping any running containers...
docker-compose down

echo [INFO] Building containers...
docker-compose build

echo [INFO] Starting containers in detached mode...
docker-compose up -d

REM =============================================
REM Display Success Message
REM =============================================
echo.
echo [SUCCESS] Backend services are now running!
echo [INFO] API Documentation: http://localhost:8000/docs
echo [INFO] API Base URL: http://localhost:8000
echo.

pause 