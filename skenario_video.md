# Skenario Video: Real-Time PPE Safety Monitor

Durasi target 2:30 sampai 2:50. Bahasa Indonesia sehari-hari. Narasi untuk ElevenLabs, visual dibuat dengan Remotion oleh model lain.

## 1. Aturan yang wajib dipatuhi

1. Semua angka di layar dan narasi harus sama dengan file ini. Jangan menambah angka lain.
2. Angka 24,8 persen dan 8 insiden selalu disebut sebagai "hasil program pada satu video". Jangan disebut sebagai akurasi.
3. Video asli hanya boleh dipotong dan diberi teks. Jangan menggambar kotak deteksi buatan di atasnya. Kotak yang tampil harus berasal dari `output_ppe_audit.mp4`.
4. Jangan menulis klaim seperti "nol alarm palsu" atau "terverifikasi".

## 2. Spesifikasi teknis

Remotion
- 1920x1080, 30 fps, keluaran mp4 (h264).
- Satu `<Sequence>` per scene, durasinya dari panjang mp3 (`getAudioDurationInSeconds`) ditambah 0,5 detik. Timestamp di bawah hanya perkiraan.
- Video dimasukkan dengan `<OffthreadVideo>`. Pakai `startFrom` dan `endAt` untuk memotong, volume 0.
- Fade antar scene 10 frame. Teks layar fade dan geser naik 20 px selama 12 frame.
- Latar #0B1220, teks putih, aksen merah (#EF4444) untuk pelanggaran dan hijau (#22C55E) untuk patuh. Judul 64 px, isi 36 px, margin 120 px.
- Teks layar ditulis sebagai teks Remotion. Subtitle memakai teks narasi, maksimal dua baris.
- Salin aset ke `public/` dan panggil dengan `staticFile()`.

ElevenLabs
- Model `eleven_multilingual_v2`, suara Indonesia yang tenang. Stability 0,5, similarity 0,75, style 0.
- Satu file per scene: `s01.mp3` sampai `s07.mp3`.
- Ejaan khusus di narasi (misalnya "Bait Trek") jangan diubah.

## 3. Aset yang boleh dipakai

| Path di folder proyek | Dipakai untuk |
| :--- | :--- |
| `output_ppe_audit.mp4` | cuplikan hasil, scene 3 sampai 6 |
| `result_ppe.jpg` | gambar diam deteksi, scene 2 |
| `safety_monitoring_summary.png` | grafik kepatuhan, scene 6 |
| `safety_incident_audit.json` | tabel insiden, scene 6 |

## 4. Scene

### Scene 1, 0:00 sampai 0:14, pembuka

Visual: judul "Pemantau Helm, Rompi, dan Zona Bahaya". Di belakangnya cuplikan 5 detik pertama `output_ppe_audit.mp4`, dikecilkan 60 persen dan diburamkan.

Teks layar: Real-Time PPE Safety Monitor

Narasi:
> Petugas K3 tidak bisa menatap semua kamera sepanjang hari. Jadi saya membuat program yang menonton video, lalu memberi tahu kalau ada pekerja tanpa helm, tanpa rompi, atau masuk zona bahaya.

### Scene 2, 0:14 sampai 0:36, tiga hal yang dideteksi

Visual: `result_ppe.jpg` penuh layar. Tiga label muncul bergantian di samping: "Orang", "Helm", "Rompi". Jangan menggambar kotak baru.

Teks layar: Tiga kelas: orang, helm, rompi. Kepercayaan minimal 0,4

Narasi:
> Pertama, model Yolo mencari tiga hal di setiap frame, yaitu orang, helm, dan rompi. Hasil yang kepercayaannya di bawah nol koma empat dibuang. Lalu sebuah pelacak bernama Bait Trek memberi tiap orang nomor, supaya pekerja nomor tiga tetap nomor tiga dari frame ke frame.

### Scene 3, 0:36 sampai 1:00, aturan helm, rompi, dan zona

Visual: cuplikan dari `output_ppe_audit.mp4` yang diperlambat 50 persen. Di samping muncul diagram sederhana: kotak orang dengan garis di 40 persen bagian atas ("area helm"), titik di tengah bawah kotak ("posisi kaki"), dan poligon zona.

Teks layar: Helm: 40 persen bagian atas. Kaki: titik tengah bawah kotak

Narasi:
> Berikutnya, aturannya sederhana. Helm dihitung kalau ada di empat puluh persen bagian atas badan. Rompi dihitung kalau ada di dalam kotak orang itu. Untuk zona bahaya, saya ambil posisi kaki, yaitu titik tengah di sisi bawah kotak, lalu diuji apakah titik itu ada di dalam poligon zona.

### Scene 4, 1:00 sampai 1:26, anti kedip

Visual: grafik animasi garis. Sumbu bawah frame, sumbu atas penghitung pelanggaran. Garis naik 1 per frame, turun 2 saat patuh, dan garis putus-putus di angka 15 bertuliskan "alarm". Satu lonjakan pendek yang tidak sampai 15 diberi label "kedipan, diabaikan".

Teks layar: Alarm baru setelah 15 frame berturut-turut

Narasi:
> Masalah terbesar adalah kedipan. Helm bisa hilang dari deteksi satu atau dua frame hanya karena orangnya menunduk. Kalau tiap kedipan membunyikan alarm, petugas akan berhenti percaya. Jadi tiap pekerja punya penghitung. Naik satu saat melanggar, turun dua saat patuh. Insiden baru dicatat setelah lima belas frame berturut-turut.

### Scene 5, 1:26 sampai 1:52, hasil pada video uji

Visual: cuplikan `output_ppe_audit.mp4` dengan panel status di atas yang sudah ada di video. Di kanan muncul tabel angka satu per satu.

Teks layar: 1.394 frame. 26,4 FPS di CPU. Hasil pada satu video

Narasi:
> Saya menjalankannya pada satu video uji. Ada seribu tiga ratus sembilan puluh empat frame, diproses dalam lima puluh dua koma delapan tiga detik. Itu sekitar dua puluh enam koma empat frame per detik di CPU. Cukup cepat untuk berjalan langsung.

### Scene 6, 1:52 sampai 2:22, catatan insiden

Visual: tabel dari `safety_incident_audit.json` dengan 8 baris (INC-001 sampai INC-008), baris INC-002, INC-006, INC-007 ditandai "zona". Setelah itu `safety_monitoring_summary.png`.

Teks layar: 8 insiden dieskalasi. Rata-rata patuh 24,8 persen. 10 orang pernah masuk zona

Narasi:
> Hasilnya, program mencatat delapan insiden. Semuanya tanpa helm dan rompi, dan tiga di antaranya juga masuk zona bahaya. Rata-rata pekerja yang patuh dua puluh empat koma delapan persen. Angka ini hasil keluaran program pada satu video. Saya belum melabeli video itu satu per satu, jadi belum ada angka ketepatan yang bisa dibandingkan dengan penilaian manusia.

### Scene 7, 2:22 sampai 2:45, batasan dan penutup

Visual: cuplikan terakhir video, lalu daftar dua poin muncul di kanan.

Teks layar: Nomor pekerja bisa berganti. Perlu video berlabel untuk mengukur ketepatan

Narasi:
> Ada satu kelemahan yang saya lihat di log. Nomor pekerja bisa berganti kalau pelacak kehilangan seseorang, jadi satu orang mungkin tercatat dua kali. Langkah selanjutnya, melabeli video uji supaya ketepatannya bisa diukur. Terima kasih sudah menonton.

## 5. Daftar periksa sebelum render

1. Angka cocok: 0,4, 40 persen, 15 frame, 1.394 frame, 52,83 detik, 26,4 FPS, 8 insiden, 3 insiden dengan zona, 24,8 persen, 10 orang.
2. Tidak ada kotak deteksi buatan, hanya yang ada di video asli.
3. Kalimat "hasil pada satu video" terlihat di scene 5 dan 6.
4. Subtitle sama dengan narasi. Total 2:30 sampai 2:50.
