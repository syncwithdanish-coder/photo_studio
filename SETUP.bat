@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title Product Studio — Setup

echo.
echo  ================================================================
echo     PRODUCT STUDIO v2  —  SETUP
echo  ================================================================
echo.

if not exist "main.py" (
    echo [ERROR] Run from inside the product_studio folder.
    echo   e.g.  cd H:\generator_image\product_studio
    pause & exit /b 1
)

set "PYDIR=%~dp0.python_embed"
set "PYEXE=%PYDIR%\python.exe"

REM ── Already complete? ─────────────────────────────────────────────
if exist "%PYEXE%" (
    "%PYEXE%" -c "import torch,diffusers,transformers,PyQt6" >nul 2>&1
    if not errorlevel 1 (
        echo All packages already installed.
        goto :launch
    )
    echo Packages incomplete — reinstalling...
    goto :packages
)

REM ── Download embeddable Python 3.11 ──────────────────────────────
echo [1/5] Downloading Python 3.11 embeddable...
if not exist "%PYDIR%" mkdir "%PYDIR%"

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile '%~dp0py.zip' -UseBasicParsing}"
if not exist "%~dp0py.zip" (
    echo [ERROR] Download failed — check internet connection.
    pause & exit /b 1
)
powershell -Command "Expand-Archive -Path '%~dp0py.zip' -DestinationPath '%PYDIR%' -Force"
del "%~dp0py.zip" >nul 2>&1
if not exist "%PYEXE%" ( echo [ERROR] Extraction failed. & pause & exit /b 1 )

REM Enable site-packages in embedded Python
for %%F in ("%PYDIR%\python3*._pth") do (
    powershell -Command "(Get-Content '%%F') -replace '#import site','import site' | Set-Content '%%F'"
)
if not exist "%PYDIR%\Lib\site-packages" mkdir "%PYDIR%\Lib\site-packages"

REM Install pip
echo [2/5] Installing pip...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%~dp0get-pip.py' -UseBasicParsing}"
"%PYEXE%" "%~dp0get-pip.py" --no-warn-script-location -q
del "%~dp0get-pip.py" >nul 2>&1

:packages
echo [3/5] Installing core packages...
"%PYEXE%" -m pip install --no-warn-script-location -q "numpy>=1.24,<2.0"
"%PYEXE%" -m pip install --no-warn-script-location -q "PyQt6==6.6.1" "PyQt6-Qt6==6.6.1" "PyQt6-sip>=13.6.0"
"%PYEXE%" -m pip install --no-warn-script-location -q "diffusers>=0.30.0" "transformers>=4.44.0" "accelerate>=0.33.0" "safetensors>=0.4.4" "huggingface_hub>=0.24.0" "Pillow>=10.0.0"
if errorlevel 1 ( echo [ERROR] Core package install failed. & pause & exit /b 1 )

echo [4/5] Installing PyTorch (auto-detecting GPU)...
nvidia-smi >nul 2>&1
if not errorlevel 1 (
    echo       NVIDIA GPU detected — CUDA 12.1
    "%PYEXE%" -m pip install --no-warn-script-location torch torchvision --index-url https://download.pytorch.org/whl/cu121 -q
    if errorlevel 1 (
        echo       Trying CUDA 11.8...
        "%PYEXE%" -m pip install --no-warn-script-location torch torchvision --index-url https://download.pytorch.org/whl/cu118 -q
    )
) else (
    echo       No GPU — CPU build
    "%PYEXE%" -m pip install --no-warn-script-location torch torchvision -q
)

echo [5/5] Verifying...
"%PYEXE%" -c "
ok=True
def chk(lbl,code,fatal=True):
    global ok
    try: exec(code); print(f'  [OK] {lbl}')
    except Exception as e:
        t='FAIL' if fatal else 'warn'
        print(f'  [{t}] {lbl}: {e}')
        if fatal: ok=False
chk('numpy',     'import numpy as np; assert np.__version__ < \"2\", np.__version__')
chk('torch',     'import torch; print(f\"       {torch.__version__} CUDA:{torch.cuda.is_available()}\")')
chk('transforms','import transformers; print(f\"       {transformers.__version__}\")')
chk('diffusers', 'import diffusers; print(f\"       {diffusers.__version__}\")')
chk('PIL',       'from PIL import Image')
chk('PyQt6',     'from PyQt6.QtWidgets import QApplication')
chk('SDXL',      'from diffusers import StableDiffusionXLPipeline')
chk('FLUX',      'from diffusers import FluxPipeline', fatal=False)
print(); print('READY' if ok else 'ERRORS — review above')
import sys; sys.exit(0 if ok else 1)
"
if errorlevel 1 ( echo Verification had errors. & pause & exit /b 1 )

:launch
echo.
echo  ================================================================
echo   Launching Product Studio...
echo   (Keep this window open while generating images)
echo  ================================================================
echo.
"%PYEXE%" main.py
echo.
echo Product Studio closed.
pause
