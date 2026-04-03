import math


def distance(p1, p2):
    """
    Euclidean distance between two points
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def attach_openings_to_walls(walls, openings, scale, threshold=0.5):
    """
    Attach doors/windows to nearest wall

    Args:
        walls: list of wall dicts
        openings: list of openings
        scale: pixel → meter
        threshold: max distance (meters)

    Returns:
        updated walls
    """

    for op in openings:
        center_px = op["center"]

        # convert to meters
        center_m = [center_px[0] * scale, center_px[1] * scale]

        nearest_wall = None
        min_dist = float("inf")

        for wall in walls:
            start = wall["start"]
            end = wall["end"]

            # distance to wall endpoints (simplified)
            d = min(distance(center_m, start), distance(center_m, end))

            if d < min_dist:
                min_dist = d
                nearest_wall = wall

        # attach if close enough
        if nearest_wall and min_dist < threshold:

            opening_data = {
                "pos": center_m,
                "width_m": round(op["width_px"] * scale, 3),
                "height_m": round(op["height_px"] * scale, 3),
                "orientation": nearest_wall["orientation"]
            }

            if op["type"] == "door":
                nearest_wall["doors"].append(opening_data)
            elif op["type"] == "window":
                nearest_wall["windows"].append(opening_data)

    return walls


def generate_metadata(walls):
    """
    Generate metadata summary
    """

    total_walls = len(walls)
    interior_walls = sum(1 for w in walls if w["type"] == "interior")
    exterior_walls = sum(1 for w in walls if w["type"] == "exterior")

    total_doors = sum(len(w["doors"]) for w in walls)
    total_windows = sum(len(w["windows"]) for w in walls)

    return {
        "total_walls": total_walls,
        "interior_walls": interior_walls,
        "exterior_walls": exterior_walls,
        "total_doors": total_doors,
        "total_windows": total_windows
    }


def generate_json(walls, openings, scale):
    """
    Main function to generate final JSON

    Args:
        walls: processed walls (geometry)
        openings: detected openings
        scale: pixel → meter

    Returns:
        structured JSON
    """

    # Step 1: Attach openings
    walls = attach_openings_to_walls(walls, openings, scale)

    # Step 2: Metadata
    metadata = generate_metadata(walls)

    # Step 3: Final structure
    output = {
        "metadata": metadata,
        "walls": walls
    }

    return output