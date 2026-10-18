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
