import cv2
import numpy as np


def detect_lines(edges, rho=1, theta=np.pi/180, threshold=100,
                 min_line_length=50, max_line_gap=10):
    """
    Detect lines using Probabilistic Hough Transform

    Args:
        edges: edge-detected image
        rho: distance resolution
        theta: angle resolution
        threshold: minimum votes
        min_line_length: minimum line length
        max_line_gap: max gap between segments

    Returns:
        list of lines [(x1, y1, x2, y2)]
    """

    lines = cv2.HoughLinesP(
        edges,
        rho=rho,
        theta=theta,
        threshold=threshold,
        minLineLength=min_line_length,
        maxLineGap=max_line_gap
    )

    if lines is None:
        return []

    # Flatten structure
    return [line[0] for line in lines]


def draw_lines(image, lines, color=(0, 0, 255), thickness=2):
    """
    Draw detected lines on image (for debugging)
    """
    img_copy = image.copy()

    for (x1, y1, x2, y2) in lines:
        cv2.line(img_copy, (x1, y1), (x2, y2), color, thickness)

    return img_copy