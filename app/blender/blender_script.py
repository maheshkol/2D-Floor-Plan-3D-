import bpy
import json
import sys
import math

# -----------------------------
# READ ARGUMENTS
# -----------------------------
argv = sys.argv
argv = argv[argv.index("--") + 1:]

json_path = argv[0]
output_path = argv[1]

# -----------------------------
# LOAD JSON
# -----------------------------
with open(json_path, "r") as f:
    data = json.load(f)

# -----------------------------
# CLEAR SCENE
# -----------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

SCALE = 0.1

# -----------------------------
# CREATE WALLS
# -----------------------------
for w in data.get("walls", []):
    pos = w["position"]
    dim = w["dimensions"]
    rot = w["rotation"]

    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.object

    obj.scale = (
        dim[0] * SCALE / 2,
        dim[1] * SCALE / 2,
        dim[2] * SCALE / 2
    )

    obj.location = (
        pos[0] * SCALE,
        pos[1] * SCALE,
        (dim[2] * SCALE) / 2
    )

    obj.rotation_euler[2] = rot[2]

# -----------------------------
# EXPORT GLB
# -----------------------------
bpy.ops.export_scene.gltf(filepath=output_path)

print("✅ GLB Exported:", output_path)