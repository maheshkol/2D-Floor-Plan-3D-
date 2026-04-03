import streamlit as st

def show_3d_model(model_url):
    viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128/examples/js/loaders/GLTFLoader.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body style="margin:0;">
        <div id="container"></div>

        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, 500);
            document.getElementById("container").appendChild(renderer.domElement);

            const light = new THREE.HemisphereLight(0xffffff, 0x444444);
            scene.add(light);

            const loader = new THREE.GLTFLoader();
            loader.load("{model_url}", function(gltf) {{
                scene.add(gltf.scene);
            }});

            camera.position.z = 5;

            const controls = new THREE.OrbitControls(camera, renderer.domElement);

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

    st.components.v1.html(viewer_html, height=500)
