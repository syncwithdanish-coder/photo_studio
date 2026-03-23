#!/usr/bin/env python3
"""Product Studio v2 — Entry point."""
import sys
import os

# ── Silence noisy libraries (must be before any import) ──────────────────────
os.environ["TQDM_DISABLE"]                      = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"]      = "1"
os.environ["TOKENIZERS_PARALLELISM"]            = "false"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["DIFFUSERS_VERBOSITY"]               = "error"
os.environ["PYTHONWARNINGS"]                    = "ignore"

# ── Strip Anaconda from sys.path ──────────────────────────────────────────────
def _clean():
    exe_dir = os.path.dirname(os.path.normcase(sys.executable))
    py_root = os.path.dirname(exe_dir)
    good = set()
    for c in [
        os.path.join(py_root, "Lib",  "site-packages"),
        os.path.join(py_root, "lib",  "site-packages"),
        os.path.join(exe_dir, "Lib",  "site-packages"),  # embedded
        *[os.path.join(py_root, "lib", f"python3.{v}", "site-packages") for v in [9,10,11,12]],
    ]:
        if os.path.isdir(c):
            good.add(os.path.normcase(c))

    sys.path = list(good) + [
        p for p in sys.path
        if not any(x in os.path.normcase(p) for x in ("anaconda","conda","miniconda"))
        and not ("site-packages" in os.path.normcase(p)
                 and not any(os.path.normcase(p).startswith(g) for g in good))
    ]
    for v in ("PYTHONPATH","CONDA_PREFIX","CONDA_DEFAULT_ENV","CONDA_EXE"):
        os.environ.pop(v, None)

_clean()

# ── Project root ──────────────────────────────────────────────────────────────
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# ── Windows Qt DLL fix ────────────────────────────────────────────────────────
if sys.platform == "win32":
    for _sp in sys.path:
        _qt_bin = os.path.join(_sp, "PyQt6", "Qt6", "bin")
        if os.path.isdir(_qt_bin):
            try: os.add_dll_directory(_qt_bin)
            except Exception: pass
            os.environ["PATH"] = _qt_bin + os.pathsep + os.environ.get("PATH", "")
            break

# ── Import Qt ─────────────────────────────────────────────────────────────────
try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
except Exception as e:
    # Write error to file and show Windows dialog
    import traceback
    _err = traceback.format_exc()
    _log = os.path.join(os.path.expanduser("~"), "ProductStudio", "startup_error.txt")
    os.makedirs(os.path.dirname(_log), exist_ok=True)
    open(_log, "w").write(f"PyQt6 failed:\n{e}\n\n{_err}")
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            f"PyQt6 failed to load:\n\n{e}\n\nRun SETUP.bat to fix.\n\nError saved to:\n{_log}",
            "Product Studio — Error", 0x10,
        )
    except Exception:
        pass
    sys.exit(1)

from ui.main_window import MainWindow


def main():
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName("Product Studio")

    _qss = os.path.join(_ROOT, "ui", "style.qss")
    if os.path.exists(_qss):
        try:
            app.setStyleSheet(open(_qss, encoding="utf-8").read())
        except Exception:
            pass

    try:
        win = MainWindow()
        win.show()
    except Exception as e:
        import traceback
        err = traceback.format_exc()
        _log = os.path.join(os.path.expanduser("~"), "ProductStudio", "startup_error.txt")
        open(_log, "w", encoding="utf-8").write(err)
        mb = QMessageBox(); mb.setIcon(QMessageBox.Icon.Critical)
        mb.setWindowTitle("Product Studio — Startup Error")
        mb.setText(f"Failed to start:\n\n{str(e)[:400]}\n\nFull log: {_log}")
        mb.exec()
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
