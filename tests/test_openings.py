from backend.preprocessing.image_loader import load_image
from backend.door_window_detection.detect_openings import OpeningDetector
import cv2

image = load_image("data/samples/sample.png", from_drive=True)

detector = OpeningDetector()
openings = detector.detect_openings(image)

print("Detected openings:", openings)

# draw boxes
for op in openings:
    x1, y1, x2, y2 = map(int, op["bbox"])
    cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)

cv2.imshow("Openings", image)
cv2.waitKey(0)
cv2.destroyAllWindows()