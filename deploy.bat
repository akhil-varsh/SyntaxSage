@echo off
REM SyntaxSage Docker Deployment Script for Windows
title SyntaxSage Docker Deployment

echo.
echo ==========================================
echo   SyntaxSage Docker Deployment (Windows)
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed
    echo Please install Docker Desktop from https://docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker Compose is not installed
    echo Please install Docker Compose or use Docker Desktop
    pause
    exit /b 1
)

echo Docker and Docker Compose are available
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo Docker is running
echo.

REM Pull Gemma3 model
echo Pulling Gemma3 model (this may take a while)...
docker pull ai/gemma3:4B-Q4_K_M

if errorlevel 1 (
    echo Failed to pull Gemma3 model
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo Gemma3 model pulled successfully
echo.

REM Build and start services
echo Building and starting SyntaxSage services...
docker-compose up --build -d

if errorlevel 1 (
    echo Failed to start services
    echo Check the logs with: docker-compose logs
    pause
    exit /b 1
)

echo Services started successfully!
echo.

REM Wait for services
echo Waiting for services to be ready...
timeout /t 15 /nobreak >nul

echo.
echo SyntaxSage is now running!
echo.
echo Access points:
echo   * Streamlit App: http://localhost:8501
echo   * Gemma3 API:   http://localhost:8080
echo   * Nginx Proxy:  http://localhost:80
echo.
echo Management commands:
echo   * View logs:     docker-compose logs -f
echo   * Stop services: docker-compose down
echo   * Restart:       docker-compose restart
echo.
echo Opening SyntaxSage in your default browser...
start http://localhost:8501

echo.
echo Press any key to exit...
pause >nul