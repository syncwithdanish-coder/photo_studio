@echo off
REM ═══════════════════════════════════════════════════════════════════════
REM  Product Studio — NUCLEAR CLEAN FIX
REM  The existing .venv was made with Anaconda Python — must rebuild it
REM  using plain Python (py launcher or python3) instead.
REM ═══════════════════════════════════════════════════════════════════════

echo.
echo  ================================================================
echo     PRODUCT STUDIO — CLEAN ENVIRONMENT SETUP
echo  ================================================================
echo.

if not exist "main.py" (
    echo [ERROR] Run this from inside the product_studio folder.
    echo   e.g.  cd H:\generator_image\product_studio
    pause & exit /b 1
)

REM ── Step 1: Find a non-Anaconda Python ────────────────────────────
echo [1] Finding a clean Python installation (not Anaconda)...
echo.

set CLEAN_PY=

REM Try py launcher first — picks plain Python installs
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('py -3.12 -c "import sys; print(sys.executable)"') do set CLEAN_PY=%%i
    echo     Found via py launcher (3.12): !CLEAN_PY!
    goto :found_python
)

py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('py -3.11 -c "import sys; print(sys.executable)"') do set CLEAN_PY=%%i
    echo     Found via py launcher (3.11): !CLEAN_PY!
    goto :found_python
)

py -3.10 --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('py -3.10 -c "import sys; print(sys.executable)"') do set CLEAN_PY=%%i
    echo     Found via py launcher (3.10): !CLEAN_PY!
    goto :found_python
)

REM Fallback: look for Python in common install paths (NOT anaconda)
for %%D in (
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
) do (
    if exist %%D (
        REM Check it is not Anaconda
        %%D -c "import sys; exit(0 if 'anaconda' not in sys.executable.lower() and 'conda' not in sys.executable.lower() else 1)" >nul 2>&1
        if not errorlevel 1 (
            set CLEAN_PY=%%D
            echo     Found clean Python: %%D
            goto :found_python
        )
    )
)

REM Nothing found
echo.
echo  ================================================================
echo   [ERROR] No clean Python installation found.
echo.
echo   You need to install plain Python from:
echo     https://python.org/downloads
echo.
echo   During installation:
echo     - Tick "Add Python to PATH"
echo     - Do NOT use the Anaconda Prompt
echo.
echo   After installing, run this script again.
echo  ================================================================
pause & exit /b 1

:found_python
echo.
REM Verify it is really not Anaconda
"%CLEAN_PY%" -c "
import sys
exe = sys.executable.lower()
if 'anaconda' in exe or 'conda' in exe:
    print('[FAIL] This Python is still Anaconda:', sys.executable)
    sys.exit(1)
print('[OK] Clean Python confirmed:', sys.executable)
print(f'     Version: {sys.version}')
"
if errorlevel 1 (
    echo [ERROR] Could not find a clean Python. See instructions above.
    pause & exit /b 1
)

REM ── Step 2: Nuke the tainted .venv ────────────────────────────────
echo.
echo [2] Removing old Anaconda-tainted .venv...
if exist ".venv" (
    rmdir /s /q .venv
    echo     Old .venv deleted.
) else (
    echo     No old .venv found.
)

REM ── Step 3: Create fresh venv with clean Python ───────────────────
echo.
echo [3] Creating fresh .venv with clean Python...
"%CLEAN_PY%" -m venv .venv
if errorlevel 1 (
    echo [ERROR] Failed to create venv.
    pause & exit /b 1
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate new venv.
    pause & exit /b 1
)

echo.
echo     Active Python (must NOT be Anaconda):
where python
python -c "import sys; print('    exe:', sys.executable)"
echo.

REM ── Step 4: Upgrade pip ───────────────────────────────────────────
echo [4] Upgrading pip...
python -m pip install --upgrade pip -q

REM ── Step 5: Pin numpy < 2 ─────────────────────────────────────────
echo [5] Pinning numpy ^<2.0 (prevents scipy binary conflicts)...
pip install "numpy>=1.24.0,<2.0.0" -q

REM ── Step 6: PyQt6 ─────────────────────────────────────────────────
echo [6] Installing PyQt6...
pip install "PyQt6==6.6.1" "PyQt6-Qt6==6.6.1" "PyQt6-sip>=13.6.0" -q

REM ── Step 7: AI stack ──────────────────────────────────────────────
echo [7] Installing AI stack (diffusers, transformers, etc.)...
pip install ^
    "diffusers>=0.30.0" ^
    "transformers>=4.44.0" ^
    "accelerate>=0.33.0" ^
    "safetensors>=0.4.4" ^
    "huggingface_hub>=0.24.0" ^
    "Pillow>=10.0.0" ^
    -q
if errorlevel 1 (
    echo [ERROR] AI stack install failed.
    pause & exit /b 1
)

REM ── Step 8: Auto-detect GPU and install PyTorch ───────────────────
echo [8] Detecting GPU and installing PyTorch...
nvidia-smi >nul 2>&1
if not errorlevel 1 (
    echo     NVIDIA GPU detected — installing CUDA 12.1 build...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 -q
    if errorlevel 1 (
        echo     CUDA 12.1 failed — trying CUDA 11.8...
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 -q
    )
) else (
    echo     No GPU detected — installing CPU build...
    pip install torch torchvision -q
)
if errorlevel 1 (
    echo [ERROR] PyTorch install failed.
    pause & exit /b 1
)

REM ── Step 9: Full verification ─────────────────────────────────────
echo.
echo  ================================================================
echo   VERIFICATION
echo  ================================================================
python -c "
import sys, os

def chk(label, code, fatal=True):
    try:
        result = {}
        exec(code, result)
        note = result.get('note', '')
        print(f'  [OK]  {label}  {note}')
        return True
    except Exception as e:
        tag = 'FAIL' if fatal else 'WARN'
        print(f'  [{tag}] {label}: {e}')
        return not fatal

ok = True

# Confirm not anaconda
exe = sys.executable.lower()
if 'anaconda' in exe or 'conda' in exe:
    print(f'  [FAIL] Still using Anaconda Python: {sys.executable}')
    ok = False
else:
    print(f'  [OK]  Python executable: {sys.executable}')

ok &= chk('numpy  < 2.0',
    'import numpy as np; v=np.__version__; assert v < \"2\", f\"numpy {v} >= 2!\"; note=v')
ok &= chk('torch',
    'import torch; note=f\"{torch.__version__} | CUDA:{torch.cuda.is_available()}\"')
ok &= chk('torchvision',     'import torchvision; note=torchvision.__version__')
ok &= chk('transformers',    'import transformers; note=transformers.__version__')
ok &= chk('diffusers',       'import diffusers; note=diffusers.__version__')
ok &= chk('accelerate',      'import accelerate; note=accelerate.__version__')
ok &= chk('PIL',             'from PIL import Image; import PIL; note=PIL.__version__')
ok &= chk('PyQt6',           'from PyQt6.QtWidgets import QApplication')
ok &= chk('SDXL pipeline',   'from diffusers import StableDiffusionXLPipeline')
chk('FLUX pipeline',         'from diffusers import FluxPipeline', fatal=False)

print()
if ok:
    print('  ALL CHECKS PASSED — ready!')
else:
    print('  Some checks failed. Review above.')
    import sys; sys.exit(1)
"
if errorlevel 1 (
    echo.
    echo [ERROR] Verification failed. Review the output above.
    pause & exit /b 1
)

echo.
echo  ================================================================
echo   Launching Product Studio...
echo  ================================================================
echo.
python main.py
pause
