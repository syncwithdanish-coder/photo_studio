"""Theme page — Stage 2. Painted shot previews update per theme."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QCheckBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QLinearGradient, QRadialGradient,
    QFont, QPen, QBrush,
)
from prompts.theme_prompts import get_all_themes as all_themes, get_theme

SHOT_STYLES = {
    "shot_a": {"label": "HERO",      "sub": "Front · Studio lit",  "lx": 0.25, "ly": 0.10},
    "shot_b": {"label": "LIFESTYLE", "sub": "3/4 · Natural light", "lx": 0.75, "ly": 0.10},
    "shot_c": {"label": "MACRO",     "sub": "Close-up · Detail",   "lx": 0.50, "ly": 0.30},
    "shot_d": {"label": "FLAT-LAY",  "sub": "Overhead · Styled",   "lx": 0.50, "ly": 0.05},
}


class Canvas(QWidget):
    def __init__(self, shot_id, accent, bg, parent=None):
        super().__init__(parent)
        self.sid    = shot_id
        self.accent = accent
        self.bg     = bg
        self.setFixedHeight(120)

    def set_palette(self, accent, bg):
        self.accent = accent; self.bg = bg; self.update()

    def paintEvent(self, _):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        a  = QColor(self.accent)
        bg = QColor(self.bg)

        # Background
        grad = QLinearGradient(0,0,w,h)
        grad.setColorAt(0, bg.lighter(120)); grad.setColorAt(1, bg)
        p.fillRect(0,0,w,h, QBrush(grad))

        # Glow
        st = SHOT_STYLES.get(self.sid, SHOT_STYLES["shot_a"])
        rg = QRadialGradient(w*st["lx"], h*st["ly"], w*0.7)
        c  = QColor(a); c.setAlpha(55)
        o  = QColor(a); o.setAlpha(0)
        rg.setColorAt(0,c); rg.setColorAt(1,o)
        p.fillRect(0,0,w,h, QBrush(rg))

        # Silhouette
        cx, cy = w//2, int(h*0.46)
        p.setPen(Qt.PenStyle.NoPen)
        sid = self.sid

        if sid == "shot_a":
            p.setBrush(QBrush(QColor(0,0,0,70)))
            p.drawEllipse(cx-22, cy+24, 44, 10)
            bg2 = QLinearGradient(cx-14, cy-28, cx+14, cy+22)
            bg2.setColorAt(0, a.lighter(170)); bg2.setColorAt(1, a.darker(130))
            p.setBrush(QBrush(bg2)); p.drawRoundedRect(cx-14, cy-28, 28, 50, 5, 5)
            hl = QLinearGradient(cx-14, cy-28, cx-8, cy+22)
            hl.setColorAt(0, QColor(255,255,255,60)); hl.setColorAt(1, QColor(255,255,255,0))
            p.setBrush(QBrush(hl)); p.drawRoundedRect(cx-14, cy-28, 7, 50, 3, 3)

        elif sid == "shot_b":
            tg = QLinearGradient(0,cy+8,0,cy+32)
            tg.setColorAt(0, a.darker(200)); tg.setColorAt(1, QColor(0,0,0,0))
            p.setBrush(QBrush(tg)); p.drawRect(0, cy+8, w, 36)
            bg2 = QLinearGradient(cx-12, cy-22, cx+12, cy+10)
            bg2.setColorAt(0, a.lighter(155)); bg2.setColorAt(1, a.darker(125))
            p.setBrush(QBrush(bg2)); p.drawRoundedRect(cx-12, cy-22, 24, 30, 4, 4)
            p.setBrush(QBrush(a.darker(160))); p.drawEllipse(cx-36, cy+2, 14, 8)
            p.drawRoundedRect(cx+26, cy-6, 10, 14, 2, 2)

        elif sid == "shot_c":
            ring = QColor(a); ring.setAlpha(40)
            p.setBrush(QBrush(ring)); p.drawEllipse(cx-32, cy-32, 64, 64)
            cg = QRadialGradient(cx-8, cy-10, 34)
            cg.setColorAt(0, a.lighter(175)); cg.setColorAt(0.6, a); cg.setColorAt(1, a.darker(155))
            p.setBrush(QBrush(cg)); p.drawEllipse(cx-26, cy-26, 52, 52)
            p.setBrush(QBrush(QColor(255,255,255,75))); p.drawEllipse(cx-14, cy-17, 12, 9)
            p.setPen(QPen(QColor(0,0,0,35), 1))
            for i in range(-18, 20, 5): p.drawLine(cx+i, cy-26, cx+i, cy+26)

        elif sid == "shot_d":
            sg = QLinearGradient(0,0,w,h)
            sg.setColorAt(0, a.darker(235)); sg.setColorAt(1, a.darker(270))
            p.setBrush(QBrush(sg)); p.drawRect(0,0,w,h)
            mg = QLinearGradient(cx-18, cy-30, cx+18, cy+30)
            mg.setColorAt(0, a.lighter(155)); mg.setColorAt(1, a)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(mg)); p.drawRoundedRect(cx-18, cy-30, 36, 60, 4, 4)
            p.setBrush(QBrush(a.lighter(118))); p.drawEllipse(cx-46, cy-10, 18, 18)
            p.drawRoundedRect(cx+28, cy-22, 16, 38, 3, 3)
            p.setPen(QPen(QColor(0,0,0,28), 1))
            for i in range(4): p.drawLine(cx-18, cy-22+i*15, cx+18, cy-22+i*15)

        # Label overlay
        fade = QLinearGradient(0, int(h*0.55), 0, h)
        fade.setColorAt(0, QColor(0,0,0,0)); fade.setColorAt(1, QColor(0,0,0,188))
        p.setPen(Qt.PenStyle.NoPen); p.fillRect(0,0,w,h, QBrush(fade))
        p.setPen(QPen(a, 1))
        f = QFont("Segoe UI", 7, QFont.Weight.Bold)
        f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2.5)
        p.setFont(f); p.drawText(7, h-19, st["label"])
        p.setPen(QPen(QColor(255,255,255,100))); p.setFont(QFont("Segoe UI", 6))
        p.drawText(7, h-7, st["sub"])
        p.end()


class ShotCard(QFrame):
    def __init__(self, shot, palette, parent=None):
        super().__init__(parent)
        self.shot = shot; self._pal = palette
        self.setObjectName("shot_card"); self.setFixedWidth(168)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)
        self.canvas = Canvas(shot["id"], palette[0], palette[1])
        lay.addWidget(self.canvas)
        strip = QFrame(); strip.setObjectName("shot_info")
        sl = QVBoxLayout(strip); sl.setContentsMargins(10,7,10,7); sl.setSpacing(3)
        top = QHBoxLayout(); top.setSpacing(6)
        self.chk = QCheckBox(); self.chk.setObjectName("shot_chk"); self.chk.setChecked(True)
        top.addWidget(self.chk)
        name = shot["label"].split("—")[-1].strip() if "—" in shot["label"] else shot["label"]
        top.addWidget(QLabel(name, objectName="shot_card_lbl")); top.addStretch()
        sl.addLayout(top)
        sl.addWidget(QLabel(shot["type"], objectName="shot_card_type"))
        lay.addWidget(strip)

    def set_palette(self, pal):
        self._pal = pal; self.canvas.set_palette(pal[0], pal[1])

    def is_checked(self): return self.chk.isChecked()
    def shot_id(self):    return self.shot["id"]
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton: self.chk.setChecked(not self.chk.isChecked())


class ThemeCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, theme, parent=None):
        super().__init__(parent)
        self.theme = theme; self.setObjectName("theme_card")
        self.setCursor(Qt.CursorShape.PointingHandCursor); self.setFixedHeight(70)
        lay = QHBoxLayout(self); lay.setContentsMargins(14,10,14,10); lay.setSpacing(10)
        lay.addWidget(QLabel(theme["icon"], objectName="theme_icon"))
        txt = QVBoxLayout(); txt.setSpacing(2)
        txt.addWidget(QLabel(theme["name"], objectName="theme_name"))
        txt.addWidget(QLabel(theme["concept"], objectName="theme_info"))
        lay.addLayout(txt, 1)
        lay.addWidget(QLabel(f"{len(theme['shots'])} shots", objectName="shot_badge"))

    def set_sel(self, v):
        self.setObjectName("theme_card_sel" if v else "theme_card")
        self.style().unpolish(self); self.style().polish(self)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton: self.clicked.emit(self.theme["id"])


class ThemePage(QWidget):
    def __init__(self, state, on_next, on_back, parent=None):
        super().__init__(parent)
        self.state   = state
        self.on_next = on_next
        self.on_back = on_back
        self._cards: dict[str, ThemeCard] = {}
        self._shots: list[ShotCard]       = []
        self._build()

    def _build(self):
        out = QVBoxLayout(self); out.setContentsMargins(56,32,56,32); out.setSpacing(0)
        out.addWidget(QLabel("Select Theme & Shots", objectName="page_title"))
        out.addSpacing(4)
        sub = QLabel("Click a theme — the shot previews update to show lighting and style for each angle.")
        sub.setObjectName("page_sub"); sub.setWordWrap(True); out.addWidget(sub)
        out.addSpacing(18)

        body = QHBoxLayout(); body.setSpacing(22)

        # Left: theme list
        lft = QVBoxLayout(); lft.setSpacing(8)
        lft.addWidget(QLabel("ENVIRONMENT", objectName="section_lbl"))

        ts = QScrollArea(); ts.setObjectName("themes_scroll")
        ts.setWidgetResizable(True); ts.setFixedWidth(262)
        ts.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        tc = QWidget(); tl = QVBoxLayout(tc)
        tl.setContentsMargins(0,0,2,0); tl.setSpacing(6)
        for t in all_themes():
            card = ThemeCard(t); card.clicked.connect(self.select)
            self._cards[t["id"]] = card; tl.addWidget(card)
        tl.addStretch(); ts.setWidget(tc); lft.addWidget(ts, 1)
        body.addLayout(lft)

        vd = QFrame(); vd.setFrameShape(QFrame.Shape.VLine); vd.setObjectName("v_div")
        body.addWidget(vd)

        # Right: shot previews
        rgt = QVBoxLayout(); rgt.setSpacing(10)
        hdr = QHBoxLayout()
        self.sec_lbl = QLabel("SHOT PREVIEWS", objectName="section_lbl")
        hdr.addWidget(self.sec_lbl); hdr.addStretch()
        for lbl, val in [("All", True), ("None", False)]:
            b = QPushButton(lbl); b.setObjectName("btn_micro"); b.setFixedHeight(24)
            b.clicked.connect(lambda _, v=val: self._set_all(v))
            hdr.addWidget(b)
        rgt.addLayout(hdr)

        self.concept = QLabel("← Click a theme to preview shots", objectName="theme_concept")
        self.concept.setWordWrap(True); rgt.addWidget(self.concept)

        ss = QScrollArea(); ss.setObjectName("shots_scroll"); ss.setWidgetResizable(True)
        ss.setMinimumHeight(210)
        ss.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sc = QWidget(); self.sl = QHBoxLayout(self.sc)
        self.sl.setContentsMargins(2,2,2,2); self.sl.setSpacing(10)
        self.sl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ss.setWidget(self.sc); rgt.addWidget(ss, 1)

        self.collage_chk = QCheckBox("  Generate a collage combining all selected shots")
        self.collage_chk.setObjectName("collage_chk"); self.collage_chk.setChecked(True)
        rgt.addWidget(self.collage_chk)
        body.addLayout(rgt, 1); out.addLayout(body, 1); out.addSpacing(14)

        nav = QHBoxLayout()
        bk = QPushButton("← Back"); bk.setObjectName("btn_secondary"); bk.clicked.connect(self.on_back)
        nav.addWidget(bk); nav.addStretch()
        self.nxt = QPushButton("Configure Model  →"); self.nxt.setObjectName("btn_primary")
        self.nxt.setEnabled(False); self.nxt.clicked.connect(self._next)
        nav.addWidget(self.nxt); out.addLayout(nav)

    def refresh(self):
        if self.state.get("selected_theme"): self.select(self.state["selected_theme"])

    def select(self, tid: str):
        for k, c in self._cards.items(): c.set_sel(k == tid)
        self.state["selected_theme"] = tid
        theme = get_theme(tid)
        _BG = {"dining":"#2a1e10","kitchen":"#121e1a","living_room":"#201408",
               "alfresco":"#101808","spa":"#0c1818","studio":"#141414","cafe":"#180c04"}
        pal   = (theme.get("color","#c8a96e"), theme.get("bg", _BG.get(tid,"#1a1a1c")))
        self.concept.setText(f"{theme['name']}  ·  {theme['concept']}")
        for c in self._shots: c.deleteLater()
        self._shots.clear()
        while self.sl.count():
            item = self.sl.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for shot in theme["shots"]:
            card = ShotCard(shot, pal); self._shots.append(card); self.sl.addWidget(card)
        self.sl.addStretch()
        self.nxt.setEnabled(True)

    def _set_all(self, v):
        for c in self._shots: c.chk.setChecked(v)

    def _next(self):
        sel = [c.shot_id() for c in self._shots if c.is_checked()]
        if not sel: return
        self.state["selected_shots"]   = sel
        self.state["generate_collage"] = self.collage_chk.isChecked()
        self.on_next()
