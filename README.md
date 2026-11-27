# Dashboard ODP & Homepass

Dashboard untuk melihat jumlah ODP dan homepass (ODP × port) per segment, dengan filter region dan vendor, rincian per segment, dan unduhan Excel.

Homepass dihitung dari jumlah port semua ODP.

## Isi repositori

| File | Fungsi |
|---|---|
| `index.html` | Halaman dashboard (satu file, tanpa build) |
| `data.json` | Salinan data terakhir. Saat situs ditayangkan, file ini dibuat ulang otomatis dari Google Drive |
| `build_data.py` | Skrip untuk membuat `data.json` dari file Excel |
| `.github/workflows/sinkron-data.yml` | Alur otomatis: unduh Excel dari Google Drive, buat `data.json`, tayangkan situs |

## Sinkron otomatis dengan Google Drive

Alur `sinkron-data.yml` berjalan sekitar tiap 5 menit (jadwal tercepat yang diizinkan GitHub), tiap ada push ke `main`, dan bisa dijalankan manual. Isinya: mengunduh `Summary_ODP.xlsx` dari Google Drive, membuat `data.json`, lalu menayangkan situs ke GitHub Pages. Halaman yang sedang terbuka memeriksa `data.json` baru tiap 1 menit.

Pemasangan satu kali:

1. Gabungkan (merge) cabang ini ke `main`.
2. Buka **Settings → Pages**, pada **Build and deployment → Source** pilih **GitHub Actions**.
3. Buka tab **Actions → Sinkron data dan deploy situs → Run workflow** untuk menjalankan pertama kali. Alamat situs muncul di halaman Pages.

Syarat dan batasan:

- File di Google Drive harus dibagikan dengan akses **Siapa saja yang memiliki link** (Viewer). Jika akses dibatasi, unduhan gagal dan situs memakai `data.json` terakhir yang ada di repositori (tampil peringatan di log Actions).
- ID file ada di `DRIVE_FILE_ID` pada file alur. Ganti jika file di Drive diganti dengan file baru.
- Jadwal GitHub bisa tertunda beberapa menit, jadi data tidak persis real time.
- Jadwal otomatis GitHub berhenti sendiri jika repositori tidak ada aktivitas selama 60 hari. Jalankan manual sekali untuk mengaktifkan lagi.

## Menjalankan manual (tanpa Actions)

1. Siapkan file Excel terbaru. Kolom wajib: `Segment` dan `port`. Kolom lain yang dipakai: `ODP ID`, `Region`, `Stasiun`, `Vendor Name`.
2. Jalankan:

   ```
   pip install pandas openpyxl
   python build_data.py Summary_ODP.xlsx
   ```

3. Commit dan push `data.json` yang baru. Jika memakai **Deploy from a branch** (bukan GitHub Actions), situs memakai data baru begitu halaman dimuat ulang.

`build_data.py` memakai aturan hitung yang sama dengan dashboard: satu baris ODP dihitung satu ODP, ODP ID kembar tetap dihitung, sedangkan baris dengan port kosong dilewati.

## Catatan

- Jika `data.json` tidak bisa dimuat (misalnya `index.html` dibuka langsung dari folder), dashboard memakai salinan data yang tertanam di `index.html`.
- Segment baru di file Excel muncul otomatis sebagai kartu baru. Kartu `VIBERLINK` selalu ditampilkan dan terisi begitu ada baris dengan segment tersebut.
