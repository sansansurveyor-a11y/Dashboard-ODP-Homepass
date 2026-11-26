# Dashboard ODP & Homepass

Dashboard untuk melihat jumlah ODP dan homepass (ODP × port) per segment, dengan filter region dan vendor, rincian per segment, dan unduhan Excel.

Homepass dihitung dari jumlah port semua ODP.

## Isi repositori

| File | Fungsi |
|---|---|
| `index.html` | Halaman dashboard (satu file, tanpa build) |
| `data.json` | Data yang ditampilkan, hasil rangkuman file Excel |
| `build_data.py` | Skrip untuk membuat `data.json` dari file Excel terbaru |

## Memasang sebagai situs (GitHub Pages)

1. Buka repositori di GitHub, lalu **Settings → Pages**.
2. Pada **Build and deployment**, pilih **Deploy from a branch**, branch `main`, folder `/ (root)`, lalu **Save**.
3. Tunggu sebentar. Alamat situs muncul di halaman yang sama.

Dashboard memuat font dan pustaka Excel dari internet, jadi perlu koneksi.

## Memperbarui data

1. Siapkan file Excel terbaru. Kolom wajib: `Segment` dan `port`. Kolom lain yang dipakai: `ODP ID`, `Region`, `Stasiun`, `Vendor Name`.
2. Jalankan:

   ```
   pip install pandas openpyxl
   python build_data.py Summary_ODP.xlsx
   ```

3. Unggah `data.json` yang baru ke repositori (commit dan push). Situs memakai data baru begitu halaman dimuat ulang.

`build_data.py` memakai aturan hitung yang sama dengan dashboard: satu baris ODP dihitung satu ODP, ODP ID kembar dan baris dengan port kosong dilewati.

## Catatan

- Jika `data.json` tidak bisa dimuat (misalnya `index.html` dibuka langsung dari folder), dashboard memakai salinan data yang tertanam di `index.html`.
- Segment baru di file Excel muncul otomatis sebagai kartu baru. Kartu `VIBERLINK` selalu ditampilkan dan terisi begitu ada baris dengan segment tersebut.
