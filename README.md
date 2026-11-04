# 🦺 Real-Time PPE Safety & Hazard Zone Monitor (K3 / HSE)

Sistem pengawasan keselamatan kerja (K3/HSE) real-time berbasis **YOLOv11 Object Detection**, **ByteTrack Multi-Object Tracking**, dan **Temporal Hysteresis Alarm**. Mengawasi kepatuhan APD (helm dan rompi keselamatan) serta pelanggaran zona berbahaya di area konstruksi dan industri.

---

## 🎯 Nilai Bisnis & Masalah Industri
- **Problem:** Petugas K3 lapangan tidak dapat memantau puluhan kamera CCTV secara serentak 24/7. Selain itu, alarm deteksi frame-by-frame standar sering mengalami *flickering* (false alarm sesaat akibat oklusi parsial atau pekerja menunduk 1-2 frame), menyebabkan "alarm fatigue" bagi petugas.
- **Solusi AI:** 
  1. Pelacakan identitas pekerja secara persisten via **ByteTrack ID**.
  2. **Temporal Hysteresis Logic:** Alarm hanya diaktifkan jika pelanggaran berlangsung secara persisten selama $\ge 15$ frame berurutan (~0.5 - 1 detik), mengeliminasi false alarm transien.
  3. **Pencatatan Insiden Otomatis:** Menghasilkan audit log terstruktur berstandar K3 untuk pelaporan investigasi kecelakaan kerja.

---

## 🏗️ Pendekatan Teknis (Intermediate-Level Engineering)
1. **Multi-Class Detection:** Menggunakan bobot deteksi PPE (`ppe.pt`) untuk kelas `person`, `helmet`, dan `vest`.
2. **Geometric Spatial Assignment:** 
   - Helm dievaluasi pada 40% area atas bounding box pekerja.
   - Rompi dievaluasi pada area torso tengah.
   - Kaki pekerja diproyeksikan pada titik bawah tengah bounding box untuk uji poligon zona bahaya (`cv2.pointPolygonTest`).
3. **Temporal Violation Counter & Escalation:** Setiap pekerja memiliki state pelanggaran independen. Pelanggaran persisten langsung dicatat ke `safety_incident_audit.json`.
4. **Dark HUD Visual Telemetry:** Overlay dashboard real-time dengan status kepatuhan K3, counter pekerja, dan banner peringatan merah saat status `ALARM ESCALATED`.

---

## 📊 Hasil Benchmark & Validasi Riil

Pengujian komprehensif dijalankan pada rekaman video lingkungan industri nyata:
- **Total Frame Diproses:** 1.394 frame video
- **Waktu Pemrosesan:** 52,83 detik
- **Throughput Inferensi:** **26,4 FPS** (Real-Time di CPU host)
- **Tingkat Kepatuhan APD Rata-rata:** 24.8%
- **Insiden K3 Terverifikasi:** 8 insiden pelanggaran persisten tereskalasi (bebas false alarm sesaat)

---

## 🖼️ Hasil Visual & Laporan Audit

- **Artikel Publikasi Teknis (Medium Style):** [`MEDIUM_ARTICLE.md`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/MEDIUM_ARTICLE.md) / [`artikel.md`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/artikel.md)  
  Ulasan engineering komprehensif: eliminasi alarm fatigue, pelacakan ByteTrack, batas topologi kranial 40%, dan filter histeresis temporal leaky-integrator.
- **Video Presentasi Portofolio (Remotion + ElevenLabs):** [`video_presentation.mp4`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/video_presentation.mp4) ([Naskah Skenario Bahasa Inggris](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/skenario_video_en.md))  
  Video presentasi Full HD 1080p berdurasi ~2:18 menit dengan narasi suara natural berbahasa Inggris, teks layar, dan demonstrasi K3 anti-flicker real-time.
- **Audit Video Lengkap:** [`output_ppe_audit.mp4`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/output_ppe_audit.mp4)  
  Video hasil pemantauan dengan tracking ID pekerja, poligon zona bahaya, dan HUD banner status K3 real-time.
- **Grafik Kepatuhan Time-Series:** [`safety_monitoring_summary.png`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/safety_monitoring_summary.png)  
  Visualisasi persentase pekerja patuh frame-demi-frame dengan penanda waktu eskalasi insiden K3.
- **Laporan Insiden K3 JSON:** [`safety_incident_audit.json`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/safety_incident_audit.json)  
  Log formal yang mencantumkan timestamp frame, ID pekerja, dan jenis pelanggaran (*No Helmet, No Vest, Hazard Zone Intrusion*).
- **Contoh Snapshot Deteksi:** [`result_ppe.jpg`](file:///H:/coding/Portfolio/Computer%20Vision/02_RealTime_PPE_Safety_Monitor/result_ppe.jpg)

---

## 🚀 Cara Menjalankan

### 1. Menjalankan Pemantauan Video Lengkap (Audit Video + Log)
```bash
python app.py --source sample_person.mp4 --weights ppe.pt --out output_ppe_audit.mp4 --headless
```

### 2. Menjalankan dengan Tampilan Layar Langsung (GUI)
```bash
python app.py --source sample_person.mp4 --weights ppe.pt
```
*(Tekan tombol `q` untuk berhenti).*

### 3. Menguji pada Citra Diam (Snapshot)
```bash
python -c "from src.detector import PPEDetector; import cv2; det=PPEDetector('ppe.pt'); img=cv2.imread('sample_construction.jpg'); res,_=det.detect_and_check(img); cv2.imwrite('result_test.jpg', res)"
```
