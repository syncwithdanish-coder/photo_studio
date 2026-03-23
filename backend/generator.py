"""
Product Studio — Generator
Two modes:
  1. HuggingFace Inference API  — no local GPU at all, just an internet call
  2. Local SDXL-Turbo           — 4-step, sequential CPU offload, fits 4GB VRAM
"""
import gc
import io
import os
import sys
import time
import traceback
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from PyQt6.QtCore import QThread, pyqtSignal

from backend.config import OUTPUTS_DIR, MODELS_DIR
from backend.models import AVAILABLE_MODELS

# Log to file only — never to stdout (prevents Windows CMD pause)
_log_path = Path.home() / "ProductStudio" / "product_studio.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    handlers=[logging.FileHandler(_log_path, encoding="utf-8")],
)
log = logging.getLogger(__name__)


@dataclass
class GenConfig:
    model_key:   str   = "hf_api_flux_schnell"
    width:       int   = 1024
    height:      int   = 1024
    steps:       int   = 4
    cfg:         float = 0.0
    seed:        int   = -1
    hf_token:    str   = ""


# ─────────────────────────────────────────────────────────────────────────────
class GenerationWorker(QThread):
    progress    = pyqtSignal(int, str)    # (percent, message)
    image_ready = pyqtSignal(str, str)    # (filepath, label)
    error       = pyqtSignal(str)
    finished    = pyqtSignal(list)        # [filepath, ...]

    def __init__(self, prompts: list[dict], config: GenConfig):
        super().__init__()
        self.prompts   = prompts
        self.config    = config
        self._stop     = False
        self._pipe     = None             # cached local pipeline

    def stop(self):
        self._stop = True

    # ── Thread entry ─────────────────────────────────────────────────────────
    def run(self):
        # Strip Anaconda from sys.path in this thread
        sys.path = [p for p in sys.path
                    if not any(x in p.lower() for x in ("anaconda", "conda", "miniconda"))]
        try:
            paths = self._run_all()
            if not self._stop:
                self.finished.emit(paths)
        except Exception as e:
            tb = traceback.format_exc()
            log.error(f"Generation failed:\n{tb}")
            self.error.emit(self._human_error(str(e), tb))

    # ── Main loop ─────────────────────────────────────────────────────────────
    def _run_all(self) -> list[str]:
        model_info = AVAILABLE_MODELS[self.config.model_key]
        total      = len(self.prompts)
        out_paths  = []

        for i, p in enumerate(self.prompts):
            if self._stop:
                break

            pct = int(5 + (i / total) * 88)
            self.progress.emit(pct, f"Generating {p['label']}  ({i+1}/{total})…")
            log.info(f"Shot {i+1}/{total}: {p['label']}")

            ref_images = p.get("ref_images", [])
            if model_info["type"] == "hf_api":
                img_bytes = self._call_hf_api(p["positive"], ref_images)
            else:
                img_bytes = self._run_local(p["positive"], p.get("negative", ""), ref_images)

            # Save
            seed_part = str(self.config.seed) if self.config.seed >= 0 else str(int(time.time()))
            fname     = f"{p.get('shot_id','shot')}_{seed_part}.png"
            fpath     = OUTPUTS_DIR / fname
            fpath.write_bytes(img_bytes)

            out_paths.append(str(fpath))
            self.image_ready.emit(str(fpath), p["label"])
            log.info(f"Saved: {fpath}")

            self.progress.emit(
                int(5 + ((i + 1) / total) * 88),
                f"✓  {p['label']}"
            )

        self.progress.emit(100, f"Done — {len(out_paths)} image(s) generated")
        return out_paths

    # ── HuggingFace Inference API ─────────────────────────────────────────────
    def _call_hf_api(self, prompt: str, ref_images: list = None) -> bytes:
        """
        HF Inference API call.
        If ref_images are provided: uses image-to-image (IP-Adapter style via
        the img2img endpoint) so the actual product appears in the scene.
        Falls back to text-to-image if img2img not supported by the model.
        """
        import urllib.request
        import urllib.error
        import json
        import base64

        model = AVAILABLE_MODELS[self.config.model_key]["api_model"]
        token = self.config.hf_token

        if not token:
            raise RuntimeError(
                "HuggingFace token required for API mode.\n"
                "Go to Upload page → Edit token, or switch to a Local model."
            )

        # ── Build payload ─────────────────────────────────────────────────────
        # If we have reference product images, send the first one as init_image
        # with a strength that preserves the product but applies the scene style.
        ref_b64 = None
        if ref_images:
            try:
                from PIL import Image as PILImage
                import io
                with PILImage.open(ref_images[0]) as im:
                    # Resize to model input size
                    im = im.convert("RGB").resize(
                        (self.config.width, self.config.height),
                        PILImage.LANCZOS
                    )
                    buf = io.BytesIO()
                    im.save(buf, format="PNG")
                    ref_b64 = base64.b64encode(buf.getvalue()).decode()
            except Exception as e:
                log.warning(f"Could not load reference image: {e} — falling back to text2img")

        if ref_b64:
            # img2img: product image → styled scene
            # strength 0.65 = keeps ~35% of product structure, applies 65% scene
            payload = json.dumps({
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": self.config.steps,
                    "guidance_scale":      max(self.config.cfg, 7.5),
                    "width":               self.config.width,
                    "height":              self.config.height,
                    "image":               ref_b64,
                    "strength":            0.72,   # 0=copy image, 1=ignore image
                }
            }).encode("utf-8")
            log.info(f"img2img mode — reference: {ref_images[0]}")
        else:
            # text2img fallback
            payload = json.dumps({
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": self.config.steps,
                    "guidance_scale":      self.config.cfg,
                    "width":               self.config.width,
                    "height":              self.config.height,
                }
            }).encode("utf-8")
            log.info("text2img mode (no reference image)")

        url = f"https://router.huggingface.co/hf-inference/models/{model}"

        req = urllib.request.Request(
            url,
            data    = payload,
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type":  "application/json",
                "Accept":        "image/png",
            },
            method = "POST",
        )

    def _run_local(self, positive: str, negative: str, ref_images: list = None) -> bytes:
        import torch
        from diffusers import (
            StableDiffusionXLPipeline,
            AutoPipelineForText2Image,
            AutoPipelineForImage2Image,
        )
        from diffusers import DPMSolverMultistepScheduler

        has_cuda = torch.cuda.is_available()
        dtype    = torch.float16 if has_cuda else torch.float32
        device   = "cuda" if has_cuda else "cpu"
        model_id = AVAILABLE_MODELS[self.config.model_key]["model_id"]
        mtype    = AVAILABLE_MODELS[self.config.model_key]["type"]

        if self._pipe is None:
            self.progress.emit(3, "Loading model… (~1 min first time, cached after)")
            log.info(f"Loading {model_id}  dtype={dtype}")

            load_kw = {
                "torch_dtype":    dtype,
                "use_safetensors": True,
                "cache_dir":       str(MODELS_DIR),
            }
            # Only use fp16 variant if on GPU
            if has_cuda:
                load_kw["variant"] = "fp16"

            if mtype == "local_sdxl_turbo":
                pipe = AutoPipelineForText2Image.from_pretrained(model_id, **load_kw)
            else:
                pipe = StableDiffusionXLPipeline.from_pretrained(model_id, **load_kw)
                # Faster scheduler for 20-step runs
                pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                    pipe.scheduler.config,
                    use_karras_sigmas=True,
                )

            # 4GB VRAM optimizations
            pipe.enable_sequential_cpu_offload()  # loads each layer to GPU only when needed
            try:
                pipe.enable_attention_slicing(1)  # slice attention computation
            except Exception:
                pass
            try:
                pipe.enable_vae_slicing()         # slice VAE decode
            except Exception:
                pass
            try:
                pipe.enable_vae_tiling()          # tile large images
            except Exception:
                pass

            self._pipe = pipe
            log.info("Pipeline loaded and optimized for 4GB VRAM")

        # Run inference
        seed = self.config.seed if self.config.seed >= 0 else int(time.time() * 1000) % (2**32)
        gen  = torch.Generator(device="cpu").manual_seed(seed)

        # ── img2img when reference product images are available ───────────────
        ref_pil = None
        if ref_images:
            try:
                from PIL import Image as PILImage
                with PILImage.open(ref_images[0]) as im:
                    ref_pil = im.convert("RGB").resize(
                        (self.config.width, self.config.height), PILImage.LANCZOS
                    )
                log.info(f"Local img2img — reference: {ref_images[0]}")
            except Exception as e:
                log.warning(f"Could not load local reference: {e}")

        if ref_pil is not None:
            # Switch to img2img pipeline (reuses same weights, no re-download)
            try:
                img2img_pipe = AutoPipelineForImage2Image.from_pipe(self._pipe)
                kw = dict(
                    prompt              = positive,
                    image               = ref_pil,
                    strength            = 0.72,
                    num_inference_steps = max(self.config.steps, 10),
                    generator           = gen,
                )
                if mtype == "local_sdxl":
                    kw["negative_prompt"] = negative
                    kw["guidance_scale"]  = self.config.cfg
                result = img2img_pipe(**kw)
                img    = result.images[0]
            except Exception as e:
                log.warning(f"img2img failed ({e}), falling back to text2img")
                ref_pil = None

        if ref_pil is None:
            # text2img fallback
            kw = dict(
                prompt              = positive,
                width               = self.config.width,
                height              = self.config.height,
                num_inference_steps = self.config.steps,
                generator           = gen,
            )
            if mtype == "local_sdxl":
                kw["negative_prompt"] = negative
                kw["guidance_scale"]  = self.config.cfg
            result = self._pipe(**kw)
            img    = result.images[0]

        # Convert PIL image to PNG bytes
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf.read()

    # ── Human-readable errors ─────────────────────────────────────────────────
    def _human_error(self, msg: str, tb: str) -> str:
        m = msg.lower()

        if "401" in msg or "token" in m and ("invalid" in m or "access" in m):
            return (
                "🔑  Authentication failed (401)\n\n"
                "Your HuggingFace token is missing or invalid.\n\n"
                "Fix:\n"
                "  1. Go to Upload page → click 'Edit' next to the token field\n"
                "  2. Create a token at https://huggingface.co/settings/tokens\n"
                "  3. For FLUX, accept the licence first at:\n"
                "     https://huggingface.co/black-forest-labs/FLUX.1-schnell\n\n"
                "Or switch to a LOCAL model — those need no token at all."
            )
        if "cuda out of memory" in m or "out of memory" in m:
            return (
                "💾  GPU out of memory\n\n"
                "Your GPU does not have enough VRAM for this resolution.\n\n"
                "Fix:\n"
                "  • Reduce resolution to 512×512 in Configure\n"
                "  • Switch to SDXL-Turbo (4 steps, lightest local model)\n"
                "  • Switch to an API model (runs on HF servers, uses no local GPU)"
            )
        if "no module named" in m or "importerror" in m:
            return (
                "📦  Missing package\n\n"
                f"{msg}\n\n"
                "Run SETUP.bat to reinstall all dependencies."
            )
        if "urllib" in m or "connection" in m or "timeout" in m:
            return (
                "🌐  Network error\n\n"
                f"{msg}\n\n"
                "Check your internet connection and try again.\n"
                "Or switch to a LOCAL model for offline use."
            )
        return f"Error: {msg}"


# ─────────────────────────────────────────────────────────────────────────────
class CollageWorker(QThread):
    finished = pyqtSignal(str)
    error    = pyqtSignal(str)

    def __init__(self, image_paths: list[str], output_path: str):
        super().__init__()
        self.image_paths = image_paths
        self.output_path = output_path

    def run(self):
        try:
            from PIL import Image
            images = [Image.open(p).convert("RGB") for p in self.image_paths]
            n = len(images)
            cols = 2 if n > 2 else n
            rows = (n + cols - 1) // cols
            cw   = max(i.width  for i in images)
            ch   = max(i.height for i in images)
            gap  = 10
            out  = Image.new("RGB",
                             (cols * cw + (cols + 1) * gap,
                              rows * ch + (rows + 1) * gap),
                             (14, 14, 15))
            for idx, img in enumerate(images[:cols * rows]):
                r  = idx // cols
                c  = idx %  cols
                x  = gap + c * (cw + gap)
                y  = gap + r * (ch + gap)
                out.paste(img.resize((cw, ch), Image.LANCZOS), (x, y))
            out.save(self.output_path)
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))
