import os
import cv2


def get_base_path():
    """
    Detect environment (Colab or Local)
    """
    if "COLAB_GPU" in os.environ:
        return "/content/drive/MyDrive/2D-FloorPlan-3D"
    else:
        return "G:/My Drive/2D-FloorPlan-3D"  # change if needed


def build_path(relative_path: str) -> str:
    """
    Build absolute path using base path
    """
    base = get_base_path()
    return os.path.join(base, relative_path)


def load_image(image_path: str, from_drive: bool = False):
    """
    Load image from path

    Args:
        image_path (str): relative or absolute path
        from_drive (bool): if True, treat path as relative to Drive

    Returns:
        image (numpy array)
    """

    if from_drive:
        image_path = build_path(image_path)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found: {image_path}")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"❌ Failed to load image: {image_path}")

    return image


def load_grayscale(image_path: str, from_drive: bool = False):
    """
    Load image in grayscale
    """
    if from_drive:
        image_path = build_path(image_path)

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(f"❌ Failed to load grayscale image: {image_path}")

    return image


def resize_image(image, width: int = 1024):
    """
    Resize image maintaining aspect ratio
    """
    h, w = image.shape[:2]

    if w <= width:
        return image

    ratio = width / w
    new_dim = (width, int(h * ratio))

    resized = cv2.resize(image, new_dim, interpolation=cv2.INTER_AREA)

    return resized


def normalize_image(image):
    """
    Normalize pixel values (0–1)
    """
    return image / 255.0