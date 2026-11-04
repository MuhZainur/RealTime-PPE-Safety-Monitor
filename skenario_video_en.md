# Video Presentation Scenario (English): Real-Time PPE Safety Monitor

> **Voice:** Natural Conversational English Narration (ElevenLabs / Azure Neural Speech)
> **Total Duration:** 138.34s (~2.31 min, 4150 frames @ 30 FPS)
> **Format:** 1920x1080 Full HD, Remotion MP4

---

### S01: Real-Time PPE Safety Monitor
- **Duration:** 13.51s audio + 0.5s pause = 14.01s (420 frames)
- **On-Screen Title:** `Real-Time PPE Safety Monitor`
- **On-Screen Subtitle:** `Automated hard hat, safety vest, and hazard zone compliance`
- **Narration (Spoken):**
  > "Safety officers cannot watch every camera feed around the clock. So I developed a computer vision system that monitors video streams, flagging workers without hard hats, without safety vests, or entering designated hazard zones."

### S02: Three Detection Classes: Person, Helmet, Vest
- **Duration:** 19.30s audio + 0.5s pause = 19.80s (594 frames)
- **On-Screen Title:** `Three Detection Classes: Person, Helmet, Vest`
- **On-Screen Subtitle:** `Minimum detection confidence threshold: 0.40 with ByteTrack persistence`
- **Narration (Spoken):**
  > "First, a YOLO model scans each frame for three classes: person, helmet, and vest. Any detection with confidence below zero point four is discarded. Then, a multi-object tracker called ByteTrack assigns each worker a persistent ID, ensuring worker number three remains worker number three across frames."

### S03: Helmet: Top 40% of Bounding Box. Feet: Bottom-Center in Polygon
- **Duration:** 19.64s audio + 0.5s pause = 20.14s (604 frames)
- **On-Screen Title:** `Helmet: Top 40% of Bounding Box. Feet: Bottom-Center in Polygon`
- **On-Screen Subtitle:** `Spatial containment rules and ray-casting polygon testing`
- **Narration (Spoken):**
  > "The logic is straightforward. A helmet is considered worn if its center lies within the upper forty percent of the person's bounding box. A vest must be inside the body region. For hazard zones, I track the worker's foot position—the bottom-center coordinate of the box—and test whether that point falls inside the restricted polygon."

### S04: Alarm Escalates Only After 15 Consecutive Violation Frames
- **Duration:** 26.36s audio + 0.5s pause = 26.86s (806 frames)
- **On-Screen Title:** `Alarm Escalates Only After 15 Consecutive Violation Frames`
- **On-Screen Subtitle:** `Temporal hysteresis filter suppresses transient flicker and prevents alarm fatigue`
- **Narration (Spoken):**
  > "The biggest practical obstacle is detection flickering. A helmet might disappear for one or two frames simply because a worker looked down. If every momentary glitch triggered an alarm, operators would suffer alarm fatigue. So each worker has a temporal counter: incrementing by one during a violation, and decrementing by two when compliant. An official incident is only escalated after fifteen consecutive violation frames."

### S05: 1,394 Frames Processed at 26.4 FPS on CPU
- **Duration:** 16.20s audio + 0.5s pause = 16.70s (501 frames)
- **On-Screen Title:** `1,394 Frames Processed at 26.4 FPS on CPU`
- **On-Screen Subtitle:** `Results measured across a single unannotated operational video`
- **Narration (Spoken):**
  > "I evaluated the pipeline on a test video containing one thousand three hundred ninety-four frames, which processed in fifty-two point eight three seconds. That averages approximately twenty-six point four frames per second on CPU, comfortably fast enough for real-time monitoring."

### S06: 8 Incidents Escalated | Average Compliance: 24.8%
- **Duration:** 22.80s audio + 0.5s pause = 23.30s (699 frames)
- **On-Screen Title:** `8 Incidents Escalated | Average Compliance: 24.8%`
- **On-Screen Subtitle:** `Automated log output on a single test video (Not yet human-annotated ground truth)`
- **Narration (Spoken):**
  > "The audit log recorded eight confirmed incidents—all involving missing helmets and vests, with three also breaching the hazard zone. The average worker compliance was twenty-four point eight percent. Please note, these metrics reflect the automated system output on a single unannotated video. Ground-truth frame labels were not available to calculate human-verified precision."

### S07: Next Steps: Benchmark on Labeled Safety Video Datasets
- **Duration:** 17.03s audio + 0.5s pause = 17.53s (526 frames)
- **On-Screen Title:** `Next Steps: Benchmark on Labeled Safety Video Datasets`
- **On-Screen Subtitle:** `Worker IDs can switch during occlusions; ground-truth precision measurement needed`
- **Narration (Spoken):**
  > "One limitation observed in the logs is that worker IDs can switch if tracking is lost during heavy occlusions, meaning a single individual might be counted twice. The next milestone is benchmarking on fully annotated ground-truth datasets to quantify formal precision and recall. Thank you for watching."

