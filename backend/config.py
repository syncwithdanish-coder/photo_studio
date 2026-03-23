"""
Persistent config — saves to ~/ProductStudio/config.json
"""
import json
from pathlib import Path

CONFIG_FILE = Path.home() / "ProductStudio" / "config.json"
OUTPUTS_DIR = Path.home() / "ProductStudio" / "outputs"
MODELS_DIR  = Path.home() / "ProductStudio" / "models"

for _d in (CONFIG_FILE.parent, OUTPUTS_DIR, MODELS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

_DEFAULTS = {
    "hf_token":      "",
    "default_model": "sdxl_turbo",
    "welcomed":      False,
}

def load() -> dict:
    try:
        if CONFIG_FILE.exists():
            d = json.loads(CONFIG_FILE.read_text("utf-8"))
            for k, v in _DEFAULTS.items():
                d.setdefault(k, v)
            return d
    except Exception:
        pass
    return dict(_DEFAULTS)

def save(patch: dict):
    d = load()
    d.update(patch)
    CONFIG_FILE.write_text(json.dumps(d, indent=2), encoding="utf-8")

def get_token()         -> str:  return load().get("hf_token", "")
def get_default_model() -> str:  return load().get("default_model", "sdxl_turbo")
def is_first_run()      -> bool: return not load().get("welcomed", False)
def mark_welcomed():             save({"welcomed": True})
