"""
gui/input_panel.py
==================
Panel KIRI: form input, tombol [Hitung Akar] & [Reset], dan petunjuk penggunaan.

Aturan tombol:
  - [Hitung Akar]  aktif hanya bila SEMUA isian terisi.
  - [Reset]        aktif bila ada isian atau ada hasil yang bisa dihapus.
  Tombol non-aktif tampil dengan opacity 25% (diatur di theme.py).
"""

from __future__ import annotations

from typing import Dict

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from backend.bisection_solver import superscript_exponents   # [PERUBAHAN 5]

# (kunci, label, placeholder, contoh)
FIELDS = [
    ("function", "Fungsi F(X)", "Masukkan Fungsi F(X)", "Contoh: x**2 - 5x + 4"),   # [PERUBAHAN 4]
    ("a", "Batas Bawah (a)", "Masukkan Nilai Batas Bawah", "Contoh: 2"),
    ("b", "Batas Atas (b)", "Masukkan Nilai Batas Atas", "Contoh: 5"),
    ("eps", "Nilai Galat (ε)", "Masukkan Nilai Galat", "Contoh: 0,0001"),
    ("n", "Iterasi Maksimum (N)", "Masukkan Iterasi Maksimum", "Contoh: 20 (Maks : 100)"),
    ("decimals", "Jumlah Angka Desimal", "Masukkan Jumlah Angka Desimal", "Contoh: 4 (Maks : 4)"),
]

GUIDE = [
    "· Gunakan x untuk variabel dan (*) sebagai perkalian",
    "· Gunakan / untuk pembagian dan (**) untuk pangkat",
    "· Pemisah desimal boleh koma (,) atau titik (.)",
    "· Ketik ** lalu angka, otomatis jadi pangkat (x**2 → x²)",   # [PERUBAHAN 5]
]


class InputPanel(QFrame):
