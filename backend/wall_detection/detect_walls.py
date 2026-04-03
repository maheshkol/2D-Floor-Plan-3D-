import math


def calculate_length(x1, y1, x2, y2):
    """
    Calculate length of line
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_orientation(x1, y1, x2, y2, angle_threshold=10):
    """
    Determine orientation (horizontal / vertical)
    """
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

    if abs(angle) < angle_threshold:
        return "horizontal"
    elif abs(abs(angle) - 90) < angle_threshold:
        return "vertical"
    else:
        return "other"


def filter_walls(lines, min_length=100):
    """
    Filter valid walls from detected lines

    Args:
        lines: list of lines
        min_length: minimum wall length

    Returns:
        filtered walls
    """

    walls = []

    for (x1, y1, x2, y2) in lines:
        length = calculate_length(x1, y1, x2, y2)

        if length < min_length:
            continue

        orientation = get_orientation(x1, y1, x2, y2)

        if orientation == "other":
            continue

        walls.append({
            "start": [x1, y1],
            "end": [x2, y2],
            "length_px": length,
            "orientation": orientation
        })

    return walls


def merge_similar_walls(walls, threshold=10):
    """
    Merge nearby parallel walls (basic version)

    Args:
        walls: list of walls
        threshold: distance threshold

    Returns:
        merged walls
    """

    merged = []

    for wall in walls:
        added = False

        for m in merged:
            if wall["orientation"] != m["orientation"]:
                continue

            # simple proximity check
            if abs(wall["start"][0] - m["start"][0]) < threshold and \
               abs(wall["start"][1] - m["start"][1]) < threshold:

                # merge by extending
                m["end"] = wall["end"]
                added = True
                break

        if not added:
            merged.append(wall)

    return merged