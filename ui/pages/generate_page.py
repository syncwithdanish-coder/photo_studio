"""Generate page — Stage 4."""
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QScrollArea, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap

from backend.generator import GenerationWorker, CollageWorker, GenConfig
from backend.config    import OUTPUTS_DIR, save
from prompts.theme_prompts import get_theme, build_prompt, NEGATIVE_PROMPT as NEGATIVE
from ui.auth_dialog    import AuthDialog


class LiveThumb(QFrame):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.setObjectName("live_thumb"); self.setFixedSize(192, 222)
        lay = QVBoxLayout(self); lay.setContentsMargins(5,5,5,5); lay.setSpacing(5)
        self.img = QLabel("⏳")
        self.img.setObjectName("live_thumb"); self.img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img.setFixedHeight(175); lay.addWidget(self.img)
        self.lbl = QLabel(label); self.lbl.setObjectName("live_lbl")
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); self.lbl.setWordWrap(True)
        lay.addWidget(self.lbl)

    def set_image(self, path):
        pix = QPixmap(path).scaled(180, 162,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        self.img.setPixmap(pix); self.img.setText("")
        self.setObjectName("live_thumb_done")
        self.style().unpolish(self); self.style().polish(self)


class GeneratePage(QWidget):
    def __init__(self, state, on_done, on_back, parent=None):
        super().__init__(parent)
        self.state   = state
        self.on_done = on_done
        self.on_back = on_back
        self._worker = self._collage = None
        self._thumbs: dict[str, LiveThumb] = {}
        self._prompts = []
        self._build()

    def _build(self):
        out = QVBoxLayout(self); out.setContentsMargins(56,32,56,32); out.setSpacing(0)
        out.addWidget(QLabel("Generating Images", objectName="page_title"))
        out.addSpacing(6)
        self.status = QLabel("Starting…"); self.status.setObjectName("page_sub")
        self.status.setWordWrap(True); out.addWidget(self.status)
        out.addSpacing(16)

        self.bar = QProgressBar(); self.bar.setObjectName("gen_progress")
        self.bar.setRange(0, 100); self.bar.setTextVisible(False); self.bar.setFixedHeight(10)
        out.addWidget(self.bar)
        self.pct = QLabel("0%"); self.pct.setObjectName("pct_lbl"); out.addWidget(self.pct)
        out.addSpacing(20)

        sc = QScrollArea(); sc.setObjectName("live_scroll"); sc.setWidgetResizable(True)
        self.tc = QWidget(); self.tl = QHBoxLayout(self.tc)
        self.tl.setContentsMargins(4,4,4,4); self.tl.setSpacing(12)
        self.tl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sc.setWidget(self.tc); out.addWidget(sc, 1); out.addSpacing(16)

        self.err = QLabel(""); self.err.setObjectName("error_box")
        self.err.setWordWrap(True); self.err.hide(); out.addWidget(self.err)

        nav = QHBoxLayout()
        self.cancel = QPushButton("✕ Cancel"); self.cancel.setObjectName("btn_danger")
        self.cancel.clicked.connect(self._cancel); nav.addWidget(self.cancel)
        nav.addStretch()
        self.nxt = QPushButton("View Results  →"); self.nxt.setObjectName("btn_primary")
        self.nxt.setEnabled(False); self.nxt.clicked.connect(self.on_done)
        nav.addWidget(self.nxt); out.addLayout(nav)

    def start_generation(self):
        # Reset
        while self.tl.count():
            item = self.tl.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._thumbs.clear(); self.bar.setValue(0); self.pct.setText("0%")
        self.nxt.setEnabled(False); self.cancel.setEnabled(True)
        self.err.hide(); self.state["generated_images"] = {}

        theme_id = self.state.get("selected_theme", "")
        sel      = self.state.get("selected_shots", [])
        product  = self.state.get("product_description", "product")
        cfg: GenConfig = self.state["gen_config"]

        # Guard: get_theme can return None if theme_id doesn't match
        theme = get_theme(theme_id)
        if not theme:
            self._on_error(
                f"Theme '{theme_id}' not found. Please go back and select a theme again."
            )
            return

        # Collect uploaded reference images (used for image-guided generation)
        ref_images = self.state.get("uploaded_images", [])

        prompts = []
        for shot in theme["shots"]:
            if shot["id"] not in sel: continue
            t = LiveThumb(shot["label"])
            self._thumbs[shot["id"]] = t; self.tl.addWidget(t)
            prompts.append({
                "label":      shot["label"],
                "shot_id":    f"{theme_id}_{shot['id']}",
                "positive":   build_prompt(shot["prompt"], product),
                "negative":   NEGATIVE,
                "ref_images": ref_images,   # pass uploaded images for img2img guidance
            })

        self._prompts = prompts
        if ref_images:
            self.status.setText(
                f"Generating with your {len(ref_images)} product image(s) as reference… "
                "The AI will style your actual product in each scene."
            )
        else:
            self.status.setText("Loading model… API models start in ~5s, local models in ~60s first run")
        self._start_worker(prompts, cfg)

    def _start_worker(self, prompts, cfg):
        self._worker = GenerationWorker(prompts, cfg)
        self._worker.progress.connect(self._on_progress)
        self._worker.image_ready.connect(self._on_image)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    @pyqtSlot(int, str)
    def _on_progress(self, pct, msg):
        if pct >= 0: self.bar.setValue(pct); self.pct.setText(f"{pct}%")
        self.status.setText(msg)

    @pyqtSlot(str, str)
    def _on_image(self, path, label):
        for sid, thumb in self._thumbs.items():
            if sid in path: thumb.set_image(path); break
        else:
            for thumb in self._thumbs.values():
                if not thumb.img.pixmap() or thumb.img.pixmap().isNull():
                    thumb.set_image(path); break
        self.state["generated_images"][label] = path

    @pyqtSlot(list)
    def _on_done(self, paths):
        self.cancel.setEnabled(False)
        self.state["generated_image_paths"] = paths
        if self.state.get("generate_collage") and len(paths) >= 2:
            self.status.setText("Building collage…")
            cp = str(OUTPUTS_DIR / f"collage_{self.state['selected_theme']}.png")
            self._collage = CollageWorker(paths, cp)
            self._collage.finished.connect(self._on_collage)
            self._collage.error.connect(lambda e: self._finish(paths))
            self._collage.start()
        else:
            self._finish(paths)

    def _on_collage(self, path):
        self.state["collage_path"] = path
        t = LiveThumb("▦ Collage"); t.set_image(path); self.tl.addWidget(t)
        self._finish(self.state.get("generated_image_paths", []))

    def _finish(self, paths):
        self.status.setText(f"✓ Done — {len(paths)} image(s) ready")
        self.nxt.setEnabled(True)

    @pyqtSlot(str)
    def _on_error(self, msg):
        self.cancel.setEnabled(False)
        self.status.setText("Generation failed.")

        # Auth error → popup and retry
        if "401" in msg or "token" in msg.lower():
            dlg = AuthDialog(self, first_time=False)
            if dlg.exec():
                new_tok = dlg.get_token()
                save({"hf_token": new_tok})
                self.state["hf_token"] = new_tok
                cfg = self.state["gen_config"]
                from dataclasses import replace
                new_cfg = GenConfig(
                    model_key=cfg.model_key, width=cfg.width, height=cfg.height,
                    steps=cfg.steps, cfg=cfg.cfg, seed=cfg.seed, hf_token=new_tok,
                )
                self.state["gen_config"] = new_cfg
                self.err.hide(); self.bar.setValue(0)
                self.status.setText("Retrying with new token…")
                self.cancel.setEnabled(True); self._start_worker(self._prompts, new_cfg)
                return

        self.err.setText(msg); self.err.show()
        self.cancel.setText("← Back"); self.cancel.setEnabled(True)
        try: self.cancel.clicked.disconnect()
        except Exception: pass
        self.cancel.clicked.connect(self.on_back)

    def _cancel(self):
        if self._worker: self._worker.stop(); self._worker.quit()
        self.on_back()
