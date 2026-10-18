"""
gui/theme.py
============
Design system aplikasi: palet warna Mode Terang & Mode Gelap, serta
penyusun stylesheet Qt (QSS). Semua warna mengikuti spesifikasi.

Catatan: "Opacity 25%" / "75%" pada spesifikasi diwujudkan dengan warna rgba().
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Theme:
    name: str
    # --- umum ---
    bg: str                 # latar belakang aplikasi
    panel: str              # latar kartu/panel
    text: str               # judul & label
    hint: str               # teks petunjuk (opacity 75%)
    # --- form ---
    field_bg: str
    field_border: str
    placeholder_rgba: Tuple[int, int, int, int]   # placeholder (opacity 25%)
    # --- tombol ---
    btn: str
    btn_text: str
    btn_hover: str
    btn_disabled: str       # latar tombol non-aktif (opacity 25%)
    # --- hasil & tabel ---
    root_value: str         # warna angka hasil akar
    header_bg: str
