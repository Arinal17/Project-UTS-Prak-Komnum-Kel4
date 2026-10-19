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
# 1) pengguna mengetik "." / "," tepat setelah superscript -> kembalikan ke bentuk ketikan
    text = re.sub(rf"({_SUP_RUN})(?={_FRACTION_AHEAD})",
                  lambda m: "**" + m.group(1).translate(_FROM_SUP), text)
    # 2) digit baru setelah superscript digabung menjadi satu pangkat
    text = re.sub(rf"({_SUP_RUN})(\d+)(?!\d)(?!{_FRACTION_AHEAD})",
                  lambda m: (m.group(1) + m.group(2)).translate(_TO_SUP), text)
    # 3) "**n" atau "^n" (n bulat, boleh negatif) -> superscript
    text = re.sub(rf"\s*(?:\*\*|\^)\s*(-?\d+)(?!\d)(?!{_FRACTION_AHEAD})",
                  lambda m: m.group(1).translate(_TO_SUP), text)
    return text


def _superscripts_to_python(text: str) -> str:
    """Kebalikannya, untuk parser: "x²" -> "x**2", "x⁻²" -> "x**(-2)"."""
    def repl(m):
        digits = m.group(0).translate(_FROM_SUP)
        return f"**({digits})" if digits.startswith("-") else f"**{digits}"
    return re.sub(_SUP_RUN, repl, text)


def _normalize_function_text(text: str) -> str:
    """Rapikan teks fungsi: huruf kecil, simbol unicode, koma desimal."""
    s = text.strip().lower()
    s = _superscripts_to_python(s)                    
    for old, new in {"−": "-", "–": "-", "×": "*", "÷": "/"}.items():
        s = s.replace(old, new)
    # "0,5x" -> "0.5x" (koma di antara dua digit dianggap koma desimal)
    s = re.sub(r"(?<=\d),(?=\d)", ".", s)
    return s


@dataclass
class ParsedFunction:
    """Hasil parsing fungsi: ekspresi SymPy + fungsi skalar + fungsi vektor."""
    expr: sp.Expr
    scalar: Callable[[float], float]                # untuk perhitungan bisangatseksi
    vector: Callable[[np.ndarray], np.ndarray]      # untuk menggambar grafik gacor
    display: str                                    # teks fungsi untuk legends never die


def parse_function(text: str) -> ParsedFunction:
    """Ubah teks seperti 'x**2 - 2x + 1' menjadi objek ParsedFunction."""
    if not text or not text.strip():
        raise InputError("Fungsi F(X) belum diisi.")

    s = _normalize_function_text(text)
    hint = "Contoh penulisan yang benar: x**2 - 5x + 4  atau  sin(x) - x/2"   
    if not _ALLOWED_CHARS.match(s):
        raise InputError("Fungsi mengandung karakter yang tidak diizinkan.\n" + hint)

    try:
        expr = parse_expr(s, local_dict=dict(_LOCALS), global_dict=dict(_GLOBALS),
                          transformations=_TRANSFORMS)
    except Exception:
        raise InputError("Penulisan fungsi tidak valid.\n" + hint)

    if not isinstance(expr, sp.Expr):
        raise InputError("Fungsi tidak valid.\n" + hint)
    if not expr.free_symbols <= {_X}:
        raise InputError("Fungsi hanya boleh memakai variabel x.\n" + hint)

    raw_scalar = sp.lambdify(_X, expr, modules="math")
    raw_vector = sp.lambdify(_X, expr, modules="numpy")

    def scalar(x: float) -> float:
        try:
            val = float(raw_scalar(x))
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):
            raise InputError(f"f(x) tidak terdefinisi (bukan bilangan real) di x = {x:g}.")
        if not math.isfinite(val):
            raise InputError(f"f(x) bernilai tak hingga / tidak terdefinisi di x = {x:g}.")
        return val

    def vector(xs: np.ndarray) -> np.ndarray:
        # Untuk grafik: titik yang tidak terdefinisi menjadi NaN (kurva terputus).
        with np.errstate(all="ignore"):
            try:
                ys = np.asarray(raw_vector(xs), dtype=float)
                if ys.ndim == 0:
                    ys = np.full_like(xs, float(ys), dtype=float)
            except Exception:
                ys = np.full_like(xs, np.nan, dtype=float)
                for i, xv in enumerate(xs):
                    try:
                        ys[i] = scalar(float(xv))
                    except InputError:
                        pass
        ys[~np.isfinite(ys)] = np.nan
        return ys

    # teks legend = teks yang klen ketik (urutan suku tidak
    # ditukar seperti hasil SymPy), dengan pangkat ditulis superscript tanpa "^".
    display = superscript_exponents(text.strip())
    return ParsedFunction(expr, scalar, vector, display)


# ==========================================================================
# 2. VALIDASI INPUT
# ==========================================================================
def parse_number(text: str, label: str) -> float:
    """Ubah teks ('0,0001', '2', '1e-4') menjadi float; koma dianggap desimal."""
    t = (text or "").strip().replace(",", ".")
    if not t:
        raise InputError(f"{label} belum diisi.")
    try:
        val = float(t)
    except ValueError:
        raise InputError(f"{label} harus berupa angka.")
    if not math.isfinite(val):
        raise InputError(f"{label} harus berupa angka yang valid.")
    return val


def parse_integer(text: str, label: str) -> int:
    val = parse_number(text, label)
    if val != int(val):
        raise InputError(f"{label} harus berupa bilangan bulat.")
    return int(val)


@dataclass
class SolverInputs:
    """Semua input yang sudah tervalidasi."""
    function: ParsedFunction
    a: float
    b: float
    eps: float
    n_max: int
    decimals: int


def parse_inputs(function: str, a: str, b: str, eps: str, n: str, decimals: str) -> SolverInputs:
    """Validasi seluruh isian form; lempar InputError bila ada yang salah."""
    func = parse_function(function)
    a_val = parse_number(a, "Batas Bawah (a)")
    b_val = parse_number(b, "Batas Atas (b)")
    eps_val = parse_number(eps, "Nilai Galat (ε)")
    n_val = parse_integer(n, "Iterasi Maksimum (N)")
    dec_val = parse_integer(decimals, "Jumlah Angka Desimal")

    if a_val >= b_val:
        raise InputError("Batas Bawah (a) harus lebih kecil dari Batas Atas (b).")
    if eps_val <= 0:
        raise InputError("Nilai Galat (ε) harus lebih besar dari 0.")
    if not 1 <= n_val <= MAX_ITERATIONS:
        raise InputError(f"Iterasi Maksimum (N) harus antara 1 dan {MAX_ITERATIONS}.")
    if not 1 <= dec_val <= MAX_DECIMALS:
        raise InputError(f"Jumlah Angka Desimal harus antara 1 dan {MAX_DECIMALS}.")
    return SolverInputs(func, a_val, b_val, eps_val, n_val, dec_val)


# ==========================================================================
# 3. ALGORITMA BISEKSI
# ==========================================================================
@dataclass
class IterationRow:
    r: int          # nomor iterasi
    a: float
    b: float
    fa: float
    fb: float
