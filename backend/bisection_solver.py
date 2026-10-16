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