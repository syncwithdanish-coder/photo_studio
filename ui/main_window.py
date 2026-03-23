"""Main window."""
import traceback
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QFrame, QMessageBox,
)
from PyQt6.QtCore import Qt

from ui.pages.upload_page   import UploadPage
from ui.pages.theme_page    import ThemePage
from ui.pages.config_page   import ConfigPage
from ui.pages.generate_page import GeneratePage
from ui.pages.results_page  import ResultsPage

STEPS = ["Upload", "Theme", "Configure", "Generate", "Results"]


def crash_box(title, err):
    log = Path.home() / "ProductStudio" / "crash.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"\n=== {title} ===\n{err}\n")
    try:
        mb = QMessageBox(); mb.setIcon(QMessageBox.Icon.Critical)
        mb.setWindowTitle(f"Product Studio — {title}")
        mb.setText(f"{err[:600]}\n\nFull log: {log}")
        mb.exec()
    except Exception:
        pass


class Steps(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        self.setFixedHeight(48); self._lbls = []
        for i, name in enumerate(STEPS):
            if i:
                ln = QFrame(); ln.setFixedSize(36,1); ln.setObjectName("step_conn")
                lay.addWidget(ln)
            l = QLabel(f"  {i+1}  {name}")
            l.setObjectName("step_active" if i==0 else "step_inactive")
            l.setAlignment(Qt.AlignmentFlag.AlignCenter); l.setFixedHeight(34)
            self._lbls.append(l); lay.addWidget(l)

    def set(self, idx):
        for i, l in enumerate(self._lbls):
            l.setObjectName("step_done" if i<idx else "step_active" if i==idx else "step_inactive")
            l.style().unpolish(l); l.style().polish(l)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Studio — AI Image Generator")
        self.setMinimumSize(1100, 760); self.resize(1320, 870)
        self.state = {
            "uploaded_images": [], "product_description": "",
            "selected_theme": None, "selected_shots": [],
            "gen_config": None, "hf_token": "",
            "generated_images": {}, "collage_path": None,
            "generated_image_paths": [],
            "output_dir": str(Path.home() / "ProductStudio" / "outputs"),
        }
        try:
            self._build()
        except Exception:
            crash_box("Startup Error", traceback.format_exc()); raise

    def _build(self):
        root = QWidget(); self.setCentralWidget(root)
        rl = QVBoxLayout(root); rl.setContentsMargins(0,0,0,0); rl.setSpacing(0)

        # Topbar
        tb = QWidget(); tb.setObjectName("topbar"); tb.setFixedHeight(60)
        tbl = QHBoxLayout(tb); tbl.setContentsMargins(24,0,24,0)
        tbl.addWidget(QLabel("PRODUCT STUDIO", objectName="logo_label"))
        tbl.addStretch()
        self.steps = Steps(); tbl.addWidget(self.steps)
        tbl.addStretch()
        tbl.addWidget(QLabel("v2.0  •  Offline+API", objectName="ver_label"))
        rl.addWidget(tb)
        div = QFrame(); div.setFixedHeight(1); div.setObjectName("top_div"); rl.addWidget(div)

        self.stack = QStackedWidget(); rl.addWidget(self.stack)

        for attr, factory in [
            ("upload",   lambda: UploadPage(self.state, self._to_theme)),
            ("theme",    lambda: ThemePage(self.state, self._to_config, self._to_upload)),
            ("config",   lambda: ConfigPage(self.state, self._to_generate, self._to_theme)),
            ("generate", lambda: GeneratePage(self.state, self._to_results, self._to_config)),
            ("results",  lambda: ResultsPage(self.state, self._to_upload)),
        ]:
            try:
                pg = factory(); setattr(self, attr, pg); self.stack.addWidget(pg)
            except Exception:
                crash_box(f"Page Error ({attr})", traceback.format_exc()); raise

        self.stack.setCurrentIndex(0)

    def _to_upload(self):
        self.state["uploaded_images"] = []; self.state["selected_theme"] = None
        self.stack.setCurrentIndex(0); self.steps.set(0)
        try: self.upload.reset()
        except Exception: pass

    def _to_theme(self):
        self.stack.setCurrentIndex(1); self.steps.set(1)
        try: self.theme.refresh()
        except Exception as e: crash_box("Theme Error", traceback.format_exc())

    def _to_config(self):
        self.stack.setCurrentIndex(2); self.steps.set(2)
        try: self.config.refresh()
        except Exception as e: crash_box("Config Error", traceback.format_exc())

    def _to_generate(self):
        self.stack.setCurrentIndex(3); self.steps.set(3)
        try: self.generate.start_generation()
        except Exception as e: crash_box("Generation Error", traceback.format_exc())

    def _to_results(self):
        self.stack.setCurrentIndex(4); self.steps.set(4)
        try: self.results.refresh()
        except Exception as e: crash_box("Results Error", traceback.format_exc())
