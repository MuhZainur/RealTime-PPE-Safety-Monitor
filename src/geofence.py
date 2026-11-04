"""Zona berbahaya berbentuk poligon. Koordinat zona dalam pecahan 0-1 agar tidak tergantung resolusi."""
from __future__ import annotations

import cv2
import numpy as np


class Zone:
    def __init__(self, norm_points: list[tuple[float, float]], width: int, height: int) -> None:
        self.poly = np.array([(x * width, y * height) for x, y in norm_points], dtype=np.float32)

    def contains(self, point: tuple[float, float]) -> bool:
        return cv2.pointPolygonTest(self.poly, (float(point[0]), float(point[1])), False) >= 0

    def draw(self, frame, alarm: bool) -> None:
        color = (0, 0, 255) if alarm else (0, 165, 255)
        cv2.polylines(frame, [self.poly.astype(np.int32)], True, color, 2)


def foot_point(box: tuple[float, float, float, float]) -> tuple[float, float]:
    """Titik tengah sisi bawah kotak = posisi kaki di lantai."""
    return (box[0] + box[2]) / 2, box[3]


def parse_zone(text: str) -> list[tuple[float, float]]:
    """'0.5,0.5;1,0.5;1,1;0.5,1' -> [(0.5,0.5), ...]"""
    pts = [tuple(float(v) for v in p.split(",")) for p in text.split(";")]
    assert len(pts) >= 3 and all(len(p) == 2 for p in pts), "zona butuh >=3 titik 'x,y'"
    return pts
