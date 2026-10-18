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
        self.fig = figure
        self.theme = theme
        self.ax = self.fig.add_subplot(111)
        self._home: Tuple[Tuple[float, float], Tuple[float, float]] = (EMPTY_XLIM, EMPTY_YLIM)
        self._drag: Optional[dict] = None
        self._state: Optional[dict] = None      # data hasil terakhir (untuk ganti tema)
        self._fn = None                          # [PERUBAHAN 3] fungsi vektor f(x) yang sedang digambar
        self._line: Optional[Line2D] = None      # [PERUBAHAN 3] objek garis kurva

        # [PERUBAHAN 3] area plot dibuat hampir memenuhi canvas (margin dikecilkan)
        self.fig.subplots_adjust(left=0.085, right=0.985, top=0.985, bottom=0.14)
        canvas = self.fig.canvas
        canvas.mpl_connect("scroll_event", self._on_scroll)
        canvas.mpl_connect("button_press_event", self._on_press)
        canvas.mpl_connect("motion_notify_event", self._on_motion)
        canvas.mpl_connect("button_release_event", self._on_release)
        self.clear()

    # ------------------------------------------------------------------ API
    def set_theme(self, theme) -> None:
        """Ganti tema lalu gambar ulang kondisi terakhir (posisi zoom/geser dipertahankan)."""
        self.theme = theme
        if self._state is None:
            self.clear()
            return
        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
        self.plot(**self._state)
        self.ax.set_xlim(*xlim)                  # [PERUBAHAN 3] jangan reset zoom saat ganti tema
        self.ax.set_ylim(*ylim)
        self._finish()

    def clear(self) -> None:
        """Kembali ke grid kosong awal."""
        self._state = None
        self._fn = None                          # [PERUBAHAN 3]
        self._line = None                        # [PERUBAHAN 3]
        self._reset_axes()
        self.ax.set_xlim(*EMPTY_XLIM)
        self.ax.set_ylim(*EMPTY_YLIM)
        self._home = (EMPTY_XLIM, EMPTY_YLIM)
        self._finish()

    def plot(self, function: ParsedFunction, a: float, b: float,
             root: float, f_root: float, decimals: int) -> None:
        """Gambar kurva f(x), interval [a, b], dan titik akar."""
