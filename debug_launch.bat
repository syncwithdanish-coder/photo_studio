@echo off
REM Product Studio — DEBUG LAUNCH
REM Use this if the app crashes silently — keeps CMD open and shows all errors.

cd /d "%~dp0"
title Product Studio DEBUG

echo.
echo  ================================================
echo     PRODUCT STUDIO — DEBUG MODE
echo     Errors will be visible in this window.
echo  ================================================
echo.

if exist ".python_embed\python.exe" (
    echo Using: .python_embed\python.exe
    .python_embed\python.exe main.py
    echo.
    echo === App exited ===
    pause
    exit /b 0
)

if exist ".venv\Scripts\python.exe" (
    echo Using: .venv\Scripts\python.exe
    .venv\Scripts\python.exe main.py
    echo.
    echo === App exited ===
    pause
    exit /b 0
)

echo [ERROR] No Python environment found. Run SETUP.bat first.
pause
