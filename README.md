# KHARISMA Workshop Analytics — FINAL XLS + USER MANAGEMENT

Versi final gabungan: UI terbaru + Login/User Management + Admin License + parser sesuai 7 laporan `.xls` yang digunakan KHARISMA SENTOSA.

## Login awal
- Username: `admin`
- Password: `admin123`

## 7 laporan sumber yang didukung
1. `MaintainPKB.xls`
2. `RptPelanggan.xls`
3. `RptServicePenjualan.xls`
4. `RptNotaBahan.Bill Of Material Issue To PKB.xls`
5. `RptPenjualanPart.Billing Service.xls`
6. `RptNotaBahan.Bill Of Sales Order Consumable.xls`
7. `RptPenjualanPart.Billing SparePart.xls`

## Fitur utama
- Pembacaan `.xls` menggunakan `xlrd` dengan fallback LibreOffice bila tersedia.
- Registry laporan membaca periode dari isi laporan; format seperti `01.08.2026 S/D 31.08.2026` dan `01.08.2026 s.d 31.08.2026` didukung.
- Data historis disimpan permanen di komputer lokal dan tidak hilang saat browser refresh.
- Login lokal dan User Management.
- Default password `admin123`.
- Ganti username/password dan reset password ke default.
- Admin License: aktivasi license, status license, Computer ID, dan reset binding lokal.
- Jika license expired/belum aktif, aplikasi tetap bisa dibuka tetapi hanya halaman User Management yang dapat diakses.
- KPI cards hanya ditampilkan di Dashboard.
- Service Advisor dinormalisasi case-insensitive.
- 1 PKB = 1 UE.
- Data Input menerima banyak file per jenis laporan tanpa menimpa histori sebelumnya.
- Export Excel tersedia pada tabel-tabel analitik.

## Menjalankan
Jalankan `JALANKAN_APLIKASI.bat` pada Windows, atau:

```bash
streamlit run app.py
```

Jika instalasi baru:

```bash
pip install -r requirements.txt
```

### Login Session 48 Jam
Versi ini menyimpan sesi login lokal selama **48 jam** setelah login berhasil. Sesi tetap aktif saat browser di-refresh, tab ditutup lalu aplikasi dibuka kembali pada komputer yang sama, selama 48 jam belum lewat. Tombol **LOGOUT** menghapus sesi secara langsung. Perubahan username/password juga otomatis membatalkan sesi lama sehingga login ulang diperlukan.

## V23 — revisi
- Target & Pencapaian: tombol "Input Target" satu blok dengan judul; jarak antar blok dilonggarkan di semua halaman.
- Comparative: mode komparasi berupa dropdown (Per Bulan/Kuartal/Semester/Tahun, 3 & 6 Bulan Terakhir); cabang mengikuti sidebar.
- UE: tabel seragam berhalaman; UE per SA & Layanan memakai donat Dashboard.
- Sparepart & Bahan: semua tabel desain RK, maks 10 baris + nomor halaman.
- Bahan: kategori berdasarkan kode (mapping di expander), Rekapitulasi Penjualan Bahan.
- Management Insight: status target, diagnosis gap, skenario, strategi, rencana aksi, early warning.
