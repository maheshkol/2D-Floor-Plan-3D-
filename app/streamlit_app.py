import streamlit as st
import json
import tempfile
import os
from PIL import Image
import cv2
import numpy as np
import sys
import io

from ultralytics import YOLO

# 🔥 ADD PROJECT ROOT TO PATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from backend.pipeline import FloorPlanPipeline

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="2D Floor Plan → 3D",
    layout="wide"
)

MODEL_PATH = "https://huggingface.co/maheshkol/2D-FLOOR-PLAN-3D/resolve/main/best.pt"

# -----------------------------
# LOAD MODEL (CACHE)
# -----------------------------
@st.cache_resource
def load_model():
    try:
        return YOLO(MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

# -----------------------------
# UI TITLE
# -----------------------------
st.title("🏠 2D Floor Plan to 3D Converter")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Settings")

scale = st.sidebar.slider(
    "Pixel to Meter Scale",
    min_value=0.001,
    max_value=0.1,
    value=0.02,
    step=0.001
)

confidence = st.sidebar.slider(
    "Detection Confidence",
    0.1, 0.9, 0.3
)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Floor Plan (PNG, JPG, PDF)",
    type=["png", "jpg", "jpeg", "pdf"]
)

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file is not None:

    # Read file once
    file_bytes = uploaded_file.read()

    if len(file_bytes) == 0:
        st.error("❌ Uploaded file is empty")
        st.stop()

    # Show image
    image = Image.open(io.BytesIO(file_bytes))
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Save temp file
    temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    if os.path.getsize(temp_path) == 0:
        st.error("❌ Temp file is empty")
        st.stop()

    # -----------------------------
    # YOLO PREVIEW
    # -----------------------------
    if model is not None:
        st.subheader("🔍 Detection Preview")

        results = model.predict(
            source=temp_path,
            conf=confidence,
            save=False
        )

        annotated = results[0].plot()
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        st.image(annotated, caption="YOLO Detection", use_container_width=True)

    # -----------------------------
    # RUN PIPELINE
    # -----------------------------
    pipeline = FloorPlanPipeline()

    if st.button("🚀 Run Full Pipeline"):

        with st.spinner("Processing..."):
            try:
                result = pipeline.run(
                    input_path=temp_path,
                    from_drive=False,
                    scale_px_to_m=scale
                )

                st.success("✅ Processing Complete!")

                # ✅ STORE DATA FOR 3D PAGE
                st.session_state["walls_for_3d"] = result["walls_geo"]
                st.session_state["scene_3d"] = result["scene_3d"]

                # Debug
                st.subheader("🔍 Debug Scene Data")
                st.json(result["scene_3d"])

            except Exception as e:
                st.error(f"❌ Pipeline Error: {e}")
                st.stop()

        # -----------------------------
        # TABS (CLEAN)
        # -----------------------------
        tab1, tab2 = st.tabs(["🧱 Walls", "📄 JSON"])

        # -----------------------------
        # TAB 1: WALLS
        # -----------------------------
        with tab1:
            st.subheader("Detected Walls")
            st.metric("Total Walls", len(result["walls_geo"]))
            st.json(result["walls_geo"])

        # -----------------------------
        # TAB 2: JSON
        # -----------------------------
        with tab2:
            st.subheader("Generated JSON")

            st.json(result["json"])

            json_str = json.dumps(result["json"], indent=2)

            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name="floor_plan.json",
                mime="application/json"
            )

        # -----------------------------
        # NAVIGATION TO 3D PAGE
        # -----------------------------
        st.info("👉 Open '3D Viewer' from sidebar to see interactive 3D")

        if st.button("🚀 Open 3D Viewer"):
            st.switch_page("pages/3d_viewer.py")
