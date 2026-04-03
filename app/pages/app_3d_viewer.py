```python
import streamlit as st
import json

st.set_page_config(page_title="3D Floor Plan", layout="wide")

st.title("🏠 3D Floor Plan Viewer (No Blender 🚀)")
st.write("Visualize your detected walls in 3D using Three.js")

st.write("---")

# -----------------------------------
# 🔄 CONVERT WALL FORMAT
# -----------------------------------
def convert_walls(raw_walls):
    converted = []

    for wall in raw_walls:
        x1, y1 = wall["start"]
        x2, y2 = wall["end"]

        width = abs(x2 - x1)
        height = abs(y2 - y1)

        width = width if width > 0 else 0.2
        height = height if height > 0 else 0.2

        converted.append({
            "x": (x1 + x2) / 2,
            "y": (y1 + y2) / 2,
            "width": width,
            "height": height
        })

    return {"walls": converted}


# -----------------------------------
# 🎮 THREE.JS RENDERER
# -----------------------------------
def render_3d_floor(json_data):
    data = json.dumps(json_data)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body style="margin:0;">
        <div id="container"></div>

        <script>
            const data = {data};

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf5f5f5);

            const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
            camera.position.set(8, 8, 8);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, 500);
            document.getElementById("container").appendChild(renderer.domElement);

            const controls = new THREE.OrbitControls(camera, renderer.domElement);

            // Lighting
            const light = new THREE.HemisphereLight(0xffffff, 0x444444);
            scene.add(light);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
            directionalLight.position.set(5,10,7);
            scene.add(directionalLight);

            // Floor
            const floorGeo = new THREE.PlaneGeometry(20, 20);
            const floorMat = new THREE.MeshStandardMaterial({{ color: 0xdddddd }});
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = Math.PI / 2;
            scene.add(floor);

            // Grid
            const grid = new THREE.GridHelper(20, 20);
            scene.add(grid);

            // Walls
            data.walls.forEach(w => {{
                const geometry = new THREE.BoxGeometry(w.width, 2, w.height);
                const material = new THREE.MeshStandardMaterial({{ color: 0x888888 }});
                const wall = new THREE.Mesh(geometry, material);

                wall.position.set(w.x, 1, w.y);
                scene.add(wall);
            }});

            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}

            animate();
        </script>
    </body>
    </html>
    """

    st.components.v1.html(html_code, height=500)


# -----------------------------------
# 📥 INPUT OPTIONS
# -----------------------------------
st.subheader("📥 Input Options")

tab1, tab2 = st.tabs(["Upload JSON", "Use Sample"])

# 🔹 Upload JSON
with tab1:
    uploaded_file = st.file_uploader("Upload wall JSON", type=["json"])

    if uploaded_file:
        raw_data = json.load(uploaded_file)
        json_data = convert_walls(raw_data["walls"])

        st.success("✅ Loaded successfully")
        render_3d_floor(json_data)

# 🔹 Sample Data
with tab2:
    sample_data = {
        "walls": [
            {"start": [0, 0], "end": [5, 0]},
            {"start": [5, 0], "end": [5, 5]},
            {"start": [5, 5], "end": [0, 5]},
            {"start": [0, 5], "end": [0, 0]}
        ]
    }

    st.info("Showing sample floor plan")
    json_data = convert_walls(sample_data["walls"])
    render_3d_floor(json_data)
