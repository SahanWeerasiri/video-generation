import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time

# Input coordinates for locations
locations = [
    {"name": "Colombo", "coords": [79.861244, 6.927079]},
    {"name": "Galle", "coords": [80.2210, 6.0535]},
    {"name": "Yala National Park", "coords": [81.5016, 6.3728]},
    {"name": "Trincomalee", "coords": [81.2330, 8.5774]},
    {"name": "Colombo", "coords": [79.861244, 6.927079]}  # Return to start
]

print("Initializing animation...")
start_time = time.time()

# Set up the map
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Set the extent of the map to cover all locations
lons = [loc["coords"][0] for loc in locations]
lats = [loc["coords"][1] for loc in locations]
ax.set_extent([min(lons)-1, max(lons)+1, min(lats)-1, max(lats)+1], crs=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Add markers for all locations
for loc in locations:
    ax.plot(loc["coords"][0], loc["coords"][1], 'ro', transform=ccrs.PlateCarree(), markersize=8)

# Animation function
line, = ax.plot([], [], 'b-', linewidth=2, transform=ccrs.PlateCarree())
point, = ax.plot([], [], 'bo', transform=ccrs.PlateCarree(), markersize=10)

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(frame):
    total_frames = 100 * (len(locations) - 1)
    current_segment = frame // 100
    progress_in_segment = (frame % 100) / 100

    start = locations[current_segment]["coords"]
    end = locations[current_segment + 1]["coords"]

    current_lon = start[0] + (end[0] - start[0]) * progress_in_segment
    current_lat = start[1] + (end[1] - start[1]) * progress_in_segment

    lons = [loc["coords"][0] for loc in locations[:current_segment+1]] + [current_lon]
    lats = [loc["coords"][1] for loc in locations[:current_segment+1]] + [current_lat]

    line.set_data(lons, lats)
    point.set_data(current_lon, current_lat)

    if frame % 10 == 0:
        progress = (frame + 1) / total_frames * 100
        elapsed_time = time.time() - start_time
        estimated_total_time = elapsed_time / (progress / 100)
        remaining_time = estimated_total_time - elapsed_time
        print(f"Progress: {progress:.1f}% | Estimated time remaining: {remaining_time:.1f} seconds")

    return line, point

total_frames = 100 * (len(locations) - 1)
print("Creating animation...")
anim = FuncAnimation(fig, animate, frames=total_frames, init_func=init, blit=True)

print("Saving animation as video...")
anim.save('map_transition.mp4', writer='ffmpeg', fps=30)
print("Video created successfully: map_transition.mp4")

total_time = time.time() - start_time
print(f"Total execution time: {total_time:.1f} seconds")

plt.close(fig)