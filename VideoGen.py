import folium
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import time

# Input coordinates for locations
locations = [
    {"name": "Colombo", "coords": [6.927079, 79.861244]},
    {"name": "Galle", "coords": [6.0535, 80.2210]},
    {"name": "Yala National Park", "coords": [6.3728, 81.5016]},
    {"name": "Trincomalee", "coords": [8.5774, 81.2330]},
    {"name": "Colombo", "coords": [6.927079, 79.861244]}  # Return to start
]

def create_map(location, zoom):
    m = folium.Map(location=location, zoom_start=zoom, tiles='OpenStreetMap')
    for i, loc in enumerate(locations):
        folium.Marker(
            loc["coords"], 
            popup=f'{loc["name"]} - Day {i+1}', 
            icon=folium.Icon(color='green' if i == 0 else 'red')
        ).add_to(m)
    return m

def map_to_image(m):
    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    return img

print("Initializing animation...")
start_time = time.time()

total_frames = 100 * (len(locations) - 1)
frames = []

for frame in range(total_frames):
    current_segment = frame // 100
    progress_in_segment = (frame % 100) / 100

    start = locations[current_segment]["coords"]
    end = locations[current_segment + 1]["coords"]

    current_lat = start[0] + (end[0] - start[0]) * progress_in_segment
    current_lon = start[1] + (end[1] - start[1]) * progress_in_segment

    # Calculate zoom level (zoom out, then in)
    max_zoom = 12
    min_zoom = 6
    if progress_in_segment <= 0.5:
        zoom = max_zoom + (min_zoom - max_zoom) * (progress_in_segment * 2)
    else:
        zoom = min_zoom + (max_zoom - min_zoom) * ((progress_in_segment - 0.5) * 2)

    m = create_map([current_lat, current_lon], zoom)
    img = map_to_image(m)
    frames.append(img)

    # Print progress
    if frame % 10 == 0:
        progress = (frame + 1) / total_frames * 100
        elapsed_time = time.time() - start_time
        estimated_total_time = elapsed_time / (progress / 100)
        remaining_time = estimated_total_time - elapsed_time
        print(f"Progress: {progress:.1f}% | Estimated time remaining: {remaining_time:.1f} seconds")

print("Saving animation as video...")
frames[0].save('map_transition.gif', save_all=True, append_images=frames[1:], duration=50, loop=0)
print("Video created successfully: map_transition.gif")

total_time = time.time() - start_time
print(f"Total execution time: {total_time:.1f} seconds")