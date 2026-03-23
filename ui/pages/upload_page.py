"""Upload page — Stage 1."""
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QScrollArea, QFileDialog, QComboBox, QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImageReader

from backend.config  import load, save, get_token, get_default_model, is_first_run, mark_welcomed
from backend.models  import AVAILABLE_MODELS
from ui.auth_dialog  import AuthDialog


class Thumb(QFrame):
    removed = pyqtSignal(str)

    def __init__(self, path: str, parent=None):
        super().__init__(parent)
        self.path = path
        self.setObjectName("img_thumb")
        self.setFixedSize(158, 168)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(3)

        img = QLabel()
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setFixedHeight(126)

        try:
            reader = QImageReader(path)
            reader.setAutoTransform(True)
            qi = reader.read()
            if not qi.isNull():
                pix = QPixmap.fromImage(qi).scaled(
                    146, 122,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                img.setPixmap(pix)
            else:
                raise RuntimeError("null image")
        except Exception:
            try:
                from PIL import Image as PILImg
                import tempfile
                with PILImg.open(path) as im:
                    buf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                    im.convert("RGB").save(buf.name)
                    buf.close()
                pix = QPixmap(buf.name).scaled(
                    146, 122,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                os.unlink(buf.name)
                img.setPixmap(pix)
            except Exception:
                img.setText("🖼")
                img.setStyleSheet("font-size:28px;color:#5a5652;")

        lay.addWidget(img)

        name = Path(path).name
        name_lbl = QLabel(name[:18] + "…" if len(name) > 18 else name)
        name_lbl.setObjectName("thumb_name")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(name_lbl)

        rm = QPushButton("✕")
        rm.setObjectName("thumb_remove")
        rm.setFixedSize(22, 22)
        rm.setCursor(Qt.CursorShape.PointingHandCursor)
        rm.clicked.connect(lambda: self.removed.emit(self.path))
        rm.setParent(self)
        rm.move(132, 4)


class DropZone(QFrame):
    dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("drop_zone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(140)
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(6)
        for txt, obj in [("⬆", "drop_icon"),
                          ("Drop images here", "drop_title"),
                          ("JPG · PNG · WEBP  ·  1–5 images", "drop_sub")]:
            l = QLabel(txt); l.setObjectName(obj)
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(l)

    def _set(self, name):
        self.setObjectName(name); self.style().unpolish(self); self.style().polish(self)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls(): e.acceptProposedAction(); self._set("drop_zone_active")

    def dragLeaveEvent(self, e): self._set("drop_zone")

    def dropEvent(self, e):
        self._set("drop_zone")
        paths = [u.toLocalFile() for u in e.mimeData().urls()
                 if u.toLocalFile().lower().endswith(
                     (".jpg",".jpeg",".png",".webp",".bmp",".tif",".tiff"))]
        if paths: self.dropped.emit(paths)


class UploadPage(QWidget):
    def __init__(self, state: dict, on_next, parent=None):
        super().__init__(parent)
        self.state   = state
        self.on_next = on_next
        self._build()
        # First-run welcome after UI is ready
        if is_first_run():
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(300, self._welcome)

    def _welcome(self):
        dlg = AuthDialog(self, first_time=True)
        if dlg.exec():
            tok = dlg.get_token()
            if tok:
                self._set_token(tok)
        mark_welcomed()
        # Load any saved settings
        cfg = load()
        if cfg.get("hf_token") and not self.state.get("hf_token"):
            self._set_token(cfg["hf_token"], silent=True)

    def _set_token(self, tok: str, silent: bool = False):
        self.state["hf_token"] = tok
        self.tok_inp.blockSignals(True)
        self.tok_inp.setText(tok)
        self.tok_inp.blockSignals(False)
        if not silent:
            save({"hf_token": tok})
        self.tok_status.setText("✓ Token saved")
        self.tok_status.setObjectName("tok_ok")

    def _build(self):
        out = QVBoxLayout(self)
        out.setContentsMargins(56, 32, 56, 32)
        out.setSpacing(0)

        out.addWidget(QLabel("Upload Product Images", objectName="page_title"))
        out.addSpacing(5)
        sub = QLabel("Upload 1–5 product photos. Select your AI model on the right — "
                     "<b>HF API models run on HuggingFace servers (no local GPU needed)</b>, "
                     "local models run on your 4GB GPU.")
        sub.setObjectName("page_sub"); sub.setWordWrap(True)
        sub.setTextFormat(Qt.TextFormat.RichText)
        out.addWidget(sub)
        out.addSpacing(20)

        cols = QHBoxLayout(); cols.setSpacing(32)

        # LEFT
        left = QVBoxLayout(); left.setSpacing(10)

        left.addWidget(QLabel("Product Description", objectName="field_lbl"))
        self.desc = QLineEdit()
        self.desc.setObjectName("input_text")
        self.desc.setPlaceholderText("e.g.  matte black ceramic non-stick frying pan")
        self.desc.setFixedHeight(44)
        left.addWidget(self.desc)

        self.drop = DropZone()
        self.drop.dropped.connect(self._add)
        left.addWidget(self.drop)

        br = QHBoxLayout()
        bb = QPushButton("Browse Files…")
        bb.setObjectName("btn_secondary")
        bb.setCursor(Qt.CursorShape.PointingHandCursor)
        bb.clicked.connect(self._browse)
        self.cnt = QLabel("0 / 5 images"); self.cnt.setObjectName("count_lbl")
        br.addWidget(bb); br.addWidget(self.cnt); br.addStretch()
        left.addLayout(br)

        sc = QScrollArea(); sc.setObjectName("thumb_scroll")
        sc.setWidgetResizable(True); sc.setFixedHeight(185)
        sc.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tc = QWidget()
        self.tl = QHBoxLayout(self.tc)
        self.tl.setContentsMargins(4,4,4,4); self.tl.setSpacing(8)
        self.tl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sc.setWidget(self.tc)
        left.addWidget(sc)
        cols.addLayout(left, 3)

        # RIGHT sidebar
        sb = QFrame(); sb.setObjectName("sidebar")
        sbl = QVBoxLayout(sb); sbl.setContentsMargins(20,18,20,18); sbl.setSpacing(12)

        sbl.addWidget(QLabel("AI MODEL", objectName="section_lbl"))

        self.model_cb = QComboBox(); self.model_cb.setObjectName("combo")
        self.model_cb.setFixedHeight(42)
        for key, info in AVAILABLE_MODELS.items():
            self.model_cb.addItem(info["label"], key)

        saved = get_default_model()
        for i in range(self.model_cb.count()):
            if self.model_cb.itemData(i) == saved:
                self.model_cb.setCurrentIndex(i); break

        self.model_cb.currentIndexChanged.connect(self._on_model)
        sbl.addWidget(self.model_cb)

        self.mdesc = QLabel(""); self.mdesc.setObjectName("model_desc")
        self.mdesc.setWordWrap(True); sbl.addWidget(self.mdesc)

        self.badge = QLabel(""); self.badge.setObjectName("badge_ok")
        self.badge.setWordWrap(True); sbl.addWidget(self.badge)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine); div.setObjectName("top_div")
        sbl.addWidget(div)

        sbl.addWidget(QLabel("HUGGINGFACE TOKEN", objectName="section_lbl"))

        tr = QHBoxLayout()
        self.tok_inp = QLineEdit(); self.tok_inp.setObjectName("input_text")
        self.tok_inp.setFixedHeight(40); self.tok_inp.setEchoMode(QLineEdit.EchoMode.Password)
        self.tok_inp.setPlaceholderText("Paste token or click Edit")
        self.tok_inp.textChanged.connect(self._on_tok)
        tr.addWidget(self.tok_inp, 1)
        edit = QPushButton("Edit"); edit.setObjectName("btn_micro")
        edit.setFixedHeight(40); edit.setCursor(Qt.CursorShape.PointingHandCursor)
        edit.clicked.connect(self._edit_tok)
        tr.addWidget(edit); sbl.addLayout(tr)

        self.tok_status = QLabel(""); self.tok_status.setObjectName("tok_ok")
        sbl.addWidget(self.tok_status)
        sbl.addStretch()
        cols.addWidget(sb, 2)

        out.addLayout(cols, 1)
        out.addSpacing(16)

        nav = QHBoxLayout(); nav.addStretch()
        self.nxt = QPushButton("Continue to Theme Selection  →")
        self.nxt.setObjectName("btn_primary"); self.nxt.setEnabled(False)
        self.nxt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nxt.clicked.connect(self._next)
        nav.addWidget(self.nxt); out.addLayout(nav)

        # init
        self._on_model(self.model_cb.currentIndex())
        tok = get_token()
        if tok:
            self._set_token(tok, silent=True)

    def _on_model(self, _=None):
        key  = self.model_cb.currentData()
        info = AVAILABLE_MODELS.get(key, {})
        self.mdesc.setText(info.get("description", ""))
        if info.get("token_required"):
            self.badge.setText("⚠  Free HF token required for this model")
            self.badge.setObjectName("badge_warn")
        else:
            self.badge.setText("✓  No token required — runs locally")
            self.badge.setObjectName("badge_ok")
        self.badge.style().unpolish(self.badge); self.badge.style().polish(self.badge)
        save({"default_model": key}); self.state["default_model"] = key

    def _on_tok(self, text):
        tok = text.strip(); self.state["hf_token"] = tok
        if tok: save({"hf_token": tok}); self.tok_status.setText("✓ Token saved")

    def _edit_tok(self):
        dlg = AuthDialog(self, first_time=False)
        if dlg.exec(): self._set_token(dlg.get_token())

    def _browse(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Product Images", "",
            "Images (*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tiff)"
        )
        if files: self._add(files)

    def _add(self, paths):
        imgs = self.state["uploaded_images"]
        for p in paths:
            if p not in imgs and len(imgs) < 5 and os.path.isfile(p):
                imgs.append(p)
                try:
                    t = Thumb(p); t.removed.connect(self._remove)
                    self.tl.addWidget(t)
                except Exception:
                    pass
        self._refresh()

    def _remove(self, path):
        if path in self.state["uploaded_images"]:
            self.state["uploaded_images"].remove(path)
        for i in range(self.tl.count()):
            w = self.tl.itemAt(i)
            if w and w.widget() and getattr(w.widget(), "path", None) == path:
                w.widget().deleteLater(); break
        self._refresh()

    def _refresh(self):
        n = len(self.state["uploaded_images"])
        self.cnt.setText(f"{n} / 5 images"); self.nxt.setEnabled(n >= 1)
        self.drop.setEnabled(n < 5)

    def _next(self):
        self.state["product_description"] = self.desc.text().strip() or "product"
        self.state["default_model"]       = self.model_cb.currentData()
        self.on_next()

    def reset(self):
        for p in list(self.state.get("uploaded_images", [])): self._remove(p)
        self.state["uploaded_images"] = []; self.desc.clear(); self._refresh()
