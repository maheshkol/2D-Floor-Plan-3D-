from backend.three_d.converter_2d_to_3d import generate_3d_scene

json_data = {
    "walls": [
        {
            "start": [0, 0],
            "end": [5, 0],
            "doors": [
                {
                    "pos": [2, 0],
                    "width_m": 1,
                    "height_m": 2
                }
            ],
            "windows": []
        }
    ]
}

scene = generate_3d_scene(json_data)

print(scene)