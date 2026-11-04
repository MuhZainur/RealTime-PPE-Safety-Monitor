"""Unit tests for Geofence Polygon checking and PPE compliance logic."""

import pytest
from src.geofence import Zone, foot_point, parse_zone
from src.detector import Det, check_ppe


def test_parse_zone():
    zone_str = "0.0,0.0;1.0,0.0;1.0,1.0;0.0,1.0"
    pts = parse_zone(zone_str)
    assert len(pts) == 4
    assert pts[0] == (0.0, 0.0)


def test_zone_containment():
    pts = [(0.0, 0.0), (0.5, 0.0), (0.5, 0.5), (0.0, 0.5)]
    zone = Zone(pts, width=100, height=100)
    
    # Inside zone
    assert zone.contains((25, 25)) is True
    # Outside zone
    assert zone.contains((75, 75)) is False


def test_foot_point():
    box = (10.0, 20.0, 50.0, 100.0)  # (x1, y1, x2, y2)
    # Foot point should be center of bottom edge: x = (10+50)/2 = 30, y = 100
    pt = foot_point(box)
    assert pt == (30.0, 100.0)


def test_check_ppe_logic():
    # Person box: [100, 100, 200, 300] (w=100, h=200)
    person_box = (100.0, 100.0, 200.0, 300.0)
    
    # Helmet inside top 40% (y between 100 and 180)
    helmet = Det(label="helmet", box=(130.0, 110.0, 170.0, 140.0), track_id=None)
    # Vest in torso (y between 150 and 250)
    vest = Det(label="vest", box=(120.0, 160.0, 180.0, 240.0), track_id=None)
    
    dets = [helmet, vest]
    has_helmet, has_vest = check_ppe(person_box, dets)
    assert has_helmet is True
    assert has_vest is True
