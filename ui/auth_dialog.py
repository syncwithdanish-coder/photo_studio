"""Auth dialog — shown on first run and on 401 errors."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QCheckBox,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from backend.config import get_token, save


class AuthDialog(QDialog):
    def __init__(self, parent=None, first_time: bool = True):
        super().__init__(parent)
        self.first_time = first_time
        self.setWindowTitle("HuggingFace Setup" if first_time else "Authentication Required")
        self.setModal(True)
        self.setMinimumWidth(620)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build()

    def _build(self):
        out = QVBoxLayout(self)
        out.setContentsMargins(36, 28, 36, 24)
        out.setSpacing(16)

        title = QLabel("Welcome to Product Studio" if self.first_time else "Authentication Required  (401)")
        title.setObjectName("dlg_title" if self.first_time else "dlg_title_warn")
        out.addWidget(title)

        sub = QLabel(
            "For the <b>HF API models</b> (fastest, no local GPU), a free HuggingFace token is needed.<br>"
            "For <b>Local SDXL</b> models, no token is required at all — click Skip."
            if self.first_time else
            "Your token is missing or invalid. Follow the steps below, then paste and save."
        )
        sub.setObjectName("dlg_sub")
        sub.setWordWrap(True)
        sub.setTextFormat(Qt.TextFormat.RichText)
        out.addWidget(sub)

        # Steps
        steps_box = QFrame()
        steps_box.setObjectName("dlg_steps")
        sb = QVBoxLayout(steps_box)
        sb.setContentsMargins(16, 14, 16, 14)
        sb.setSpacing(10)
        lbl = QLabel("4 STEPS TO GET A FREE TOKEN")
        lbl.setObjectName("dlg_steps_title")
        sb.addWidget(lbl)

        for num, text, link_lbl, url in [
            ("1", "Create free account",           "huggingface.co/join →",          "https://huggingface.co/join"),
            ("2", "Accept FLUX.1-schnell licence", "Open model page →",              "https://huggingface.co/black-forest-labs/FLUX.1-schnell"),
            ("3", "Accept FLUX.1-dev licence",     "Open model page →",              "https://huggingface.co/black-forest-labs/FLUX.1-dev"),
            ("4", "Create a READ token",           "huggingface.co/settings/tokens →","https://huggingface.co/settings/tokens"),
        ]:
            row = QHBoxLayout()
            badge = QLabel(num)
            badge.setObjectName("step_badge")
            badge.setFixedSize(26, 26)
            badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row.addWidget(badge)
            row.addWidget(QLabel(text, objectName="dlg_step_txt"))
            row.addStretch()
            btn = QPushButton(link_lbl)
            btn.setObjectName("btn_link")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, u=url: QDesktopServices.openUrl(QUrl(u)))
            row.addWidget(btn)
            sb.addLayout(row)

        out.addWidget(steps_box)

        # Token input
        out.addWidget(QLabel("Paste your token here:", objectName="field_lbl"))
        tok_row = QHBoxLayout()
        self.tok = QLineEdit()
        self.tok.setObjectName("input_text")
        self.tok.setFixedHeight(46)
        self.tok.setEchoMode(QLineEdit.EchoMode.Password)
        self.tok.setPlaceholderText("hf_xxxxxxxxxxxxxxxxxxxx")
        saved = get_token()
        if saved:
            self.tok.setText(saved)
        tok_row.addWidget(self.tok, 1)
        show = QCheckBox("Show")
        show.toggled.connect(lambda v: self.tok.setEchoMode(
            QLineEdit.EchoMode.Normal if v else QLineEdit.EchoMode.Password))
        tok_row.addWidget(show)
        out.addLayout(tok_row)

        self.remember = QCheckBox("Remember token on this computer")
        self.remember.setObjectName("cfg_chk")
        self.remember.setChecked(True)
        out.addWidget(self.remember)

        btns = QHBoxLayout()
        if self.first_time:
            skip = QPushButton("Skip — Use Local Models (no token)")
            skip.setObjectName("btn_secondary")
            skip.clicked.connect(self.reject)
            btns.addWidget(skip)
        btns.addStretch()
        save_btn = QPushButton("  Save Token  ✓  ")
        save_btn.setObjectName("btn_primary")
        save_btn.clicked.connect(self._save)
        btns.addWidget(save_btn)
        out.addLayout(btns)

    def _save(self):
        token = self.tok.text().strip()
        if self.remember.isChecked() and token:
            save({"hf_token": token})
        self.accept()

    def get_token(self) -> str:
        return self.tok.text().strip()
