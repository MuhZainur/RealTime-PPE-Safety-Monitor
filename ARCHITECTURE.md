# Arsitektur

```mermaid
flowchart LR
    V[Video / webcam] --> D["YOLO11n fine-tuned<br/>person, helmet, vest"]
    D --> T[ByteTrack<br/>ID per pekerja]
    T --> P[check_ppe<br/>helm di 40% atas, rompi di dalam kotak]
    T --> F[foot_point<br/>tengah sisi bawah kotak]
    F --> G["Zone.contains<br/>cv2.pointPolygonTest"]
    P --> O[Overlay: kotak hijau/merah + ID]
    G --> O
    G --> C[Set ID unik pelanggar zona]
    C --> O
    O --> W[Jendela OpenCV + status ALARM]
```

| File | Peran |
|---|---|
| `src/detector.py` | wrapper YOLO + tracker, aturan APD |
| `src/geofence.py` | poligon zona dan titik kaki |
| `app.py` | loop video, gambar overlay dan alarm |
