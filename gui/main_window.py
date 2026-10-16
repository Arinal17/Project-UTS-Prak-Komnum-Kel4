"""
gui/main_window.py
==================
Jendela utama desktop: header (toggle tema, judul, kredit), tata letak 3 kolom,
dan penghubung (controller) antara panel-panel GUI dengan backend.

Tata letak:
  [Panel Input] | [Hasil Perhitungan ] | [Grafik Fungsi]
                | [Tabel Iterasi      ] |
"""

from __future__ import annotations

import math

from PyQt6.QtCore import QPointF, QSize, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import (
    QGraphicsDropShadowEffect, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from backend.bisection_solver import InputError, parse_inputs, solve, summarize
from gui.graph_panel import GraphPanel
from gui.input_panel import InputPanel
from gui.result_panel import ResultPanel
from gui.table_panel import TablePanel
from gui.theme import DARK, LIGHT, build_stylesheet


class ThemeToggleButton(QPushButton):
    """Tombol ikon: bulan (saat Mode Terang) / matahari (saat Mode Gelap)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("themeToggle")
        self.setFixedSize(QSize(44, 44))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Ganti mode terang / gelap")
        self._dark = False
        self._color = QColor("#000000")

    def set_mode(self, dark: bool, icon_color: str) -> None:
        self._dark = dark
        self._color = QColor(icon_color)
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(44, 44)

def paintEvent(self, event) -> None:            # ikon digambar manual (tanpa file gambar)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = QPointF(self.width() / 2, self.height() / 2)
        r = 13.0
        if not self._dark:
            # BULAN = lingkaran dikurangi lingkaran lain yang bergeser
            outer = QPainterPath()
            outer.addEllipse(c, r, r)
            cut = QPainterPath()
            cut.addEllipse(QPointF(c.x() + r * 0.55, c.y() - r * 0.35), r * 0.85, r * 0.85)
            p.fillPath(outer.subtracted(cut), self._color)
        else:
            # MATAHARI = lingkaran kecil + 8 sinar
            pen = QPen(self._color, 2.2)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(c, r * 0.5, r * 0.5)
            for i in range(8):
                ang = i * math.pi / 4
                p1 = QPointF(c.x() + math.cos(ang) * r * 0.78, c.y() + math.sin(ang) * r * 0.78)
                p2 = QPointF(c.x() + math.cos(ang) * r * 1.05, c.y() + math.sin(ang) * r * 1.05)
                p.drawLine(p1, p2)
        p.end()


def _add_shadow(widget: QWidget) -> None:
    """Bayangan lembut di bawah kartu."""
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(26)
    effect.setOffset(0, 6)
    effect.setColor(QColor(0, 0, 0, 60))
    widget.setGraphicsEffect(effect)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Metode Biseksi")
        self.resize(1440, 900)
        self.setMinimumSize(1150, 720)
        self._theme = LIGHT

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 8, 14, 18)
        root.setSpacing(10)