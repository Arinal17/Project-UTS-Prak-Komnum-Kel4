"""
backend/bisection_solver.py
===========================
Logika bisnis (backend) Metode Biseksi.

Modul ini TIDAK bergantung pada GUI sama sekali, sehingga bisa diuji / dipakai
ulang secara terpisah. Isinya:
  1. Parser fungsi f(x) berbasis SymPy (dengan whitelist karakter & nama).
  2. Validasi seluruh input pengguna.
  3. Algoritma biseksi (mengikuti slide algoritma pada materi).
  4. Pemformatan angka (koma desimal + notasi ilmiah otomatis).
  5. Penyusun teks ringkasan / kesimpulan.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Callable, List, Optional

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# --------------------------------------------------------------------------
# Konstanta batas input
# --------------------------------------------------------------------------
MAX_ITERATIONS = 100   # iterasi maksimum yang boleh diinput
MAX_DECIMALS = 4       # jumlah angka desimal maksimum yang boleh diinput


class InputError(ValueError):
    """Dilempar bila input pengguna / evaluasi fungsi tidak valid."""


# ==========================================================================
# 1. PARSER FUNGSI f(x)
# ==========================================================================
_X = sp.Symbol("x")

# Hanya karakter berikut yang boleh muncul di teks fungsi (setelah dinormalkan).
_ALLOWED_CHARS = re.compile(r"^[0-9a-z+\-*/^().,\s]+$")

# Namespace terbatas untuk parse_expr (tanpa __builtins__ => lebih aman).
_GLOBALS = {
    "__builtins__": {},
    # kelas-kelas yang dibutuhkan transformasi SymPy
    "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational,
    "Symbol": sp.Symbol, "Function": sp.Function,
    # fungsi matematika yang diizinkan
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "exp": sp.exp, "log": sp.log, "ln": sp.log,
    "log10": lambda v: sp.log(v, 10),
    "sqrt": sp.sqrt, "abs": sp.Abs,
}
_LOCALS = {"x": _X, "e": sp.E, "pi": sp.pi}

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


# --------------------------------------------------------------------------
# Pangkat dinampakkan sebagai superscript anjay (tanpa tanda ^ / **)
# --------------------------------------------------------------------------
_SUP_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_TO_SUP = str.maketrans("0123456789-", _SUP_DIGITS + "⁻")
_FROM_SUP = str.maketrans(_SUP_DIGITS + "⁻", "0123456789-")
_SUP_RUN = f"⁻?[{_SUP_DIGITS}]+"          # deretan karakter superscript, angka pangkat tu
_FRACTION_AHEAD = r"[.,](?:\d|$)"          # tanda desimal setelah angka (pangkat pecahan, kek 0.5)


def superscript_exponents(text: str) -> str:
    """
    Ubah pangkat bilangan bulat menjadi superscript:
        "x**2 - 5x + 4" -> "x² - 5x + 4"      "x^10" -> "x¹⁰"      "x**-2" -> "x⁻²"
    Dipakai untuk kolom input (diketik langsung berubah) DAN semua tampilan fungsi.

    Aturan khusus:
      - Pangkat pecahan/desimal ("x**0.5", "x**(1/2)") dibiarkan apa adanya, sebab
        tidak ada simbol superscript untuk titik/koma/garis miring.
      - Digit yang diketik tepat setelah superscript digabung ("x¹" + "0" -> "x¹⁰").
      - Fungsi ini aman dipanggil berulang kali (hasilnya stabil).
    """
