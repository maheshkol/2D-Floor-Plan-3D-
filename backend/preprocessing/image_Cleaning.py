import cv2
import numpy as np


def remove_noise(image, method="gaussian"):
    """
    Remove noise from image
    """
    if image is None:
        raise ValueError("❌ Image is None in remove_noise")

    if method == "gaussian":
        return cv2.GaussianBlur(image, (5, 5), 0)

    elif method == "median":
        return cv2.medianBlur(image, 5)

    else:
        raise ValueError("Invalid noise removal method")


def apply_threshold(image, method="adaptive"):
    """
    Convert image to binary
    """
    if method == "adaptive":
        return cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )

    elif method == "otsu":
        _, thresh = cv2.threshold(
            image,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        return thresh

    else:
        raise ValueError("Invalid threshold method")


def detect_edges(image, low=50, high=150):
    """
    Detect edges using Canny
    """
    return cv2.Canny(image, low, high)


def morphological_operations(image):
    """
    Improve structure using morphology
    """
    kernel = np.ones((3, 3), np.uint8)

    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)
    dilated = cv2.dilate(closed, kernel, iterations=1)

    return dilated


# 🔥 FIXED FUNCTION (MAIN ISSUE WAS HERE)
def clean_image_pipeline(image):

    if image is None:
        raise ValueError("❌ Image is None")

    # ✅ FIX: handle all cases properly
    if len(image.shape) == 3:
        if image.shape[2] == 3:
            # BGR image → convert
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif image.shape[2] == 1:
            # already grayscale → squeeze
            image = image[:, :, 0]

    # DEBUG
    print("✅ Final image shape:", image.shape)

    # Step 1
    denoised = remove_noise(image)

    # Step 2
    binary = apply_threshold(denoised)

    # Step 3
    morphed = morphological_operations(binary)

    # Step 4
    edges = detect_edges(morphed)

    return edges