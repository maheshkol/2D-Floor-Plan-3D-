# backend/three_d/converter_2d_to_3d.py

from backend.three_d.mesh_builder import create_wall_mesh, create_opening_mesh


def convert_walls_to_3d(walls):
    """
    Convert all walls to 3D meshes
    """

    wall_meshes = []

    for wall in walls:
        mesh = create_wall_mesh(
            wall["start"],
            wall["end"]
        )

        wall_meshes.append(mesh)

    return wall_meshes


def convert_openings_to_3d(walls):
    """
    Convert all doors/windows to 3D meshes
    """

    opening_meshes = []

    for wall in walls:

        for door in wall.get("doors", []):
            door["type"] = "door"
            opening_meshes.append(create_opening_mesh(door))

        for window in wall.get("windows", []):
            window["type"] = "window"
            opening_meshes.append(create_opening_mesh(window))

    return opening_meshes


def generate_3d_scene(json_data):
    """
    Main function to generate full 3D scene

    Args:
        json_data: output from JSON generator

    Returns:
        scene dict
    """

    walls = json_data["walls"]

    wall_meshes = convert_walls_to_3d(walls)
    opening_meshes = convert_openings_to_3d(walls)

    scene = {
        "walls": wall_meshes,
        "openings": opening_meshes
    }

    return scene