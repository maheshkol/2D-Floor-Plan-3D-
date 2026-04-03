# backend/three_d/mesh_builder.py

import math


def create_wall_mesh(start, end, height=3.0, thickness=0.2):
    """
    Convert 2D wall → 3D mesh

    Args:
        start: [x, y]
        end: [x, y]
        height: wall height (meters)
        thickness: wall thickness

    Returns:
        dict representing 3D wall
    """

    x1, y1 = start
    x2, y2 = end

    # length of wall
    length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # midpoint (position)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # rotation angle
    angle = math.atan2(y2 - y1, x2 - x1)

    return {
        "type": "wall",
        "position": [mid_x, mid_y, height / 2],
        "dimensions": [length, thickness, height],
        "rotation": [0, 0, angle]
    }


def create_opening_mesh(opening, wall_height=3.0):
    """
    Create door/window mesh

    Args:
        opening: dict from JSON

    Returns:
        3D object
    """

    x, y = opening["pos"]
    width = opening["width_m"]
    height = opening["height_m"]

    return {
        "type": opening.get("type", "opening"),
        "position": [x, y, height / 2],
        "dimensions": [width, 0.1, height],  # thin depth
        "rotation": [0, 0, 0]
    }