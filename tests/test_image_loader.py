from backend.preprocessing.image_loader import load_image

image = load_image("data/samples/sample.png", from_drive=True)

print("✅ Image loaded successfully")
print("Shape:", image.shape)