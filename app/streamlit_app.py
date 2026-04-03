import streamlit as st
import json
import tempfile
import os
from PIL import Image
import cv2
import numpy as np
import sys
import io
import subprocess
import tempfile

from ultralytics import YOLO

# 🔥 ADD PROJECT ROOT TO PATH (IMPORTANT)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from backend.pipeline import FloorPlanPipeline

# Add project root to Python path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
# SIDEBAR SETTINGS
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

def run_blender(scene_json_path, output_glb_path):
    blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
    
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    script_path = os.path.join(BASE_DIR, "blender", "blender_script.py")
    #script_path = r"C:\Users\Mahesh\Documents\PROJECTS\2D-Floor-Plan-3D\blender_script.py"

    command = [
        blender_exe,
        "--background",  # run without UI
        "--python", script_path,
        "--",
        scene_json_path,
        output_glb_path
    ]

    subprocess.run(command, check=True)

    data_dir = os.path.join(BASE_DIR, "data")

    os.makedirs(data_dir, exist_ok=True)

    json_path = os.path.join(data_dir, "scene.json")
    glb_path = os.path.join(data_dir, "model.glb")

    # -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file is not None:

    # ✅ READ FILE ONLY ONCE
    file_bytes = uploaded_file.read()

    # DEBUG
    st.write(f"📦 Uploaded file size: {len(file_bytes)} bytes")

    if len(file_bytes) == 0:
        st.error("❌ Uploaded file is empty")
        st.stop()

    # SHOW IMAGE
    image = Image.open(io.BytesIO(file_bytes))
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Show uploaded image
    #image = Image.open(uploaded_file)
    #st.image(image, caption="📷 Uploaded Image", use_container_width=True)

    # SAVE TEMP FILE SAFELY
    temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)

    with open(temp_path, "wb") as f:
        f.write(file_bytes)
    
    #with open(temp_path, "wb", encoding="utf-8") as f:
        #f.write(file_bytes)
        
    # Save temp file
    #with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
    #    tmp.write(uploaded_file.read())
    #    temp_path = tmp.name

    import os
    file_size = os.path.getsize(temp_path)
    st.write(f"💾 Saved file size: {file_size} bytes")

    if file_size == 0:
        st.error("❌ Temp file is empty → stopping")
        st.stop()

        
    # -----------------------------
    # PIPELINE INIT
    # -----------------------------
    #pipeline = clean_image_pipeline(temp_path)
    #if os.path.exists(temp_path):
    #    cleaned = clean_image_pipeline(temp_path)
    #else:
    #    st.error("File not saved properly")

    # -----------------------------
    # YOLO PREVIEW (NEW 🔥)
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

        st.write("📂 YOLO input path:", temp_path)
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

                # ✅ DEBUG BLOCK
                st.subheader("🔍 Debug Scene Data")
                st.json(result["scene_3d"])

            except Exception as e:
                st.error(f"❌ Pipeline Error: {e}")
                st.stop()
            
            json_path = os.path.join(tempfile.gettempdir(), "scene.json")
            glb_path = os.path.join(tempfile.gettempdir(), "model.glb")

            # Save JSON
            with open(json_path, "w") as f:
                json.dump(result["scene_3d"], f)

            # Run Blender
            run_blender(json_path, glb_path)

            st.success("✅ 3D Model Generated")

        # -----------------------------
        # TABS
        # -----------------------------
        tab1, tab2, tab3 = st.tabs(["🧱 Walls", "📄 JSON", "🎮 3D View"])

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
            # TAB 3: 3D VIEW (BLENDER BASED)
            # -----------------------------
        with tab3:
            st.subheader("🎮 3D Visualization (Rotate / Zoom / Pan)")

            if "scene_3d" not in result or not result["scene_3d"]:
                st.error("❌ No 3D data generated")
                st.stop()

            import os, json, base64, tempfile

            # -----------------------------
            # PATHS
            # -----------------------------
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))

            blender_script = os.path.join(BASE_DIR, "blender", "blender_script.py")
            blender_exe = r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"

            temp_dir = tempfile.gettempdir()
            json_path = os.path.join(temp_dir, "scene.json")
            glb_path = os.path.join(temp_dir, "model.glb")

            # -----------------------------
            # SAVE JSON
            # -----------------------------
            with open(json_path, "w") as f:
                json.dump(result["scene_3d"], f)
            
           
            # -----------------------------
            # RUN BLENDER
            # -----------------------------
            import subprocess

            command = [
                blender_exe,
                "--background",
                "--python", blender_script,
                "--",
                json_path,
                glb_path
        ]

            try:
                subprocess.run(command, check=True)
                st.success("✅ 3D Model Generated")
            except Exception as e:
                st.error(f"❌ Blender Error: {e}")
                st.stop()

            # -----------------------------
            # LOAD GLB → BASE64
            # -----------------------------
            if not os.path.exists(glb_path):
                st.error("❌ GLB file not created")
                st.stop()

            with open(glb_path, "rb") as f:
                glb_bytes = f.read()

            glb_base64 = base64.b64encode(glb_bytes).decode()

            # -----------------------------
            # MODEL VIEWER (FULL CONTROL)
            # -----------------------------
            html_3d = f"""
            <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

            <model-viewer 
                src="data:model/gltf-binary;base64,{glb_base64}"
                alt="3D Floor Plan"
                camera-controls
                auto-rotate
                style="width: 100%; height: 600px;"
                exposure="1"
                shadow-intensity="1"
                camera-orbit="45deg 60deg 10m"
            >
            </model-viewer>
            """

            st.components.v1.html(html_3d, height=650)
