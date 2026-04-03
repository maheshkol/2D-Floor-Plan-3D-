import math


def calculate_angle(x1, y1, x2, y2):
    """
    Calculate angle of line in degrees
    """
    return math.degrees(math.atan2(y2 - y1, x2 - x1))


def get_orientation(x1, y1, x2, y2, threshold=10):
    """
    Classify orientation of line

    Returns:
        "horizontal", "vertical", or "other"
    """

    angle = calculate_angle(x1, y1, x2, y2)

    if abs(angle) < threshold:
        return "horizontal"
    elif abs(abs(angle) - 90) < threshold:
        return "vertical"
    else:
        return "other"