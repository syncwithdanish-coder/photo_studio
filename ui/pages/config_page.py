"""Config page — Stage 3."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QLineEdit, QFrame, QCheckBox, QGridLayout,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices

from backend.config  import get_token, save, get_default_model
from backend.models  import AVAILABLE_MODELS
from backend.generator import GenConfig
from prompts.theme_prompts import get_theme
from ui.auth_dialog  import AuthDialog

LICENCES = {
    "hf_api_flux_schnell": "https://huggingface.co/black-forest-labs/FLUX.1-schnell",
    "hf_api_flux_dev":     "https://huggingface.co/black-forest-labs/FLUX.1-dev",
}


class ConfigPage(QWidget):
    def __init__(self, state, on_next, on_back, parent=None):
        super().__init__(parent)
        self.state   = state
        self.on_next = on_next
        self.on_back = on_back
        self._build()

    def _grp(self, title):
        f = QFrame(); f.setObjectName("config_group")
        lay = QVBoxLayout(f); lay.setContentsMargins(16,12,16,16); lay.setSpacing(10)
        lay.addWidget(QLabel(title, objectName="section_lbl"))
        return f, lay

    def _build(self):
        out = QVBoxLayout(self); out.setContentsMargins(56,32,56,32); out.setSpacing(0)
        out.addWidget(QLabel("Configure Model", objectName="page_title"))
        out.addSpacing(5)
        sub = QLabel("HF API models run on HuggingFace servers — fastest, no local GPU needed. "
                     "Local models run on your 4GB GPU.")
        sub.setObjectName("page_sub"); sub.setWordWrap(True); out.addWidget(sub)
        out.addSpacing(24)

        content = QHBoxLayout(); content.setSpacing(36)

        # LEFT
        lft = QVBoxLayout(); lft.setSpacing(18)

        mg, mi = self._grp("MODEL")
        self.mcb = QComboBox(); self.mcb.setObjectName("combo"); self.mcb.setFixedHeight(44)
        for key, info in AVAILABLE_MODELS.items(): self.mcb.addItem(info["label"], key)
        self.mcb.currentIndexChanged.connect(self._on_model)
        mi.addWidget(self.mcb)
        self.mdesc = QLabel(""); self.mdesc.setObjectName("model_desc"); self.mdesc.setWordWrap(True)
        mi.addWidget(self.mdesc)
        self.mbadge = QLabel(""); self.mbadge.setObjectName("badge_ok"); self.mbadge.setWordWrap(True)
        mi.addWidget(self.mbadge)
        self.lic_btn = QPushButton("→  Accept model licence on HuggingFace")
        self.lic_btn.setObjectName("btn_link"); self.lic_btn.hide()
        self.lic_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lic_btn.clicked.connect(self._open_lic)
        mi.addWidget(self.lic_btn)
        lft.addWidget(mg)

        tg, ti = self._grp("HUGGINGFACE TOKEN")
        hint = QLabel("Not required for Local models.\nRequired for HF API models.")
        hint.setObjectName("field_hint"); hint.setWordWrap(True); ti.addWidget(hint)
        tr = QHBoxLayout()
        self.tok = QLineEdit(); self.tok.setObjectName("input_text")
        self.tok.setFixedHeight(42); self.tok.setEchoMode(QLineEdit.EchoMode.Password)
        self.tok.setPlaceholderText("hf_xxxxxxxxxxxxxxxxxxxx")
        tr.addWidget(self.tok, 1)
        eb = QPushButton("Edit"); eb.setObjectName("btn_micro"); eb.setFixedHeight(42)
        eb.clicked.connect(self._edit_tok); tr.addWidget(eb); ti.addLayout(tr)
        self.tok_st = QLabel(""); self.tok_st.setObjectName("tok_ok"); ti.addWidget(self.tok_st)
        lft.addWidget(tg)
        lft.addStretch(); content.addLayout(lft, 1)

        # RIGHT
        rgt = QVBoxLayout(); rgt.setSpacing(18)

        pg, pi = self._grp("INFERENCE PARAMETERS")
        grid = QGridLayout(); grid.setSpacing(12); grid.setColumnStretch(1, 1)

        for row, (lbl_txt, attr, lo, hi, val) in enumerate([
            ("Steps",           "steps_sp", 1,  100, 4),
            ("Guidance (CFG)",  "cfg_sp",   0,  20,  0),
            ("Seed (-1=random)","seed_sp",  -1, 999999999, -1),
        ]):
            grid.addWidget(QLabel(lbl_txt, objectName="field_lbl"), row, 0)
            sp = QSpinBox(); sp.setObjectName("spinbox")
            sp.setRange(lo, hi); sp.setValue(val); sp.setFixedHeight(40)
            grid.addWidget(sp, row, 1); setattr(self, attr, sp)

        # Resolution
        grid.addWidget(QLabel("Width × Height", objectName="field_lbl"), 3, 0)
        res_row = QHBoxLayout()
        self.wcb = QComboBox(); self.wcb.setObjectName("combo"); self.wcb.setFixedHeight(40)
        self.hcb = QComboBox(); self.hcb.setObjectName("combo"); self.hcb.setFixedHeight(40)
        for cb in (self.wcb, self.hcb):
            for r in ["512","768","1024"]: cb.addItem(r, int(r))
            cb.setCurrentText("1024")
        res_row.addWidget(self.wcb); res_row.addWidget(QLabel("×")); res_row.addWidget(self.hcb)
        grid.addLayout(res_row, 3, 1)
        pi.addLayout(grid); rgt.addWidget(pg)

        vg, vi = self._grp("MEMORY  (Local models only)")
        self.fp16  = QCheckBox("FP16 — halves VRAM, recommended")
        self.fp16.setObjectName("cfg_chk"); self.fp16.setChecked(True)
        self.seq   = QCheckBox("Sequential CPU offload — fits 4GB VRAM (slower)")
        self.seq.setObjectName("cfg_chk"); self.seq.setChecked(True)
        self.vae_s = QCheckBox("VAE slicing — reduces peak VRAM further")
        self.vae_s.setObjectName("cfg_chk"); self.vae_s.setChecked(True)
        for w in (self.fp16, self.seq, self.vae_s): vi.addWidget(w)
        rgt.addWidget(vg); rgt.addStretch(); content.addLayout(rgt, 1)

        out.addLayout(content); out.addStretch()
        self.summary = QLabel(""); self.summary.setObjectName("summary_bar")
        self.summary.setWordWrap(True); out.addWidget(self.summary); out.addSpacing(14)

        nav = QHBoxLayout()
        bk = QPushButton("← Back"); bk.setObjectName("btn_secondary"); bk.clicked.connect(self.on_back)
        nav.addWidget(bk); nav.addStretch()
        go = QPushButton("Start Generation  →"); go.setObjectName("btn_primary")
        go.setCursor(Qt.CursorShape.PointingHandCursor); go.clicked.connect(self._go)
        nav.addWidget(go); out.addLayout(nav)

        self._load_saved()

    def _load_saved(self):
        tok = get_token()
        if tok: self.tok.setText(tok); self.tok_st.setText("✓ Token loaded")
        key = self.state.get("default_model") or get_default_model()
        for i in range(self.mcb.count()):
            if self.mcb.itemData(i) == key: self.mcb.setCurrentIndex(i); break
        self._on_model(self.mcb.currentIndex())

    def _on_model(self, _=None):
        key  = self.mcb.currentData()
        info = AVAILABLE_MODELS.get(key, {})
        self.mdesc.setText(f"ℹ  {info.get('description','')}")
        self.steps_sp.setValue(info.get("steps_default", 4))
        self.cfg_sp.setValue(int(info.get("cfg_default", 0)))
        if info.get("token_required"):
            self.mbadge.setText("⚠  Free HF token required")
            self.mbadge.setObjectName("badge_warn")
            self.tok.setEnabled(True)
            self.lic_btn.setVisible(key in LICENCES)
        else:
            self.mbadge.setText("✓  No token required — runs locally")
            self.mbadge.setObjectName("badge_ok")
            self.tok.setEnabled(False)
            self.lic_btn.hide()
        self.mbadge.style().unpolish(self.mbadge); self.mbadge.style().polish(self.mbadge)

    def _open_lic(self):
        key = self.mcb.currentData()
        QDesktopServices.openUrl(QUrl(LICENCES.get(key, "https://huggingface.co")))

    def _edit_tok(self):
        dlg = AuthDialog(self, first_time=False)
        if dlg.exec():
            t = dlg.get_token(); self.tok.setText(t); self.state["hf_token"] = t
            self.tok_st.setText("✓ Token saved"); save({"hf_token": t})

    def refresh(self):
        tid  = self.state.get("selected_theme")
        n    = len(self.state.get("selected_shots", []))
        col  = self.state.get("generate_collage", True)
        name = get_theme(tid)["name"] if tid else "—"
        self.summary.setText(
            f"Ready:  {name}  ·  {n} shot{'s' if n!=1 else ''}  "
            f"{'+ collage' if col else ''}  ·  {self.mcb.currentText()}"
        )
        if self.state.get("hf_token") and not self.tok.text():
            self.tok.setText(self.state["hf_token"])
        default = self.state.get("default_model")
        if default:
            for i in range(self.mcb.count()):
                if self.mcb.itemData(i) == default: self.mcb.setCurrentIndex(i); break

    def _go(self):
        key  = self.mcb.currentData()
        info = AVAILABLE_MODELS[key]
        tok  = self.tok.text().strip() or get_token()
        if info.get("token_required") and not tok:
            dlg = AuthDialog(self, first_time=False)
            if dlg.exec(): tok = dlg.get_token(); save({"hf_token": tok})
            else:
                # fall back to first local model
                for k, v in AVAILABLE_MODELS.items():
                    if not v.get("token_required"):
                        key = k; info = v; tok = ""; break

        cfg = GenConfig(
            model_key = key,
            width     = self.wcb.currentData(),
            height    = self.hcb.currentData(),
            steps     = self.steps_sp.value(),
            cfg       = float(self.cfg_sp.value()),
            seed      = self.seed_sp.value(),
            hf_token  = tok,
        )
        self.state["gen_config"] = cfg
        self.state["hf_token"]   = tok
        self.on_next()
