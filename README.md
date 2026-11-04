# Real-Time PPE Safety and Hazard Zone Monitor

An edge-native computer vision system for industrial workplace safety compliance, combining YOLO object detection, ByteTrack multi-object tracking, and a leaky-integrator temporal hysteresis filter. The system tracks personal protective equipment (hard hats and safety vests) and monitors unauthorized worker entry into hazardous industrial machinery zones.

## Operational Problem and Engineering Solution

Standard video surveillance setups for safety compliance face a persistent operational issue known as alarm fatigue. In simple frame-by-frame detector architectures, brief sensor dropout (such as a worker momentarily bending down, turning away from the camera, or stepping behind scaffolding for two frames) causes the detector to lose sight of the hard hat. If every momentary loss triggers an audio siren or safety incident, control room operators quickly learn to mute or ignore the system.

A second issue is spatial attribution. When safety gear is detected near a worker (for example, a hard hat resting on a forklift pallet or a tool bench nearby), naive bounding box proximity metrics often treat the worker as compliant even though they are bareheaded.

This system addresses both issues through three engineering controls:
1. **Persistent identity tracking:** ByteTrack maintains unique worker IDs across occlusions, preventing duplicate violation counts.
2. **Anatomical spatial rules:** A helmet is only counted as worn if its centroid falls strictly within the upper 40% cranial region of the worker's bounding box. Vest detections are constrained to the torso.
3. **Leaky-integrator temporal hysteresis:** Violations are tracked using a per-worker integer credit counter. Alarms only escalate if a violation persists for 15 consecutive frames (roughly 0.5 to 1.0 second), filtering out transient detection flicker.

## Technical Implementation

1. **Object detection:** YOLO (`ppe.pt`) detects three primary classes: `person`, `helmet`, and `vest` at a 0.4 confidence threshold.
2. **Multi-object tracking:** ByteTrack associates low-score and high-score detections with existing tracklets using Kalman filter velocity predictions and bipartite Hungarian matching.
3. **Hazard zone geofencing:** Worker position is grounded using the bottom-center coordinate of the bounding box (foot point). This anchor is evaluated against arbitrary convex polygon zones using `cv2.pointPolygonTest`.
4. **Telemetry HUD:** An on-screen display renders bounding boxes, tracklet IDs, compliance status flags, and active hazard zone boundaries.

## Evaluation and Validation

The monitor was evaluated on real industrial workplace footage (`sample_person.mp4`, 1,394 frames at 1080p resolution):

| Metric | Result | Operational Target |
| :--- | :---: | :---: |
| Processed frames | 1,394 frames | Full sequence |
| Total processing time | 52.83 seconds | — |
| Inference throughput | 26.4 FPS (Host CPU) | >= 25 FPS (Real-time) |
| Mean compliant worker ratio | 24.8% | Ground truth benchmark |
| Verified incident escalations | 8 events | 0 false alarm bursts |
| Hysteresis threshold | 15 frames | Sustained violation filter |

The 15-frame hysteresis filter eliminated 184 momentary flicker events that would have triggered alarms under naive frame-by-frame evaluation, producing an incident log of exactly 8 sustained events.

## Documentation and Deliverables

* **Technical publication article:** [`MEDIUM_ARTICLE.md`](./MEDIUM_ARTICLE.md) or [`artikel.md`](./artikel.md) details the leaky-integrator formulation, cranial containment geometry, and real-time edge streaming considerations.
* **Video walkthrough:** [`video_presentation.mp4`](./video_presentation.mp4) provides a 1080p narrated presentation of the tracking architecture and live incident escalation ([English script transcript](./skenario_video_en.md)).
* **Annotated audit video:** [`output_ppe_audit.mp4`](./output_ppe_audit.mp4) contains the rendered video stream with bounding boxes, persistent IDs, geofence polygon overlays, and real-time compliance status banners.
* **Compliance timeline chart:** [`safety_monitoring_summary.png`](./safety_monitoring_summary.png) graphs the percentage of compliant workers over time with discrete incident escalation markers.
* **Structured incident log:** [`safety_incident_audit.json`](./safety_incident_audit.json) records timestamps, worker IDs, and violation types for each escalated event.
* **Sample detection frame:** [`result_ppe.jpg`](./result_ppe.jpg) shows worker tracking and PPE classification output.

## Running the Code

### 1. Process a video file (headless mode with video and log export)
```bash
python app.py --source sample_person.mp4 --weights ppe.pt --out output_ppe_audit.mp4 --headless
```

### 2. Run with live graphical display
```bash
python app.py --source sample_person.mp4 --weights ppe.pt
```
Press `q` to exit the window.

### 3. Define a custom hazard zone polygon
Coordinates are specified in normalized [0.0, 1.0] format:
```bash
python app.py --source sample_person.mp4 --zone "0.3,0.3;0.9,0.3;0.9,0.9;0.3,0.9"
```
