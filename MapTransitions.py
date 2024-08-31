import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import time
from PIL import Image


def map_transitions(locations):
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
        point.set_data([current_lon], [current_lat])  # Wrap in list to make it a sequence

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

    print("Saving animation as GIF...")
    writer = PillowWriter(fps=30)
    anim.save('map_transition.gif', writer=writer)
    print("Animation created successfully: map_transition.gif")

    total_time = time.time() - start_time
    print(f"Total execution time: {total_time:.1f} seconds")

    plt.close(fig)
    ###########################################################################
    #Split the GIF
    ###########################################################################
    from PIL import Image
    import os

    # Open the original GIF
    gif_path = 'map_transition.gif'
    original_gif = Image.open(gif_path)

    # Number of frames per path (100 as per your animation settings)
    frames_per_path = 100
    total_paths = len(locations) - 1  # Each segment between locations

    # Create output directory for the split GIFs
    output_dir = "split_gifs"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize an empty list to store GIF paths
    gif_paths = []

    # Loop through each path segment
    for path_index in range(total_paths):
        # Calculate the start and end frame indices for this path segment
        start_frame = path_index * frames_per_path
        end_frame = start_frame + frames_per_path

        # Create a list to store the frames for this segment
        frames = []

        # Extract frames for the current path segment
        original_gif.seek(start_frame)
        for frame_num in range(frames_per_path):
            try:
                frame = original_gif.copy()
                frames.append(frame)
                original_gif.seek(original_gif.tell() + 1)
            except EOFError:
                break

        # Save frames as a new GIF for this path segment
        segment_gif_path = os.path.join(output_dir, f"path_{path_index + 1}.gif")
        frames[0].save(
            segment_gif_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=original_gif.info['duration'],
            disposal=2
        )

        # Append the path to the gif_paths list
        gif_paths.append(segment_gif_path)

        print(f"GIF for path {path_index + 1} saved: {segment_gif_path}")

    print("All path GIFs created successfully.")
    return gif_paths