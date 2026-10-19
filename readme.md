# Metode Biseksi — Kalkulator Akar Persamaan Non-Linier

Aplikasi desktop (GUI) berbahasa Python untuk mencari **akar persamaan non-linier** dengan **Metode Biseksi**.
Cukup masukkan fungsi dan interval, lalu aplikasi menampilkan **hasil akar**, **tabel iterasi**, dan **grafik fungsi** secara otomatis.

> **Project Biseksi — Praktikum Komputasi Numerik**
> Kelompok 4

---

## Daftar Isi

1. [Apa itu Metode Biseksi?](#1-apa-itu-metode-biseksi)
2. [Fitur Aplikasi](#2-fitur-aplikasi)
3. [Source yang Diperlukan](#3-source-yang-diperlukan)
4. [Cara Instalasi & Menjalankan](#4-cara-instalasi--menjalankan)
5. [Tata Cara Penggunaan](#5-tata-cara-penggunaan)
6. [Contoh Input dan Output](#6-contoh-input-dan-output)
7. [Cara Membaca Hasil](#7-cara-membaca-hasil)
8. [Struktur Proyek](#8-struktur-proyek)
9. [Pemecahan Masalah](#9-pemecahan-masalah)
10. [Anggota Kelompok 4](#10-anggota-kelompok-4)

---

## 1. Apa itu Metode Biseksi?

Metode Biseksi adalah metode numerik untuk mencari perkiraan akar dari persamaan non-linier, yaitu nilai **x** yang membuat **f(x) = 0**.

Caranya: interval **[a, b]** dibagi dua di titik tengah, lalu dipilih bagian yang masih mengandung akar. Langkah ini diulang sampai interval cukup kecil sesuai tingkat ketelitian (galat) yang diinginkan.

**Algoritma yang dipakai:**

1. Tentukan fungsi f(x), batas bawah **a**, batas atas **b**, galat **ε**, dan iterasi maksimum **N**.
2. Hitung f(a) dan f(b). Jika **f(a) · f(b) > 0**, interval belum mengandung akar → proses berhenti.
3. Hitung titik tengah: **xr = (a + b) / 2**, lalu hitung f(xr).
4. Pilih bagian yang masih mengandung akar:
   - jika **f(xr) · f(a) < 0** → akar di kiri, maka **b = xr**
   - jika tidak → akar di kanan, maka **a = xr**
5. Jika **|b − a| < ε** atau iterasi sudah mencapai **N**, proses berhenti dan akar = **xr**. Jika belum, ulangi dari langkah 3.

---

## 2. Fitur Aplikasi

- **Kalkulator khusus Metode Biseksi** dengan 6 isian: fungsi, batas bawah, batas atas, galat, iterasi maksimum, dan jumlah angka desimal.
- **Tabel iterasi** berisi kolom `r`, `a`, `b`, `f(a)`, `f(b)`, `xr`, `|b - a|`, dan `validasi`. Tabel bisa di-scroll, dan tombol **Tampilkan Semua / Sembunyikan** mengatur banyaknya baris yang tampil.
- **Grafik fungsi** dengan titik merah penanda akar. Grafik bisa di-zoom (scroll mouse), digeser (drag), dan di-reset (klik ganda), dan kurvanya terus menyambung ke arah x yang jauh.
- **Hasil perhitungan**: akar (xr), f(xr), nomor iterasi, dan kesimpulan dalam satu kalimat.
- **Mode Terang dan Mode Gelap** (tombol bulan/matahari di kiri atas).
- **Pangkat otomatis jadi superscript**: mengetik `x**2` langsung menjadi `x²`.
- **Pengaturan angka desimal** (1–4 angka). Angka yang sangat kecil otomatis ditampilkan dalam notasi ilmiah, misalnya `4,5776E-05`.
- **Validasi input**: pesan peringatan yang jelas jika ada isian yang salah.

---

## 3. Source yang Diperlukan

| Kebutuhan | Versi yang disarankan | Fungsi |
|---|---|---|
| **Python** | 3.9 atau lebih baru | Bahasa pemrograman utama |
| **PyQt6** | 6.4 atau lebih baru | Tampilan antarmuka (GUI) |
| **Matplotlib** | 3.7 atau lebih baru | Menggambar grafik fungsi |
| **NumPy** | 1.24 atau lebih baru | Perhitungan titik-titik grafik |
| **SymPy** | 1.12 atau lebih baru | Membaca dan menghitung fungsi f(x) yang diketik |

Semua library di atas sudah tercatat di file `requirements.txt` dan bisa dipasang sekaligus (lihat bagian berikutnya).
Python dapat diunduh di <https://www.python.org/downloads/>. Saat memasang di Windows, centang **"Add Python to PATH"**.

---

## 4. Cara Instalasi & Menjalankan

**Langkah 1 — Buka terminal / Command Prompt di folder proyek**

```
cd metode_biseksi
```

**Langkah 2 — Pasang semua library yang dibutuhkan**

```
pip install -r requirements.txt
```

Atau pasang satu per satu:

```
pip install PyQt6 matplotlib numpy sympy
```

**Langkah 3 — Jalankan aplikasi**

```
python main.py
```

> Pengguna Windows yang perintah `python` / `pip`-nya tidak dikenali dapat memakai `py main.py` dan `py -m pip install -r requirements.txt`.

Jendela **Metode Biseksi** akan terbuka.

---

## 5. Tata Cara Penggunaan

### Langkah singkat

1. Isi semua kolom di **Panel Input** (sebelah kiri).
2. Klik **Hitung Akar** (atau tekan `Enter`).
3. Lihat hasilnya: **Hasil Perhitungan** dan **Tabel Iterasi** di tengah, serta **Grafik Fungsi** di kanan.
4. Klik **Reset** untuk mengosongkan semuanya dan mulai dari awal.

### Penjelasan setiap kolom input

| Kolom | Isi | Contoh | Ketentuan |
|---|---|---|---|
| **Fungsi F(X)** | Persamaan yang dicari akarnya | `x**2 - 5x + 4` | Gunakan variabel **x** |
| **Batas Bawah (a)** | Ujung kiri interval | `2` | Harus lebih kecil dari b |
| **Batas Atas (b)** | Ujung kanan interval | `5` | Harus lebih besar dari a |
| **Nilai Galat (ε)** | Tingkat ketelitian | `0,0001` | Lebih besar dari 0 |
| **Iterasi Maksimum (N)** | Batas jumlah iterasi | `20` | Bilangan bulat 1–100 |
| **Jumlah Angka Desimal** | Angka di belakang koma pada tampilan | `4` | Bilangan bulat 1–4 |

Pemisah desimal boleh koma (`0,0001`) atau titik (`0.0001`).

### Aturan penulisan fungsi

| Yang ingin ditulis | Cara mengetik | Keterangan |
|---|---|---|
| Perkalian | `2*x` atau `2x` | Tanda `*` boleh dihilangkan di depan x |
| Pembagian | `x/2` | |
| Pangkat | `x**2` atau `x^2` | Otomatis tampil sebagai `x²` |
| Pangkat negatif | `x**-2` | Tampil sebagai `x⁻²` |
| Pangkat pecahan | `x**(1/2)` | Tetap tampil seperti yang diketik |
| Akar kuadrat | `sqrt(x)` | |
| Trigonometri | `sin(x)`, `cos(x)`, `tan(x)` | x dalam **radian** |
| Eksponen / logaritma | `exp(x)`, `ln(x)`, `log10(x)` | `ln` dan `log` sama-sama logaritma natural |
| Nilai mutlak | `abs(x)` | |
| Konstanta | `pi`, `e` | |

Contoh fungsi yang valid: `x**3 - x - 2`, `sin(x) - x/2`, `exp(x) - 3`, `2(x+1) - 5`.

### Tombol-tombol

- **Hitung Akar**: aktif setelah semua kolom terisi.
- **Reset**: mengosongkan input, hasil, tabel, dan grafik.
- **Tampilkan Semua / Sembunyikan**: menampilkan seluruh iterasi sampai N, atau kembali ke tampilan ringkas.
- **Ikon bulan / matahari** (kiri atas): ganti Mode Terang / Mode Gelap.

### Tips memilih interval [a, b]

Interval harus **mengapit akar**, yaitu f(a) dan f(b) harus berlawanan tanda (satu positif, satu negatif). Jika ragu, coba beberapa nilai x dan lihat tandanya, atau perhatikan grafik di mana kurva memotong sumbu-x.

---

## 6. Contoh Input dan Output

### Contoh 1 — Akar ditemukan sebelum iterasi maksimum

**Input**

| Kolom | Isi |
|---|---|
| Fungsi F(X) | `x**2 - 5x + 4` (tampil `x² - 5x + 4`) |
| Batas Bawah (a) | `2` |
| Batas Atas (b) | `5` |
| Nilai Galat (ε) | `0,0001` |
| Iterasi Maksimum (N) | `20` |
| Jumlah Angka Desimal | `4` |

**Output — Hasil Perhitungan**

```
Akar (xr)   : 4,0000
f(xr)       : 4,5777E-05
Iterasi     : 16
Kesimpulan  : Akar fungsi berhasil ditemukan pada iterasi ke-16 dengan nilai xr = 4,0000 dan galat < 0,0001.
```

**Output — Tabel Iterasi** (cuplikan; baris 16 disorot sebagai baris solusi)

| r | a | b | f(a) | f(b) | xr | \|b - a\| | validasi |
|---|---|---|---|---|---|---|---|
| 1 | 2,0000 | 5,0000 | -2,0000 | 4,0000 | 3,5000 | 3,0000 | FALSE |
| 2 | 3,5000 | 5,0000 | -1,2500 | 4,0000 | 4,2500 | 1,5000 | FALSE |
| 3 | 3,5000 | 4,2500 | -1,2500 | 0,8125 | 3,8750 | 0,7500 | FALSE |
| … | … | … | … | … | … | … | … |
| 14 | 3,9999 | 4,0002 | -0,0004 | 0,0007 | 4,0001 | 0,0004 | FALSE |
| 15 | 3,9999 | 4,0001 | -0,0004 | 0,0002 | 4,0000 | 0,0002 | FALSE |
| **16** | **4,0000** | **4,0001** | **-0,0001** | **0,0002** | **4,0000** | **0,0001** | **TRUE** |

**Output — Grafik:** kurva parabola memotong sumbu-x di x = 1 dan x = 4. Titik merah ada di x = 4 dengan label akar `Akar = 4,0000`. Perhatikan bahwa akar yang ditemukan adalah akar di dalam interval [2, 5], yaitu x = 4, bukan x = 1.

> Klik **Tampilkan Semua** untuk melihat iterasi 17–20 (semuanya bernilai TRUE, dengan `|b - a|` yang terus mengecil, misalnya `4,5776E-05`).

---

### Contoh 2 — Iterasi maksimum tercapai sebelum galat terpenuhi

Input sama seperti Contoh 1, tetapi **Iterasi Maksimum (N) = `10`**.

**Output — Hasil Perhitungan**

```
Akar (xr)   : 4,0010
f(xr)       : 0,0029
Iterasi     : 10
Kesimpulan  : Peringatan: iterasi maksimum (N = 10) tercapai sebelum galat < 0,0001 terpenuhi.
              Akar pendekatan adalah xr = 4,0010 pada iterasi ke-10 dengan |b - a| = 0,0059.
```

Tabel menampilkan iterasi 1–10 dan baris ke-10 disorot sebagai baris solusi. Artinya akar yang didapat masih berupa **pendekatan kasar**. Naikkan nilai N agar hasilnya lebih teliti.

---

### Contoh 3 — Fungsi pangkat tiga

| Kolom | Isi |
|---|---|
| Fungsi F(X) | `x**3 - x - 2` |
| Batas Bawah (a) | `1` |
| Batas Atas (b) | `2` |
| Nilai Galat (ε) | `0,001` |
| Iterasi Maksimum (N) | `20` |
| Jumlah Angka Desimal | `4` |

**Output**

```
Akar (xr)   : 1,5210
f(xr)       : -0,0023
Iterasi     : 11
Kesimpulan  : Akar fungsi berhasil ditemukan pada iterasi ke-11 dengan nilai xr = 1,5210 dan galat < 0,0010.
```

---

### Contoh 4 — Input yang tidak valid

| Kolom | Isi |
|---|---|
| Fungsi F(X) | `x**2 - 4` |
| Batas Bawah (a) | `3` |
| Batas Atas (b) | `5` |

**Output:** muncul kotak peringatan.

```
f(a)·f(b) > 0, sehingga interval [a, b] belum menunjukkan adanya akar.
Silakan ganti nilai Batas Bawah (a) dan Batas Atas (b).
```

Sebabnya, f(3) = 5 dan f(5) = 21 sama-sama positif, sehingga tidak ada akar yang terapit. Coba a = `0` dan b = `3` (dengan ε = `0,001`), maka akar pendekatan x ≈ 2 (`1,9999`) akan ditemukan.

Pesan peringatan lain yang mungkin muncul:

| Kesalahan | Pesan |
|---|---|
| a lebih besar atau sama dengan b | Batas Bawah (a) harus lebih kecil dari Batas Atas (b). |
| N di luar 1–100 | Iterasi Maksimum (N) harus antara 1 dan 100. |
| Desimal di luar 1–4 | Jumlah Angka Desimal harus antara 1 dan 4. |
| Fungsi memakai variabel lain, mis. `y + 1` | Fungsi hanya boleh memakai variabel x. |

---

## 7. Cara Membaca Hasil

**Kolom tabel**

| Kolom | Arti |
|---|---|
| `r` | Nomor iterasi |
| `a`, `b` | Batas kiri dan kanan interval pada iterasi tersebut |
| `f(a)`, `f(b)` | Nilai fungsi di a dan b |
| `xr` | Titik tengah = (a + b) / 2, yaitu perkiraan akar |
| `\|b - a\|` | Lebar interval; makin kecil berarti makin teliti |
| `validasi` | **TRUE** jika `\|b - a\|` sudah lebih kecil dari galat ε (atau f(xr) tepat 0), selain itu **FALSE** |

**Aturan tampilan tabel**

- Secara default tabel berhenti di **baris TRUE pertama**, yang disorot dengan warna biru. Nilai `xr` pada baris itulah akar solusinya.
- Klik **Tampilkan Semua** untuk melihat seluruh iterasi sampai N. Tombolnya berubah menjadi **Sembunyikan**.
- Jika TRUE tidak muncul sampai iterasi N, semua baris ditampilkan dan baris terakhir yang menjadi solusi (muncul pesan peringatan).
- Jika baris yang tampil **15 atau kurang**, tabel dipotong tepat setelah baris terakhir, tanpa baris kosong. Jika lebih dari 15, tabel mengisi ruang dan bisa di-scroll.

**Format angka**

- Koma dipakai sebagai pemisah desimal (`4,0000`).
- Jika sebuah angka tidak nol tetapi terlalu kecil untuk ditampilkan sesuai jumlah desimal (akan tampak `0,0000`), angka itu ditampilkan dalam notasi ilmiah, misalnya `4,5776E-05` yang berarti 0,000045776.

**Grafik**

- **Scroll mouse** untuk zoom, **drag** untuk menggeser, **klik ganda** untuk kembali ke tampilan awal.
- Garis biru adalah kurva f(x), titik merah adalah akar. Teks di bawah grafik menunjukkan fungsi dan nilai akar.

---

## 8. Struktur Proyek

```
metode_biseksi/
├── main.py                    # Titik masuk: menjalankan aplikasi
├── requirements.txt           # Daftar library yang dibutuhkan
├── README.md                  # Dokumen ini
├── backend/
│   ├── __init__.py
│   └── bisection_solver.py    # Logika Metode Biseksi, pembaca fungsi, validasi, format angka
└── gui/
    ├── __init__.py
    ├── main_window.py         # Jendela utama, header, tombol tema, penghubung antar panel
    ├── input_panel.py         # Panel kiri: form input, tombol Hitung & Reset, petunjuk
    ├── result_panel.py        # Panel tengah atas: hasil perhitungan
    ├── table_panel.py         # Panel tengah bawah: tabel iterasi
    ├── graph_panel.py         # Panel kanan: kanvas grafik
    ├── plotter.py             # Penggambar grafik (zoom, geser, kurva)
    └── theme.py               # Warna Mode Terang / Gelap dan gaya tampilan
```

Pemisahan `backend` (perhitungan) dan `gui` (tampilan) membuat logika Metode Biseksi bisa diuji atau dipakai ulang tanpa antarmuka.

---

## 9. Pemecahan Masalah

| Masalah | Penyebab / Solusi |
|---|---|
| `ModuleNotFoundError: No module named 'PyQt6'` | Library belum terpasang. Jalankan `pip install -r requirements.txt`. |
| `'python' is not recognized` (Windows) | Coba `py main.py`, atau pasang ulang Python dengan opsi **Add Python to PATH**. |
| Di Linux muncul error `xcb` / `Could not load the Qt platform plugin` | Pasang dependensi: `sudo apt install libxcb-cursor0` |
| Tombol **Hitung Akar** tidak bisa diklik | Pastikan **keenam kolom** sudah terisi. |
| Muncul pesan "interval belum menunjukkan adanya akar" | f(a) dan f(b) bertanda sama. Ganti a dan b hingga mengapit akar. |
| Akar yang ditemukan bukan akar yang diharapkan | Persamaan bisa punya beberapa akar. Biseksi hanya menemukan **satu akar di dalam interval [a, b]**. Sempitkan interval di sekitar akar yang dituju. |
| Tampil peringatan "iterasi maksimum tercapai" | Naikkan N (maksimal 100) atau perbesar nilai galat ε. |
| Simbol pangkat tampil sebagai kotak kosong | Font sistem tidak mendukung superscript. Fungsi tetap dihitung dengan benar. |

---

## 10. Anggota Kelompok 4

**Project Biseksi — Praktikum Komputasi Numerik**

| No | Nama | NPM |
|---|---|---|
| 1 | Arinal Haq | 250810701100073 |
| 2 | Alief Aqsha | 250810701100063 |
| 3 | Hanif Maulana | 250810701100008 |
| 4 | Abrar Muda | 250810701100080 |
| 5 | Nabil Al Fijar | 250810701100031 |
| 6 | Putroe Zalfa | 250810701100024 |
