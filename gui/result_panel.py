"""
gui/result_panel.py
===================
Panel TENGAH-ATAS: "Hasil Perhitungan"
(Akar xr, f(xr), nomor iterasi saat TRUE ditemukan, dan kesimpulan).
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout

from backend.bisection_solver import ResultSummary


class ResultPanel(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 16, 24, 18)
        outer.setSpacing(6)

        title = QLabel("Hasil Perhitungan")
        title.setObjectName("cardTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)
        grid.setColumnStretch(2, 1)
        outer.addLayout(grid)
