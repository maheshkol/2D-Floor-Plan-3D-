import os
from pdf2image import convert_from_path
from PIL import Image


def get_base_path():
    """
    Detect environment (Colab or Local)
    """
    if "COLAB_GPU" in os.environ:
        return "/content/drive/MyDrive/2D-FloorPlan-3D"
    else:
        return "G:/My Drive/2D-FloorPlan-3D"


def build_path(relative_path: str) -> str:
    """
    Build absolute path
    """
    base = get_base_path()
    return os.path.join(base, relative_path)


def convert_pdf_to_images(
    pdf_path: str,
    output_folder: str = "data/output/",
    dpi: int = 300,
    from_drive: bool = False,
    poppler_path: str = None
):
    """
    Convert PDF to images

    Args:
        pdf_path: input PDF path
        output_folder: where to save images
        dpi: resolution (higher = better quality)
        from_drive: if True, use Drive base path
        poppler_path: required for Windows

    Returns:
        list of saved image paths
    """

    # Resolve paths
    if from_drive:
        pdf_path = build_path(pdf_path)
        output_folder = build_path(output_folder)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF not found: {pdf_path}")

    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF → images
    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=poppler_path
    )

    saved_paths = []

    for i, img in enumerate(images):
        output_path = os.path.join(output_folder, f"page_{i+1}.png")

        img.save(output_path, "PNG")
        saved_paths.append(output_path)

    return saved_paths


def convert_first_page(
    pdf_path: str,
    output_path: str = "data/output/page_1.png",
    dpi: int = 300,
    from_drive: bool = False,
    poppler_path: str = None
):
    """
    Convert only first page (faster for floor plans)

    Returns:
        saved image path
    """

    if from_drive:
        pdf_path = build_path(pdf_path)
        output_path = build_path(output_path)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF not found: {pdf_path}")

    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        first_page=1,
        last_page=1,
        poppler_path=poppler_path
    )

    image = images[0]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, "PNG")

    return output_path