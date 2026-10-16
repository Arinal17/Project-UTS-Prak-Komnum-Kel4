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
    calculate_requested = pyqtSignal()   # tombol Hitung Akar ditekan
    reset_requested = pyqtSignal()       # tombol Reset ditekan

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFixedWidth(292)
        self._has_result = False
        self.edits: Dict[str, QLineEdit] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 24, 22, 22)
        layout.setSpacing(2)

        title = QLabel("PANEL INPUT")
        title.setObjectName("cardTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        # --- field input ---
        for key, label, placeholder, example in FIELDS:
            lab = QLabel(label)
            lab.setObjectName("fieldLabel")
            edit = QLineEdit()
            edit.setPlaceholderText(placeholder)
            edit.textChanged.connect(self.update_buttons)
            edit.returnPressed.connect(self._on_enter)
            hint = QLabel(example)
            hint.setObjectName("hint")
            layout.addWidget(lab)
            layout.addWidget(edit)
            layout.addWidget(hint)
            self.edits[key] = edit
            if key == "function":                                  # [PERUBAHAN 5]
                edit.textChanged.connect(self._auto_superscript)   # ** otomatis jadi pangkat

        # --- tombol aksi (jajar horizontal) ---
        layout.addSpacing(10)
        row = QHBoxLayout()
