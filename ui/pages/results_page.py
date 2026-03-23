"""Results page — Stage 5."""
import shutil
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QFileDialog, QDialog, QDialogButtonBox,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices


class ImgCard(QFrame):
    def __init__(self, path, label, parent=None):
        super().__init__(parent)
        self.path = path; self.setObjectName("result_card")
        self.setCursor(Qt.CursorShape.PointingHandCursor); self.setFixedWidth(268)
        lay = QVBoxLayout(self); lay.setContentsMargins(7,7,7,9); lay.setSpacing(7)
        self.pix = QLabel()
        self.pix.setPixmap(QPixmap(path).scaled(254,254,
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.pix.setAlignment(Qt.AlignmentFlag.AlignCenter); self.pix.setFixedHeight(254)
        lay.addWidget(self.pix)
        lay.addWidget(QLabel(label, objectName="result_lbl",
                             alignment=Qt.AlignmentFlag.AlignCenter))
        br = QHBoxLayout()
        ob = QPushButton("Open"); ob.setObjectName("btn_micro")
        ob.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(path)))
        sb = QPushButton("Save As…"); sb.setObjectName("btn_micro")
        sb.clicked.connect(self._save)
        br.addWidget(ob); br.addWidget(sb); lay.addLayout(br)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton: self._preview()

    def _preview(self):
        d = QDialog(self); d.setWindowTitle("Preview"); d.resize(880,880)
        lay = QVBoxLayout(d)
        lbl = QLabel()
        lbl.setPixmap(QPixmap(self.path).scaled(860,860,
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); lay.addWidget(lbl)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btns.rejected.connect(d.reject); lay.addWidget(btns); d.exec()

    def _save(self):
        dst, _ = QFileDialog.getSaveFileName(self, "Save", Path(self.path).name,
                                              "PNG (*.png);;JPEG (*.jpg)")
        if dst: shutil.copy2(self.path, dst)


class ResultsPage(QWidget):
    def __init__(self, state, on_restart, parent=None):
        super().__init__(parent)
        self.state      = state
        self.on_restart = on_restart
        self._build()

    def _build(self):
        out = QVBoxLayout(self); out.setContentsMargins(56,32,56,32); out.setSpacing(0)
        out.addWidget(QLabel("Results", objectName="page_title"))
        out.addSpacing(5)
        self.sub = QLabel(""); self.sub.setObjectName("page_sub"); out.addWidget(self.sub)
        out.addSpacing(18)

        sc = QScrollArea(); sc.setObjectName("live_scroll"); sc.setWidgetResizable(True)
        self.gal = QWidget(); self.gl = QVBoxLayout(self.gal)
        self.gl.setContentsMargins(0,0,0,0); self.gl.setSpacing(24)
        sc.setWidget(self.gal); out.addWidget(sc, 1); out.addSpacing(18)

        nav = QHBoxLayout()
        rb = QPushButton("⟳  New Generation"); rb.setObjectName("btn_secondary")
        rb.clicked.connect(self.on_restart); nav.addWidget(rb); nav.addStretch()
        sa = QPushButton("Save All…"); sa.setObjectName("btn_secondary")
        sa.clicked.connect(self._save_all); nav.addWidget(sa)
        od = QPushButton("Open Output Folder"); od.setObjectName("btn_primary")
        od.clicked.connect(self._open_dir); nav.addWidget(od); out.addLayout(nav)

    def refresh(self):
        while self.gl.count():
            item = self.gl.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        paths    = self.state.get("generated_image_paths", [])
        imgs     = self.state.get("generated_images", {})
        collage  = self.state.get("collage_path")
        theme_id = self.state.get("selected_theme", "")
        self.sub.setText(
            f"{len(paths)} image{'s' if len(paths)!=1 else ''}  "
            f"{'+ collage  ' if collage else ''}·  "
            f"Theme: {theme_id.replace('_',' ').title()}"
        )

        if paths:
            lbl = QLabel("INDIVIDUAL SHOTS", objectName="section_lbl")
            self.gl.addWidget(lbl)
            row = QHBoxLayout(); row.setSpacing(14)
            row.setAlignment(Qt.AlignmentFlag.AlignLeft)
            for label, fp in (imgs.items() if imgs else
                               {f"Shot {i+1}": p for i,p in enumerate(paths)}.items()):
                if Path(fp).exists(): row.addWidget(ImgCard(fp, label))
            row.addStretch()
            rw = QWidget(); rw.setLayout(row); self.gl.addWidget(rw)

        if collage and Path(collage).exists():
            cf = QFrame(); cf.setObjectName("collage_card")
            cl = QVBoxLayout(cf); cl.setContentsMargins(12,12,12,14); cl.setSpacing(10)
            cl.addWidget(QLabel("▦  COLLAGE", objectName="collage_tag"))
            pix = QLabel()
            pix.setPixmap(QPixmap(collage).scaled(680,380,
                Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            pix.setAlignment(Qt.AlignmentFlag.AlignCenter); cl.addWidget(pix)
            br = QHBoxLayout()
            ob = QPushButton("Open Full Size"); ob.setObjectName("btn_secondary")
            ob.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(collage)))
            sb = QPushButton("Save Collage As…"); sb.setObjectName("btn_secondary")
            sb.clicked.connect(lambda: self._save_one(collage, "collage.png"))
            br.addWidget(ob); br.addWidget(sb); br.addStretch(); cl.addLayout(br)
            self.gl.addWidget(cf)

        self.gl.addStretch()

    def _save_all(self):
        dst = QFileDialog.getExistingDirectory(self, "Choose Destination")
        if not dst: return
        for p in self.state.get("generated_image_paths", []):
            if Path(p).exists(): shutil.copy2(p, dst)
        cp = self.state.get("collage_path")
        if cp and Path(cp).exists(): shutil.copy2(cp, dst)

    def _save_one(self, src, default_name):
        dst, _ = QFileDialog.getSaveFileName(self, "Save", default_name, "PNG (*.png)")
        if dst: shutil.copy2(src, dst)

    def _open_dir(self):
        from backend.config import OUTPUTS_DIR
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(OUTPUTS_DIR)))
