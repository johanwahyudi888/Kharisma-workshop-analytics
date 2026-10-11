KHARISMA Workshop Analytics V20
Perubahan: tampilan baru mengikuti referensi (header global, Dashboard, Target & Pencapaian,
Comparative, UE, Sparepart, Data Input 3 mode, konsolidasi bulanan, kartu modul, input target per cabang).
File baru: ref_ui.py (komponen tampilan). Semua fitur lama dipertahankan.
Jalankan: pip install -r requirements.txt  lalu  streamlit run app.py  (atau JALANKAN_APLIKASI.bat)
Perubahan V20: kartu formula dashboard diperbesar; donat Revenue per SA & Booking/Walk-In fix (tanpa scroll/zoom, legenda di bawah); nama SA tampil nama lengkap (dari akun pengguna / nama pada laporan Estimasi); tombol download minimalis.
Tips: agar akun SA tampil nama lengkap, isi Nama Lengkap pada User Management dengan Email Akun = kode SA (mis. johan123).

V20: formula kembali normal; donat tanpa kartu putih + legenda kanan + hover; grafik fixed; Target tanpa tab/download + detail lengkap baru; Comparative + diagram batang, tanpa multi-periode; Bahan & Consumable desain baru, 3 kategori, tabel filter/sortir.

V20: donat Dashboard bergaya kartu (header+garis, legenda kanan, Counter Sales Non-PKB); Data Input harian sesuai foto + Tambah Transaksi Manual; kartu (st.metric) & tabel kecil seluruh halaman diseragamkan dengan desain Dashboard; judul seksi memakai kartu header.


V21: Target & Pencapaian: kartu 'Hari berjalan', Tren Harian 1 Bulan dan Tren Bulanan dihapus; diganti Metrik per Kartu + Kontrol Harian (garis & kartu Target Harian Rata-rata / Rata-rata Aktual per Hari). Tren Bulanan dipindah ke Comparative Analytics. Donat Revenue per SA & UE Booking/Walk-In: latar putih dan tinggi kartu sama. Desain semua halaman dirapikan (jarak, kartu, tabel, kontrol segmen).
V21b: kartu KPI atas halaman Target dihapus; 4 kartu minimalis di bawah Kontrol Harian; jarak antar blok global diperlebar; donat Dashboard diperbaiki (tidak blank), Counter Sales Non-PKB dihapus, legenda SA bisa di-scroll; PERFORMA: cache pipeline data kini bertahan antar klik (sebelumnya dihitung ulang tiap pindah halaman/filter).
