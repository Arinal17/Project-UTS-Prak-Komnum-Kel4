"""
gui/plotter.py
==============
Logika penggambaran grafik fungsi dengan Matplotlib.

Sengaja dipisah dari PyQt (hanya memakai objek Figure) agar:
  - graph_panel.py cukup menanamkan Figure ke canvas Qt, dan
  - kode penggambaran bisa diuji tanpa GUI.

Fitur interaktif: scroll mouse = zoom, drag = geser, klik ganda = reset tampilan.

[PERUBAHAN 3] Kurva tidak lagi "terpotong": setiap kali tampilan berubah
(zoom / geser / reset) kurva dihitung ulang untuk rentang x yang sedang terlihat,
sehingga grafik selalu tersambung sampai x -> tak hingga.
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle          # [PERUBAHAN 3] bingkai area plot
from matplotlib.ticker import FuncFormatter

from backend.bisection_solver import ParsedFunction, format_number

# Tampilan awal (grid kosong) sesuai desain
EMPTY_XLIM = (-15.0, 15.0)
EMPTY_YLIM = (-20.0, 20.0)

CURVE_SAMPLES = 1500     # [PERUBAHAN 3] jumlah titik sampel kurva pada rentang x yang terlihat


def _comma_tick(value: float, _pos) -> str:
    """Label sumbu dengan koma sebagai pemisah desimal (mis. 2,5)."""
    text = f"{value:.6g}"
    if text in ("-0", "0"):
        text = "0"
    return text.replace(".", ",")


class BisectionPlotter:
    def __init__(self, figure: Figure, theme) -> None:
