# backend/door_window_detection/detect_openings.py

from backend.door_window_detection.yolo_model import YOLODetector


class OpeningDetector:
    def __init__(self, model_path=None):
        self.detector = YOLODetector(model_path)

    def detect_openings(self, image, conf_threshold=0.3):
        """
        Detect doors and windows

        Args:
            image: input image
            conf_threshold: minimum confidence

        Returns:
            openings list
        """

        detections = self.detector.detect(image)

        openings = []

        for det in detections:
            label = det["label"].lower()
            conf = det["confidence"]

            if conf < conf_threshold:
                continue

            if label not in ["door", "window"]:
                continue

            x1, y1, x2, y2 = det["bbox"]

            width = x2 - x1
            height = y2 - y1

            openings.append({
                "type": label,
                "bbox": [x1, y1, x2, y2],
                "width_px": width,
                "height_px": height,
                "center": [
                    (x1 + x2) / 2,
                    (y1 + y2) / 2
                ]
            })

        return openings