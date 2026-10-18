"""
gui/table_panel.py
==================
Panel TENGAH-BAWAH: "Tabel Iterasi" + tombol [Tampilkan Semua] / [Sembunyikan].

Aturan tampilan:
  - Default : baris r = 1 sampai baris TRUE pertama (baris solusi, disorot).
  - Klik [Tampilkan Semua] : seluruh iterasi sampai N, tombol menjadi [Sembunyikan].
  - Bila TRUE tidak ditemukan dalam N iterasi : semua baris sudah tampil,
    baris terakhir (N) disorot sebagai baris solusi, tombol non-aktif.
  - Tabel dapat di-scroll bila barisnya melebihi tinggi area tampilan.

[PERUBAHAN 1] Bila baris yang tampil <= 15 (dan tidak ada baris lagi di bawahnya),
tabel DIPOTONG: tidak ada baris kosong pengisi, tinggi tabel & kartu menyesuaikan
jumlah baris. Panel memberi tahu jendela utama lewat sinyal `trim_changed`.
"""

from __future__ import annotations

from typing import List, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QAbstractItemView, QFrame, QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QVBoxLayout,
)

from backend.bisection_solver import BisectionResult, IterationRow, format_number
from gui.theme import LIGHT

HEADERS = ["r", "a", "b", "f(a)", "f(b)", "xr", "|b - a|", "validasi"]
ROW_HEIGHT = 24

# [PERUBAHAN 1] konstanta untuk fitur "potong tabel"
TRIM_MAX_ROWS = 15                  # batas jumlah baris agar tabel dipotong
CARD_MARGINS = (24, 16, 24, 22)     # kiri, atas, kanan, bawah (dipakai juga untuk hitung tinggi kartu)
CARD_SPACING = 8
QWIDGETSIZE_MAX = 16777215          # "tanpa batas" tinggi maksimum widget Qt


class TablePanel(QFrame):
    trim_changed = pyqtSignal(bool)     # True bila tabel sedang dipotong

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self._theme = LIGHT
        self._result: Optional[BisectionResult] = None
        self._show_all = False
        self._filled_rows = 0
        self._trimmed = False           

        # font monospace untuk isi tabel
        self._mono = QFont()
        self._mono.setFamilies(["Consolas", "Menlo", "DejaVu Sans Mono", "Courier New"])
        self._mono.setStyleHint(QFont.StyleHint.Monospace)
        self._mono.setPointSize(10)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(*CARD_MARGINS)      # pakai konstanta
        layout.setSpacing(CARD_SPACING)

        # --- baris judul + tombol di kanan atas ---
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        self._title = QLabel("Tabel Iterasi")         #  disimpan untuk hitung tinggi
        self._title.setObjectName("cardTitle")
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_toggle = QPushButton("Tampilkan Semua")
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setMinimumWidth(130)
        self.btn_toggle.setEnabled(False)
        self.btn_toggle.clicked.connect(self._toggle_show_all)
        # spacer kiri selebar tombol supaya judul tetap benar-benar di tengah
        spacer = QLabel()
        spacer.setFixedWidth(130)
        top.addWidget(spacer)
        top.addWidget(self._title, 1)
        top.addWidget(self.btn_toggle)
