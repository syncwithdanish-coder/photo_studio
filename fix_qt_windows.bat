@echo off
REM ── QUICK FIX for "DLL load failed while importing QtWidgets" on Windows ──
echo.
echo  Fixing PyQt6 DLL issue...
echo.

call .venv\Scripts\activate.bat 2>nul || (
    echo [ERROR] No .venv found. Run run_windows.bat first.
    pause & exit /b 1
)

echo Removing existing PyQt6 installations...
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip PyQt6-QScintilla pyqt6-tools -y

echo.
echo Installing pinned stable version...
pip install "PyQt6==6.6.1" "PyQt6-Qt6==6.6.1" "PyQt6-sip>=13.6.0"

echo.
echo Testing...
python -c "from PyQt6.QtWidgets import QApplication; print('[OK] Fixed! PyQt6 works now.')"
if errorlevel 1 (
    echo.
    echo Still failing. Trying alternative fix via opengl...
    pip install pyopengl
    python -c "from PyQt6.QtWidgets import QApplication; print('[OK] Fixed with opengl')"
)

echo.
echo Launching app...
python main.py
pause
