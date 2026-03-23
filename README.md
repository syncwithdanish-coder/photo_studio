# Product Studio
### Offline AI Product Image Generator
**Powered by FLUX.1 & Stable Diffusion XL · No paid APIs · Fully local**

---

## What it does

Upload 1–5 reference photos of any product → choose an environment theme → generate 3–4 studio-quality product images + a collage. Everything runs on your own machine. No internet required after the initial model download. No watermarks. No paid services.

---

## Features

- **7 environment themes**: Dining Elegance, Kitchen Professional, Living Room, Outdoor Alfresco, Spa & Wellness, Minimalist Studio, Boutique Café
- **3–4 shots per theme**: Hero, Lifestyle, Macro, Flat-lay, and more — each with a unique angle, lighting, and camera spec
- **Auto collage**: Combines your generated shots into one composite image
- **4 model choices**:
  - `FLUX.1-schnell` — 4 steps, ~30 seconds/image, free, no token needed ✓
  - `FLUX.1-dev` — 28 steps, best quality, needs HuggingFace token
  - `SDXL` — 40 steps, universal compatibility
  - `SDXL-Turbo` — 4 steps, very fast preview
- **Full VRAM controls**: FP16, CPU offload, sequential offload — works on GPUs from 4 GB+
- **No watermarks**: Hard-coded in every prompt and negative prompt
- **Save anywhere**: One-click export to any folder

---

## Installation

### Requirements
- Python 3.10 or later
- 8 GB RAM minimum (16 GB recommended)
- GPU: NVIDIA with 6 GB+ VRAM (optional but strongly recommended)

### Windows
```
Double-click run_windows.bat
```
Follow the prompts. It will create a virtual environment, install everything, and launch the app.

### Linux / macOS
```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```

### Manual install
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install PyQt6 diffusers transformers accelerate safetensors Pillow huggingface_hub

# NVIDIA GPU:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# CPU only:
pip install torch torchvision

python main.py
```

---

## First Run — Model Download

The first time you select a model, it downloads from HuggingFace (~6–13 GB depending on model). This only happens once — models are cached to `~/ProductStudio/models/`.

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| FLUX.1-schnell | ~6 GB | ~30s/img | Good |
| FLUX.1-dev | ~24 GB | ~2min/img | Excellent |
| SDXL | ~7 GB | ~60s/img | Good |
| SDXL-Turbo | ~7 GB | ~15s/img | Fair |

**Recommended for most users**: Start with `FLUX.1-schnell`.

### For FLUX.1-dev
1. Create a free account at [huggingface.co](https://huggingface.co)
2. Accept the FLUX.1-dev license at [huggingface.co/black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)
3. Get a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
4. Paste it into the "HuggingFace Token" field in the Configure step

---

## Workflow

```
1. Upload (1–5 product images + description)
        ↓
2. Select Theme (7 environments available)
   + check/uncheck individual shots
        ↓
3. Configure (model, steps, resolution, VRAM options)
        ↓
4. Generate (live thumbnails appear as each image finishes)
        ↓
5. Results (preview, save individual or all, open output folder)
```

---

## Output

All outputs are saved to `~/ProductStudio/outputs/` by default.  
You can also choose a custom folder at the Results step.

---

## Tips

- **Better results**: Give a detailed product description (e.g. `matte black ceramic non-stick frying pan, 28cm, wooden handle`)
- **Low VRAM**: Enable "Sequential CPU offload" in Configure — slower but works on 4 GB GPUs
- **CPU-only**: Works but expect 5–15 minutes per image
- **Batch**: Run the same product through multiple themes for a full catalog

---

## Project Structure

```
product_studio/
├── main.py                   ← Entry point
├── requirements.txt
├── run_windows.bat
├── run_linux_mac.sh
├── ui/
│   ├── main_window.py        ← App window + navigation
│   ├── style.qss             ← Dark luxury stylesheet
│   └── pages/
│       ├── upload_page.py    ← Stage 1: upload images
│       ├── theme_page.py     ← Stage 2: theme + shot selection
│       ├── config_page.py    ← Stage 3: model configuration
│       ├── generate_page.py  ← Stage 4: generation + live preview
│       └── results_page.py   ← Stage 5: gallery + export
├── backend/
│   └── generator.py          ← Diffusers pipeline workers
└── prompts/
    └── theme_prompts.py      ← All 7 themes × 28 shots + collages
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'diffusers'`**  
→ Run the install script again or: `pip install diffusers transformers accelerate`

**`CUDA out of memory`**  
→ Enable "Sequential CPU offload" in Configure, or reduce resolution to 512×512

**Slow generation on CPU**  
→ Expected. CPU inference takes 5–20 min/image. GPU is strongly recommended.

**FLUX.1-dev download fails**  
→ Make sure you've accepted the license on HuggingFace and your token is correct.

**Black or gray output images**  
→ Usually a CFG mismatch. Use guidance_scale=0 for schnell/turbo, 3.5 for dev, 7+ for SDXL.

---

*Product Studio v1.0 — Open source, offline, no APIs, no watermarks.*
