@echo off
echo ========================================
echo Opening Fake News Detector Website
echo ========================================
echo.

REM Change to script directory
cd /d %~dp0

REM Check if backend is running
echo Checking if backend server is running...
curl -s http://localhost:5001 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backend server is running
) else (
    echo [WARNING] Backend server is not running!
    echo.
    echo Please start the backend server first:
    echo   1. Open a new terminal
    echo   2. cd D:\Fake-news-detector\Backend
    echo   3. python app.py
    echo.
    pause
)

echo.
echo Opening website in your default browser...
echo.

REM Open the HTML file in default browser
start "" "index.html"

echo.
echo ========================================
echo Website should open in your browser now!
echo ========================================
echo.
echo If you see CORS errors, use a local web server instead:
echo   python -m http.server 8000
echo   Then open: http://localhost:8000
echo.
timeout /t 3 >nul

