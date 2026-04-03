from backend.preprocessing.pdf_to_image import convert_first_page

pdf_path = "data/samples/sample.pdf"

image_path = convert_first_page(
    pdf_path,
    from_drive=True,
    poppler_path="C:/poppler/Library/bin"  # Windows only
)

print("✅ Converted:", image_path)