def calculate_scale(reference_pixels, reference_meters):
    """
    Calculate scale factor

    Example:
        100 pixels = 5 meters
        scale = 0.05
    """
    return reference_meters / reference_pixels


def pixels_to_meters(value_px, scale):
    """
    Convert pixels → meters
    """
    return value_px * scale


def convert_point(point, scale):
    """
    Convert [x, y] from pixels → meters
    """
    return [point[0] * scale, point[1] * scale]