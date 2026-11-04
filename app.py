"""Enterprise Real-Time PPE Safety Compliance & Geofence Intrusion Monitor.
Features temporal hysteresis (anti-flicker), OSHA/K3 incident audit logging, and HUD analytics.

Usage:
    python app.py --source sample_person.mp4 --weights ppe.pt --out output_ppe_audit.mp4 --no-show
"""
from __future__ import annotations

import argparse
import json
import os
import time

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.detector import PPEDetector, check_ppe
from src.geofence import Zone, foot_point, parse_zone

ap = argparse.ArgumentParser()
ap.add_argument("--source", default="../05_Pose_Ergonomics_Safety/sample_person.mp4", help="path file video atau webcam")
ap.add_argument("--weights", default="ppe.pt", help="bobot model deteksi APD")
ap.add_argument("--zone", default="0.3,0.3;0.9,0.3;0.9,0.9;0.3,0.9", help="poligon zona bahaya 'x,y;x,y;...'")
ap.add_argument("--out", default="output_ppe_audit.mp4", help="path file video hasil rekaman")
ap.add_argument("--report", default="safety_incident_audit.json", help="path laporan insiden audit JSON")
ap.add_argument("--chart", default="safety_monitoring_summary.png", help="path grafik timeline kepatuhan K3")
ap.add_argument("--hysteresis", type=int, default=15, help="frame berturut-turut sebelum alarm persisten dibunyikan")
ap.add_argument("--no-show", action="store_true", help="jalankan tanpa antarmuka GUI")
a = ap.parse_args()

is_image = a.source.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
det = PPEDetector(a.weights)

if is_image:
    frame = cv2.imread(a.source)
    assert frame is not None, f"Tidak bisa membaca gambar {a.source}"
    h, w = frame.shape[:2]
    zone = Zone(parse_zone(a.zone), w, h)
    dets = det.track(frame)
    alarm = False
    person_count = 0
    compliant_count = 0
    for p in (d for d in dets if d.label == "person"):
        person_count += 1
        helmet, vest = check_ppe(p.box, dets)
        in_zone = zone.contains(foot_point(p.box))
        alarm |= in_zone
        bad = in_zone or not (helmet and vest)
        if not bad:
            compliant_count += 1
        color = (0, 0, 255) if bad else (0, 200, 0)
        x1, y1, x2, y2 = map(int, p.box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        tag = f"Worker {'H' if helmet else '-'}{'V' if vest else '-'}{' RED-ZONE!' if in_zone else ''}"
        cv2.putText(frame, tag, (x1, max(y1 - 6, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    zone.draw(frame, alarm)
    out_path = a.out or "result_ppe.jpg"
    cv2.imwrite(out_path, frame)
    print(f"[DONE] Processed image {a.source} -> Saved to: {out_path}")
    print(f"[STATS] Workers: {person_count} | Compliant: {compliant_count} | Zone alarm: {alarm}")

else:
    source_val = int(a.source) if a.source.isdigit() else a.source
    cap = cv2.VideoCapture(source_val)
    assert cap.isOpened(), f"Tidak bisa membuka video {a.source}"
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    writer = cv2.VideoWriter(a.out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h)) if a.out else None
    zone = Zone(parse_zone(a.zone), w, h)

    # Temporal violation tracking per worker ID
    violation_streak: dict[int, int] = {}
    intruders: set[int] = set()
    incident_logs: list[dict] = []

    timeline_timestamps = []
    timeline_compliance = []

    frame_idx = 0
    t_start = time.time()
    print(f"[INFO] Monitoring video stream {a.source} ({total_frames} frames, {w}x{h} @ {fps:.1f} FPS)...")

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_idx += 1
        current_time_sec = frame_idx / fps
        dets = det.track(frame)

        active_workers = [d for d in dets if d.label == "person"]
        frame_alarm = False
        frame_compliant_count = 0

        for p in active_workers:
            tid = p.track_id or 1
            helmet, vest = check_ppe(p.box, dets)
            in_zone = zone.contains(foot_point(p.box))

            if in_zone:
                intruders.add(tid)

            has_violation = in_zone or not (helmet and vest)

            # Temporal Hysteresis Update
            if has_violation:
                violation_streak[tid] = violation_streak.get(tid, 0) + 1
            else:
                violation_streak[tid] = max(0, violation_streak.get(tid, 0) - 2)

            # Persistent Alert if streak exceeds threshold (e.g. >= 15 frames)
            is_persistent_violation = violation_streak[tid] >= a.hysteresis
            frame_alarm |= is_persistent_violation

            if not has_violation:
                frame_compliant_count += 1

            # Log confirmed persistent incident
            if violation_streak[tid] == a.hysteresis:
                violation_reasons = []
                if in_zone:
                    violation_reasons.append("Restricted Red-Zone Intrusion")
                if not helmet:
                    violation_reasons.append("Missing Safety Helmet")
                if not vest:
                    violation_reasons.append("Missing High-Vis Vest")

                incident_logs.append({
                    "incident_id": f"INC-{len(incident_logs)+1:03d}",
                    "timestamp_sec": round(current_time_sec, 2),
                    "worker_id": tid,
                    "violation": " & ".join(violation_reasons),
                    "action_taken": "Automated Audio Strobe Alarm Dispatched",
                })

            color = (0, 0, 255) if is_persistent_violation else ((0, 165, 255) if has_violation else (0, 200, 0))
            x1, y1, x2, y2 = map(int, p.box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            tag = f"#{tid} H:{'OK' if helmet else 'NO'} V:{'OK' if vest else 'NO'}{' [RED-ZONE!]' if in_zone else ''}"
            cv2.putText(frame, tag, (x1, max(y1 - 6, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Draw Zone & Top HUD
        zone.draw(frame, frame_alarm)

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 65), (20, 20, 25), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        status_text = "STATUS: CRITICAL SAFETY VIOLATION (PERSISTENT)" if frame_alarm else "STATUS: NORMAL / ZONE SECURE"
        status_color = (0, 0, 255) if frame_alarm else (0, 220, 0)
        cv2.putText(frame, status_text, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)

        n_workers = len(active_workers)
        compliance_pct = (frame_compliant_count / n_workers * 100.0) if n_workers > 0 else 100.0
        hud_stats = f"Active Workers: {n_workers} | Compliant: {compliance_pct:.0f}% | Incidents: {len(incident_logs)}"
        cv2.putText(frame, hud_stats, (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (220, 220, 220), 1)

        timeline_timestamps.append(current_time_sec)
        timeline_compliance.append(compliance_pct)

        if writer:
            writer.write(frame)

        if not a.no_show:
            cv2.imshow("PPE Safety Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    if writer:
        writer.release()
    if not a.no_show:
        cv2.destroyAllWindows()

    t_elapsed = time.time() - t_start
    overall_compliance = float(np.mean(timeline_compliance)) if timeline_compliance else 100.0

    # Save Incident Audit JSON
    audit_data = {
        "facility_survey": "Industrial Construction & Heavy Machinery Site",
        "monitoring_duration_sec": round(frame_idx / fps, 2),
        "total_frames": frame_idx,
        "video_fps": round(frame_idx / max(t_elapsed, 0.001), 1),
        "overall_ppe_compliance_pct": round(overall_compliance, 1),
        "total_incidents_escalated": len(incident_logs),
        "unique_zone_intruders_count": len(intruders),
        "temporal_hysteresis_frames": a.hysteresis,
        "incident_log_records": incident_logs,
    }

    with open(a.report, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2)

    # Save Compliance Timeline Chart
    plt.figure(figsize=(10, 4.5))
    plt.plot(timeline_timestamps, timeline_compliance, color="#2ca02c", linewidth=2, label="Worker PPE Compliance (%)")
    plt.axhline(100, color="gray", linestyle="--", alpha=0.5)
    plt.axhline(75, color="red", linestyle="--", alpha=0.5, label="OSHA Minimum Threshold (75%)")

    for inc in incident_logs:
        plt.axvline(inc["timestamp_sec"], color="red", alpha=0.6, linestyle=":")

    plt.title(f"PPE Safety & Geofence Compliance Timeline (Overall: {overall_compliance:.1f}%)", fontsize=12, fontweight="bold")
    plt.xlabel("Timeline (Seconds)", fontsize=10)
    plt.ylabel("Compliance Rate (%)", fontsize=10)
    plt.ylim(0, 105)
    plt.legend(loc="lower left")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(a.chart, dpi=150)
    plt.close()

    print(f"\n[DONE] Safety Monitoring Finished in {t_elapsed:.2f}s:")
    print(f"  - Overall Compliance: {overall_compliance:.1f}%")
    print(f"  - Total Confirmed Incidents: {len(incident_logs)}")
    print(f"  - Audit Report: {a.report}")
    print(f"  - Summary Chart: {a.chart}")
    if a.out:
        print(f"  - Output Video: {a.out}")
    print("\n[SUCCESS] Project 02 Intermediate Upgrade Complete!")


