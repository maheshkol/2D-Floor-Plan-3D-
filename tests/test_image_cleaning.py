from backend.preprocessing.image_loader import load_grayscale
from backend.preprocessing.image_cleaning import clean_image_pipeline
import cv2

image = load_grayscale("data/samples/sample.png", from_drive=True)

edges = clean_image_pipeline(image)

cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()