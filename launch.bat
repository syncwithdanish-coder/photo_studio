@echo off
cd /d "%~dp0"
title Product Studio — Keep open during generation

if exist ".python_embed\python.exe" (
    .python_embed\python.exe main.py
    echo. & echo Product Studio closed. & pause
    exit /b 0
)

echo [ERROR] Run SETUP.bat first.
pause
