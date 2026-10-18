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
    header_text: str
    cell_border: str
    row_a: str
    row_b: str
    hl_bg: str              # sorotan baris solusi (TRUE pertama)
    hl_text: str
    toggle_icon: str        # warna ikon toggle mode
    # --- grafik matplotlib ---
    plot_bg: str
    plot_axis: str
    plot_curve: str
    plot_root: str
    plot_label: str


LIGHT = Theme(
    name="light",
    bg="#F8FAFC", panel="#FFFFFF", text="#0F172A", hint="rgba(15, 23, 42, 191)",
    field_bg="#FFFFFF", field_border="#CBD5E1", placeholder_rgba=(0, 0, 0, 64),
    btn="#2563EB", btn_text="#FFFFFF", btn_hover="#1D4ED8", btn_disabled="rgba(37, 99, 235, 64)",
    root_value="#16A34A", header_bg="#F1F5F9", header_text="#0F172A", cell_border="#E2E8F0",
    row_a="#FFFFFF", row_b="#F8FAFC", hl_bg="#DBEAFE", hl_text="#1E40AF",
    toggle_icon="#000000",
    plot_bg="#FFFFFF", plot_axis="#94A3B8", plot_curve="#2563EB",
    plot_root="#DC2626", plot_label="#0F172A",
)

DARK = Theme(
    name="dark",
    bg="#0F172A", panel="#1E293B", text="#F8FAFC", hint="rgba(226, 232, 240, 191)",
    field_bg="#334155", field_border="#475569", placeholder_rgba=(255, 255, 255, 64),
    btn="#2563EB", btn_text="#FFFFFF", btn_hover="#3B82F6", btn_disabled="rgba(37, 99, 235, 64)",
    root_value="#4ADE80", header_bg="#334155", header_text="#F8FAFC", cell_border="#475569",
    row_a="#1E293B", row_b="#0F172A", hl_bg="#1E3A8A", hl_text="#93C5FD",
    toggle_icon="#FFFFFF",
