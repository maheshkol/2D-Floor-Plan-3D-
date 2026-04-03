# backend/door_window_detection/yolo_model.py

from ultralytics import YOLO
import os


class YOLODetector:
    def __init__(self, model_path=None):
        """
        Initialize YOLO model

        Args:
            model_path: path to trained YOLO model
        """

        if model_path is None:
            # default pretrained (you will replace later)
            self.model = YOLO("yolov8n.pt")
        else:
            self.model = YOLO(model_path)

    def detect(self, image):
        """
        Run detection on image

        Args:
            image: numpy array

        Returns:
            detections list
        """

        results = self.model(image)

        detections = []

        for result in results:
            boxes = result.boxes

            if boxes is None:
                continue

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                label = self.model.names[cls]

                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "label": label
                })

        return detections