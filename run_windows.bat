@echo off
setlocal EnableDelayedExpansion
REM Product Studio — Windows Setup & Run
REM Auto-detects clean Python, avoids Anaconda.

echo.
echo  ============================================
echo     PRODUCT STUDIO
echo  ============================================
echo.

if not exist "main.py" (
    echo [ERROR] Run from inside the product_studio folder.
    pause & exit /b 1
)

REM ── If .venv exists and is Anaconda-tainted, show warning ─────────
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -c "import sys; exit(1 if 'anaconda' in sys.executable.lower() or 'conda' in sys.executable.lower() else 0)" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Existing .venv uses Anaconda Python.
        echo           Run fix_dependencies_windows.bat to rebuild it properly.
        echo           Attempting to continue anyway...
        echo.
    )
)

REM ── Check if already fully set up ─────────────────────────────────
if exist ".venv\Scripts\python.exe" (
    call .venv\Scripts\activate.bat
    python -c "import torch, diffusers, transformers, PyQt6" >nul 2>&1
    if not errorlevel 1 (
        echo All dependencies found. Launching...
        python main.py
        pause & exit /b 0
    )
    echo Some dependencies missing — running setup...
)

REM ── Find clean Python ──────────────────────────────────────────────
set CLEAN_PY=
for %%V in (3.12 3.11 3.10) do (
    if not defined CLEAN_PY (
        py -%%V --version >nul 2>&1
        if not errorlevel 1 (
            for /f %%i in ('py -%%V -c "import sys; print(sys.executable)"') do (
                echo %%i | findstr /i "anaconda conda miniconda" >nul 2>&1
                if errorlevel 1 set CLEAN_PY=%%i
            )
        )
    )
)

if not defined CLEAN_PY (
    REM Fallback: check common paths
    for %%D in (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
    ) do (
        if not defined CLEAN_PY (
            if exist %%D (
                %%D -c "import sys; exit(1 if 'conda' in sys.executable.lower() else 0)" >nul 2>&1
                if not errorlevel 1 set CLEAN_PY=%%D
            )
        )
    )
)

if not defined CLEAN_PY (
    echo [ERROR] No clean Python found (only Anaconda detected).
    echo         Install plain Python 3.11 from https://python.org
    echo         Then run this script again.
    pause & exit /b 1
)

echo Using Python: %CLEAN_PY%

REM ── Rebuild venv if it's tainted ──────────────────────────────────
if exist ".venv" (
    .venv\Scripts\python.exe -c "import sys; exit(1 if 'anaconda' in sys.executable.lower() or 'conda' in sys.executable.lower() else 0)" >nul 2>&1
    if errorlevel 1 (
        echo Removing Anaconda-tainted .venv...
        rmdir /s /q .venv
    )
)

if not exist ".venv" (
    echo Creating clean virtual environment...
    "%CLEAN_PY%" -m venv .venv
    if errorlevel 1 ( echo [ERROR] venv creation failed & pause & exit /b 1 )
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip -q
pip install "numpy>=1.24.0,<2.0.0" -q
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y >nul 2>&1
pip install "PyQt6==6.6.1" "PyQt6-Qt6==6.6.1" "PyQt6-sip>=13.6.0" -q
pip install "diffusers>=0.30.0" "transformers>=4.44.0" "accelerate>=0.33.0" "safetensors>=0.4.4" "huggingface_hub>=0.24.0" "Pillow>=10.0.0" -q

python -c "import torch" >nul 2>&1
if errorlevel 1 (
    nvidia-smi >nul 2>&1
    if not errorlevel 1 (
        echo Installing PyTorch with CUDA 12.1...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 -q
    ) else (
        echo Installing PyTorch CPU...
        pip install torch torchvision -q
    )
)

echo.
echo Launching Product Studio...
python main.py
pause
