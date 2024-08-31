import folium
import io
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib

matplotlib.use('Agg')  # Use Agg backend to avoid GUI

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

# Calculate the bounding box for all locations
lats = [loc["coords"][0] for loc in locations]
lons = [loc["coords"][1] for loc in locations]
min_lat, max_lat = min(lats), max(lats)
min_lon, max_lon = min(lons), max(lons)

# Create the animation
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')

def animate(frame):
    ax.clear()
    ax.axis('off')
    
    total_frames = 100 * (len(locations) - 1)
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
    ax.imshow(img)
    return ax,

anim = FuncAnimation(fig, animate, frames=100 * (len(locations) - 1), interval=50, blit=True)

# Save the animation as a video
anim.save('map_transition.mp4', writer='ffmpeg', fps=20)
print("Video created successfully: map_transition.mp4")

plt.close(fig)