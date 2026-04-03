# backend/pipeline.py
import math
import os
import sys
from unittest import result

# 🔥 ADD PROJECT ROOT TO PATH (IMPORTANT)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from backend.preprocessing.image_loader import load_image, load_grayscale
from backend.preprocessing.image_Cleaning import clean_image_pipeline
from backend.preprocessing.pdf_to_image import convert_first_page

from backend.wall_detection.hough_transform import detect_lines
from backend.wall_detection.detect_walls import filter_walls, merge_similar_walls

from backend.door_window_detection.detect_openings import OpeningDetector

from backend.geometry.wall_geometry import process_walls
from backend.geometry.scaling import calculate_scale

from backend.jason_generator.generate_jason import generate_json

from backend.three_d.converter_2D_to_3D import generate_3d_scene




class FloorPlanPipeline:

    def __init__(self, model_path=None):
        """
        Initialize pipeline components
        """
        self.opening_detector = OpeningDetector(model_path)

    # -----------------------------
    # STEP 1: INPUT HANDLING
    # -----------------------------
    def handle_input(self, input_path, from_drive=False, poppler_path=None):
        """
        Handle PDF or image input
        """

        ext = input_path.lower().split(".")[-1]

        if ext == "pdf":
            image_path = convert_first_page(
                input_path,
                from_drive=from_drive,
                poppler_path=poppler_path
            )
        else:
            image_path = input_path

        return image_path

    # -----------------------------
    # STEP 2: LOAD + PREPROCESS
    # -----------------------------
    def preprocess(self, image_path, from_drive=False):
        """
        Load and clean image
        """

        image = load_image(image_path, from_drive=from_drive)
        gray = load_grayscale(image_path, from_drive=from_drive)

        edges = clean_image_pipeline(gray)

        return image, edges

    # -----------------------------
    # STEP 3: WALL DETECTION
    # -----------------------------
    def detect_walls(self, edges):
        """
        Detect walls from edges
        """

        lines = detect_lines(edges)

        walls = filter_walls(lines)
        walls = merge_similar_walls(walls)

        return walls

    # -----------------------------
    # STEP 4: OPENING DETECTION
    # -----------------------------
    def detect_openings(self, image):
        """
        Detect doors/windows
        """
        return self.opening_detector.detect_openings(image)

    # -----------------------------
    # STEP 5: GEOMETRY
    # -----------------------------
    def process_geometry(self, walls, scale):
        """
        Convert to real-world geometry
        """
        return process_walls(walls, scale)

    # -----------------------------
    # STEP 6: JSON GENERATION
    # -----------------------------
    def generate_output_json(self, walls, openings, scale):
        """
        Generate structured JSON
        """
        return generate_json(walls, openings, scale)

    # -----------------------------
    # STEP 7: 3D CONVERSION
    # -----------------------------
    def generate_3d(self, json_data):
        """
        Convert JSON → 3D scene
        """
        return generate_3d_scene(json_data)

    # -----------------------------
    # FULL PIPELINE
    # -----------------------------
    def run(
        self,
        input_path,
        from_drive=False,
        scale_px_to_m=0.02,
        poppler_path=None
    ):
        """
        Run full pipeline

        Args:
            input_path: PDF or image path
            from_drive: use Google Drive path
            scale_px_to_m: conversion factor
            poppler_path: required for Windows PDF

        Returns:
            dict with all outputs
        """

        print("🚀 Starting pipeline...")

        # Step 1: Handle input
        image_path = self.handle_input(
            input_path,
            from_drive=from_drive,
            poppler_path=poppler_path
        )

        # Step 2: Preprocess
        image, edges = self.preprocess(image_path, from_drive)

        # Step 3: Walls
        walls = self.detect_walls(edges)
        print(f"✅ Walls detected: {len(walls)}")

        # Step 4: Openings
        openings = self.detect_openings(image)
        print(f"✅ Openings detected: {len(openings)}")

        # Step 5: Geometry
        walls_geo = self.process_geometry(walls, scale_px_to_m)

        # Step 6: JSON
        json_output = self.generate_output_json(
            walls_geo,
            openings,
            scale_px_to_m
        )

        # Step 7: 3D Scene
        scene_3d = self.generate_3d(json_output)
        scene_3d = self.generate_3d(json_output)

        # -----------------------------
        # 🔥 ADD DOORS & WINDOWS (TEMP FIX)
        # -----------------------------
        if "openings" not in scene_3d:
            scene_3d["openings"] = []

        # If YOLO didn't detect properly → add sample openings
        if not scene_3d["openings"]:
            scene_3d["openings"] = [
                {"type": "door", "position": [5, 2], "width": 1.0, "height": 2.2},
                {"type": "window", "position": [8, 4], "width": 1.5, "height": 1.2}
        ]

        print(f"✅ Openings added to scene_3d: {len(scene_3d['openings'])}")
        
        print("🎉 Pipeline completed!")

        scene_walls = []

        # -----------------------------
        # 🔥 SCALE (VERY IMPORTANT)
        # -----------------------------
        SCALE = 0.01

        # -----------------------------
        # 🔥 FIND CENTER (IMPORTANT)
        # -----------------------------

        xs = []
        ys = []

        for wall in walls:
            xs.extend([wall["start"][0], wall["end"][0]])
            ys.extend([wall["start"][1], wall["end"][1]])

        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)

        # -----------------------------
        # 🔥 CREATE WALLS
        # -----------------------------
        for wall in walls:
            x1, y1 = wall["start"]
            x2, y2 = wall["end"]

            # length
            length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            # centered position
            cx = ((x1 + x2) / 2) - center_x
            cy = ((y1 + y2) / 2) - center_y

            # angle
            angle = math.atan2(y2 - y1, x2 - x1)

            scene_walls.append({
                "position": [cx * SCALE, cy * SCALE, 0],
                "dimensions": [length * SCALE, 0.5, 3],  # 🔥 thicker wall
                "rotation": [0, 0, angle]
            })

        # -----------------------------
        # FINAL 3D SCENE
        # -----------------------------
        scene_3d = {
            "walls": scene_walls,
            "openings": [
                {"type": "door", "position": [0, 0, 0], "width": 1.2, "height": 2.2},
                {"type": "window", "position": [2, 2, 1.2], "width": 1.5, "height": 1.2}
        ]
}


            # ADD DOORS & WINDOWS (TEMP FIX)
        return{
            "image_path": image_path,
            "walls_raw": walls,
            "walls_geo": walls_geo,
            "openings": openings,
            "json": json_output,
            "scene_3d": scene_3d
        }