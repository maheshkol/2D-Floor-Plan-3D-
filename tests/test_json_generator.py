from backend.json_generator.generate_json import generate_json

walls = [
    {
        "wall_id": "wall_1",
        "type": "interior",
        "start": [0, 0],
        "end": [5, 0],
        "length_m": 5,
        "orientation": "horizontal",
        "doors": [],
        "windows": []
    }
]

openings = [
    {
        "type": "door",
        "bbox": [10, 10, 50, 60],
        "width_px": 40,
        "height_px": 50,
        "center": [30, 30]
    }
]

scale = 0.05

result = generate_json(walls, openings, scale)

print(result)