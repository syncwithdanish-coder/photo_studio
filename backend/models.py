"""
Model registry.
Strategy: Use HuggingFace Inference API for FLUX (no local VRAM needed at all),
fall back to local SDXL-Turbo for offline use (4-step, runs in 4GB VRAM).
"""

AVAILABLE_MODELS = {
    "hf_api_flux_schnell": {
        "label":          "FLUX.1-schnell via HF API  ⚡ (Fast, no local GPU needed)",
        "type":           "hf_api",
        "api_model":      "black-forest-labs/FLUX.1-schnell",
        "steps_default":  4,
        "cfg_default":    0.0,
        "description":    "Runs on HuggingFace servers. No local GPU. Needs free HF token. ~5-15s/image.",
        "token_required": True,
        "local":          False,
    },
    "hf_api_sdxl": {
        "label":          "SDXL via HF API  (No GPU, needs free HF token)",
        "type":           "hf_api",
        "api_model":      "stabilityai/stable-diffusion-xl-base-1.0",
        "steps_default":  30,
        "cfg_default":    7.5,
        "description":    "Runs on HuggingFace servers. No local GPU. Needs free HF token.",
        "token_required": True,
        "local":          False,
    },
    "sdxl_turbo": {
        "label":          "SDXL-Turbo Local  (4GB VRAM, no token needed ✓)",
        "type":           "local_sdxl_turbo",
        "model_id":       "stabilityai/sdxl-turbo",
        "steps_default":  4,
        "cfg_default":    0.0,
        "description":    "Runs locally. 4 steps, ~20-40s/image on 4GB GPU. No token required. ~7GB download.",
        "token_required": False,
        "local":          True,
    },
    "sdxl_local": {
        "label":          "SDXL Local  (4GB VRAM, no token needed ✓, best quality)",
        "type":           "local_sdxl",
        "model_id":       "stabilityai/stable-diffusion-xl-base-1.0",
        "steps_default":  20,
        "cfg_default":    7.0,
        "description":    "Runs locally. 20 steps, ~60-90s/image on 4GB GPU. No token required. ~7GB download.",
        "token_required": False,
        "local":          True,
    },
}
