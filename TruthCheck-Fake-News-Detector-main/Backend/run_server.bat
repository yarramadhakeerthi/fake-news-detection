@echo off
echo ========================================
echo Starting Fake News Detector Server
echo ========================================
echo.
echo Make sure you're in the Backend directory!
echo.
cd /d %~dp0
python app.py
pause

