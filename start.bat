@echo off
REM Launch script for Baiboly application on Windows
REM This script starts the entire application stack using Docker Compose

echo ==================================
echo   Baiboly Application Launcher
echo ==================================
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Docker is not installed.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker compose version >nul 2>nul
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
) else (
    docker-compose --version >nul 2>nul
    if %errorlevel% equ 0 (
        set DOCKER_COMPOSE=docker-compose
    ) else (
        echo Error: Docker Compose is not installed.
        echo Please install Docker Compose from: https://docs.docker.com/compose/install/
        pause
        exit /b 1
    )
)

echo Starting Baiboly application...
echo.

REM Build and start containers
%DOCKER_COMPOSE% up --build -d

if %errorlevel% neq 0 (
    echo Error starting application. Check Docker logs.
    pause
    exit /b 1
)

echo.
echo ✓ Application started successfully!
echo.
echo Services running:
echo   • Frontend:  http://localhost:5173
echo   • Backend:   http://localhost:5000
echo   • Database:  localhost:5432
echo.
echo To view logs:
echo   %DOCKER_COMPOSE% logs -f
echo.
echo To stop the application:
echo   %DOCKER_COMPOSE% down
echo.
echo To start pgAdmin (database management):
echo   %DOCKER_COMPOSE% --profile tools up -d pgadmin
echo   Then open: http://localhost:5050
echo   Login: admin@baiboly.local / admin
echo.

REM Wait for services to be healthy
echo Waiting for services to be ready...
timeout /t 5 /nobreak >nul

REM Check if backend is responding
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend is healthy
) else (
    echo ⚠ Backend is still starting... Check logs: %DOCKER_COMPOSE% logs backend
)

REM Check if frontend is responding
curl -s http://localhost:5173 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is healthy
) else (
    echo ⚠ Frontend is still starting... Check logs: %DOCKER_COMPOSE% logs frontend
)

echo.
echo Ready to develop!
echo.
pause
