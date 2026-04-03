import bpy
import json
import sys
import math
import os
import sys

argv = sys.argv

if "--" in argv:
    argv = argv[argv.index("--") + 1:]
else:
    argv = []

if len(argv) < 2:
    raise Exception("❌ Missing arguments")

json_path = argv[0]
output_path = argv[1]

print("JSON PATH:", json_path)
print("OUTPUT PATH:", output_path)

def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)

    return mat

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

print("Walls count:", len(data.get("walls", [])))

# -----------------------------
# CLEAR SCENE
# -----------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

SCALE = 0.1

# CREATE MATERIAL FUNCTION
# -----------------------------
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)

    return mat

# -----------------------------
# MATERIALS
# -----------------------------
wall_mat = create_material("WallMat", (0.8, 0.8, 0.8))   # gray
door_mat = create_material("DoorMat", (0.55, 0.27, 0.07)) # brown
window_mat = create_material("WindowMat", (0.2, 0.6, 1.0)) # blue


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
    obj.data.materials.clear()
    obj.data.materials.append(wall_mat)
    print("Creating wall:", pos, dim)

# -----------------------------
# CREATE DOORS
# -----------------------------
for d in data.get("openings", []):
    if d.get("type") != "door":
        continue

    pos = d.get("position", [0, 0])
    if len(pos) == 3:
        x, y = pos[0], pos[1]
    else:
        x, y = pos

    width = d.get("width", 1.0)
    height = d.get("height", 2.2)

    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.object

    obj.scale = (
        width * SCALE / 2,
        0.2 * SCALE,
        height * SCALE / 2
    )

    obj.location = (
        x * SCALE,
        y * SCALE,
        height * SCALE / 2
    )

    obj.data.materials.clear()
    obj.data.materials.append(door_mat)

# -----------------------------
# CREATE WINDOWS
# -----------------------------
for w in data.get("openings", []):
    if w.get("type") != "window":
        continue

    pos = w.get("position", [0, 0])
    if len(pos) == 3:
        x, y = pos[0], pos[1]
    else:
        x, y = pos

    width = w.get("width", 1.5)
    height = w.get("height", 1.2)

    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.object

    obj.scale = (
        width * SCALE / 2,
        0.1 * SCALE,
        height * SCALE / 2
    )

    obj.location = (
        x * SCALE,
        y * SCALE,
        (height * SCALE) + 1   # slightly above ground
    )

    obj.data.materials.clear()
    obj.data.materials.append(window_mat)
    
# -----------------------------
# EXPORT GLB
# -----------------------------
bpy.ops.export_scene.gltf(filepath=output_path)

# -----------------------------
# ENSURE OUTPUT DIRECTORY EXISTS
# -----------------------------
output_dir = os.path.dirname(output_path)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Export path:", output_path)

# -----------------------------
# SELECT ALL OBJECTS
# -----------------------------
bpy.ops.object.select_all(action='SELECT')

# -----------------------------
# EXPORT GLB (FIXED)
# -----------------------------
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    use_selection=False  # 🔥 IMPORTANT
)

print("Walls:", len(data.get("walls", [])))
print("Openings:", len(data.get("openings", [])))
print("✅ GLB Export Completed")
print("✅ GLB Exported:", output_path)