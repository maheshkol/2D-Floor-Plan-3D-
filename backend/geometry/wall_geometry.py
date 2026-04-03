import math
from backend.geometry.orientation import get_orientation
from backend.geometry.scaling import pixels_to_meters, convert_point


def calculate_length(x1, y1, x2, y2):
    """
    Calculate pixel length
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def process_walls(walls, scale):
    """
    Convert walls into structured geometry

    Args:
        walls: list from detect_walls
        scale: pixel to meter scale

    Returns:
        structured wall data
    """

    processed = []

    for i, wall in enumerate(walls):
        x1, y1 = wall["start"]
        x2, y2 = wall["end"]

        length_px = calculate_length(x1, y1, x2, y2)
        length_m = pixels_to_meters(length_px, scale)

        orientation = get_orientation(x1, y1, x2, y2)

        processed.append({
            "wall_id": f"wall_{i+1}",
            "type": "interior",  # placeholder (can improve later)
            "start": convert_point([x1, y1], scale),
            "end": convert_point([x2, y2], scale),
            "length_m": round(length_m, 3),
            "orientation": orientation,
            "doors": [],
            "windows": []
        })

    return processed