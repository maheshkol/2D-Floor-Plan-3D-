from backend.geometry.wall_geometry import process_walls

walls = [
    {"start": [0, 0], "end": [200, 0]},
    {"start": [200, 0], "end": [200, 300]}
]

scale = 0.02  # 1 pixel = 0.02 meters

result = process_walls(walls, scale)

print(result)