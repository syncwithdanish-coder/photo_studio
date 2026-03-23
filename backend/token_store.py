"""
Product Studio — Persistent token & config store.
Saves to ~/ProductStudio/config.json
"""
import json
from pathlib import Path

CONFIG_PATH = Path.home() / "ProductStudio" / "config.json"

_DEFAULTS = {
    "hf_token":      "",
    "default_model": "sdxl",
    "welcomed":      False,
}


def load() -> dict:
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            # fill in any missing keys
            for k, v in _DEFAULTS.items():
                data.setdefault(k, v)
            return data
    except Exception:
        pass
    return dict(_DEFAULTS)


def save(patch: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    current = load()
    current.update(patch)
    with open(CONFIG_PATH, "w") as f:
        json.dump(current, f, indent=2)


def get_token() -> str:
    return load().get("hf_token", "")


def get_default_model() -> str:
    return load().get("default_model", "sdxl")


def is_first_run() -> bool:
    return not load().get("welcomed", False)


def mark_welcomed():
    save({"welcomed": True})
