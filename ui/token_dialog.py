"""
Product Studio — HuggingFace Token Dialog
Shown on first launch and whenever a 401 error occurs.
"""

import json
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QCheckBox,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QFont

CONFIG_PATH = Path.home() / "ProductStudio" / "config.json"


def load_config() -> dict:
    """Load persisted config from disk."""
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_config(data: dict):
    """Persist config to disk."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = load_config()
        existing.update(data)
        with open(CONFIG_PATH, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception:
        pass


def get_saved_token() -> str:
    return load_config().get("hf_token", "")


def get_default_model() -> str:
    return load_config().get("default_model", "sdxl")


class TokenDialog(QDialog):
    """
    Full-screen-style dialog for setting the HuggingFace token.
    Shown:
      - On first launch (no token saved, no config.json)
      - After a 401 error from the API
    """

    def __init__(self, parent=None, is_first_time: bool = False, error_msg: str = ""):
        super().__init__(parent)
        self.is_first_time = is_first_time
        self.setWindowTitle("HuggingFace Authentication")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build_ui(error_msg)

    def _build_ui(self, error_msg: str):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(36, 32, 36, 28)
        outer.setSpacing(20)

        # ── Title ──────────────────────────────────────────────────────────
        if self.is_first_time:
            title = QLabel("Welcome to Product Studio")
            title.setObjectName("dialog_title")
            outer.addWidget(title)

            intro = QLabel(
                "To use FLUX models (highest quality), you need a free HuggingFace token.\n"
                "SDXL works without any token — you can skip this step."
            )
            intro.setObjectName("dialog_sub")
            intro.setWordWrap(True)
            outer.addWidget(intro)
        else:
            title = QLabel("Authentication Required")
            title.setObjectName("dialog_title")
            outer.addWidget(title)

        # ── Error box (only shown on 401) ──────────────────────────────────
        if error_msg:
            err_frame = QFrame()
            err_frame.setObjectName("dialog_error_box")
            err_layout = QVBoxLayout(err_frame)
            err_layout.setContentsMargins(14, 12, 14, 12)
            err_lbl = QLabel(f"⚠  {error_msg}")
            err_lbl.setObjectName("dialog_error_text")
            err_lbl.setWordWrap(True)
            err_layout.addWidget(err_lbl)
            outer.addWidget(err_frame)

        # ── Steps ──────────────────────────────────────────────────────────
        steps_frame = QFrame()
        steps_frame.setObjectName("dialog_steps_box")
        steps_layout = QVBoxLayout(steps_frame)
        steps_layout.setContentsMargins(14, 14, 14, 14)
        steps_layout.setSpacing(10)

        steps_title = QLabel("HOW TO GET A FREE TOKEN")
        steps_title.setObjectName("dialog_steps_title")
        steps_layout.addWidget(steps_title)

        steps = [
            ("1", "Create a free account", "huggingface.co", "https://huggingface.co/join"),
            ("2", "Accept the FLUX.1-schnell licence", "FLUX.1-schnell page", "https://huggingface.co/black-forest-labs/FLUX.1-schnell"),
            ("3", "Accept the FLUX.1-dev licence (optional)", "FLUX.1-dev page", "https://huggingface.co/black-forest-labs/FLUX.1-dev"),
            ("4", "Create a Read token", "tokens settings page", "https://huggingface.co/settings/tokens"),
        ]

        for num, text, link_text, link_url in steps:
            row = QHBoxLayout()
            row.setSpacing(10)

            num_lbl = QLabel(num)
            num_lbl.setObjectName("step_num_badge")
            num_lbl.setFixedSize(24, 24)
            num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(num_lbl)

            step_lbl = QLabel(f"{text}  —  ")
            step_lbl.setObjectName("dialog_step_text")
            row.addWidget(step_lbl)

            link_btn = QPushButton(f"Open {link_text} ↗")
            link_btn.setObjectName("dialog_link_btn")
            link_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            url = link_url  # capture
            link_btn.clicked.connect(lambda _, u=url: QDesktopServices.openUrl(QUrl(u)))
            row.addWidget(link_btn)
            row.addStretch()
            steps_layout.addLayout(row)

        outer.addWidget(steps_frame)

        # ── Token input ────────────────────────────────────────────────────
        token_lbl = QLabel("Paste your HuggingFace token here:")
        token_lbl.setObjectName("field_label")
        outer.addWidget(token_lbl)

        token_row = QHBoxLayout()
        self.token_input = QLineEdit()
        self.token_input.setObjectName("config_input")
        self.token_input.setPlaceholderText("hf_xxxxxxxxxxxxxxxxxxxx")
        self.token_input.setFixedHeight(44)
        saved = get_saved_token()
        if saved:
            self.token_input.setText(saved)

        self.show_chk = QCheckBox("Show")
        self.show_chk.setObjectName("config_chk")
        self.show_chk.toggled.connect(
            lambda v: self.token_input.setEchoMode(
                QLineEdit.EchoMode.Normal if v else QLineEdit.EchoMode.Password
            )
        )
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)

        token_row.addWidget(self.token_input, 1)
        token_row.addWidget(self.show_chk)
        outer.addLayout(token_row)

        self.save_chk = QCheckBox("Remember token on this computer")
        self.save_chk.setObjectName("config_chk")
        self.save_chk.setChecked(True)
        outer.addWidget(self.save_chk)

        # ── Buttons ────────────────────────────────────────────────────────
        btn_row = QHBoxLayout()

        if self.is_first_time:
            skip_btn = QPushButton("Skip — use SDXL (no token needed)")
            skip_btn.setObjectName("secondary_btn")
            skip_btn.clicked.connect(self.reject)
            btn_row.addWidget(skip_btn)

        btn_row.addStretch()

        save_btn = QPushButton("Save Token  ✓")
        save_btn.setObjectName("primary_btn")
        save_btn.clicked.connect(self._save_and_accept)
        btn_row.addWidget(save_btn)

        outer.addLayout(btn_row)

    def _save_and_accept(self):
        token = self.token_input.text().strip()
        if self.save_chk.isChecked() and token:
            save_config({"hf_token": token})
        self.accept()

    def get_token(self) -> str:
        return self.token_input.text().strip()
