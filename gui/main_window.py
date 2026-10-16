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


