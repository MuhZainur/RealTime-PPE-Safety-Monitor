"""Wrapper YOLO + ByteTrack, dan aturan kepatuhan APD."""
from __future__ import annotations

from dataclasses import dataclass

from ultralytics import YOLO

Box = tuple[float, float, float, float]


@dataclass
class Det:
    label: str  # person | helmet | vest
    box: Box
    track_id: int | None


def _canon(name: str) -> str | None:
    n = name.lower()
    if n.startswith("no"):  # kelas negatif dataset, mis. "NO-Hardhat"
        return None
    if "person" in n or "worker" in n or "human" in n:
        return "person"
    if "helmet" in n or "hardhat" in n:
        return "helmet"
    if "vest" in n:
        return "vest"
    return None


class PPEDetector:
    def __init__(self, weights: str = "ppe.pt", conf: float = 0.4) -> None:
        self.model = YOLO(weights)
        self.conf = conf

    def track(self, frame) -> list[Det]:
        r = self.model.track(frame, persist=True, tracker="bytetrack.yaml",
                             conf=self.conf, verbose=False)[0]
        out = []
        for b in r.boxes:
            label = _canon(self.model.names[int(b.cls)])
            if label:
                tid = int(b.id) if b.id is not None else None
                out.append(Det(label, tuple(b.xyxy[0].tolist()), tid))
        return out


def check_ppe(person: Box, dets: list[Det]) -> tuple[bool, bool]:
    """(pakai_helm, pakai_rompi): pusat kotak APD harus di dalam kotak pekerja.
    Helm harus di 40% bagian atas."""
    x1, y1, x2, y2 = person
    helmet = vest = False
    for d in dets:
        cx, cy = (d.box[0] + d.box[2]) / 2, (d.box[1] + d.box[3]) / 2
        if not (x1 <= cx <= x2 and y1 <= cy <= y2):
            continue
        if d.label == "helmet" and cy <= y1 + 0.4 * (y2 - y1):
            helmet = True
        elif d.label == "vest":
            vest = True
    return helmet, vest
