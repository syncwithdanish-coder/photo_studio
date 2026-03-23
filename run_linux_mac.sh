#!/bin/bash
# Product Studio — Linux/macOS Setup & Run Script

echo ""
echo " ╔══════════════════════════════════════╗"
echo " ║     PRODUCT STUDIO — SETUP           ║"
echo " ╚══════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found. Install Python 3.10+ first."
    exit 1
fi

# Create venv
if [ ! -d ".venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "[2/3] Installing dependencies..."
pip install --upgrade pip --quiet
pip install PyQt6 diffusers transformers accelerate safetensors Pillow huggingface_hub --quiet

echo ""
echo "[3/3] Installing PyTorch..."
echo ""
echo " Choose your setup:"
echo " [1] NVIDIA GPU (CUDA 12.1)"
echo " [2] CPU only"
echo " [3] macOS (MPS / Apple Silicon)"
echo " [4] Skip (already installed)"
echo ""
read -p "Enter 1-4: " choice

case $choice in
    1) pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 ;;
    2) pip install torch torchvision ;;
    3) pip install torch torchvision ;;
    4) echo "Skipping." ;;
esac

echo ""
echo " ✓ Setup complete. Launching Product Studio..."
echo ""
python3 main.py
