@echo off
REM LoaniFi Startup Script for Windows

echo 🚀 LoaniFi - AI-Powered Loan Chatbot
echo ====================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ⚠️  No .env file found. Creating from template...
    copy .env.example .env >nul
    echo ✅ .env file created
    echo.
    echo ⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY
    echo    You can get an API key from: https://platform.openai.com/api-keys
    echo.
    pause
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Check if services are already running
docker-compose ps | findstr "Up" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Services are already running
    set /p restart="Do you want to restart them? (y/n) "
    if /i "%restart%"=="y" (
        echo 🔄 Stopping existing services...
        docker-compose down
    ) else (
        echo ✅ Keeping existing services running
        echo.
        goto :show_urls
    )
)

REM Start services
echo 🏗️  Building and starting services...
echo    (This may take a few minutes on first run)
echo.
docker-compose up -d --build

REM Wait for services to be ready
echo.
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check health
echo.
echo 🔍 Checking service health...

curl -s http://localhost:8000/health >nul 2>&1
if not errorlevel 1 (
    echo ✅ Backend is healthy
) else (
    echo ⚠️  Backend is starting... (may take a moment)
)

curl -s http://localhost:3000 >nul 2>&1
if not errorlevel 1 (
    echo ✅ Frontend is healthy
) else (
    echo ⚠️  Frontend is starting... (may take a moment)
)

:show_urls
echo.
echo ═══════════════════════════════════════
echo ✅ LoaniFi is now running!
echo ═══════════════════════════════════════
echo.
echo 📍 Access the application:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Admin Dashboard: http://localhost:3000/admin
echo.
echo 📊 View logs:
echo    docker-compose logs -f
echo.
echo 🛑 Stop services:
echo    docker-compose down
echo.
echo 🎬 Ready for demo! Check DEMO_GUIDE.md for demo instructions.
echo.
pause


