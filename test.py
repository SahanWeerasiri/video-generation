from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import *
import random

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from matplotlib.patches import Circle

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from matplotlib.patches import Circle
import numpy as np
from PIL import Image
from io import BytesIO

def create_location_maps(locations):
    # Load Sri Lanka map data from Natural Earth
    url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
    world = gpd.read_file(url)
    sri_lanka = world[world.ADMIN == 'Sri Lanka']

    maps = {}

    for location, coords in locations.items():
        # Create a GeoDataFrame for the location point
        location_point = gpd.GeoDataFrame({'name': [location]}, geometry=[Point(coords)], crs="EPSG:4326")

        # Set up the plot
        fig, ax = plt.subplots(figsize=(12, 12))

        # Plot Sri Lanka
        sri_lanka.plot(ax=ax, color='none', edgecolor='black')

        # Add contextily basemap
        ctx.add_basemap(ax, crs=sri_lanka.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

        # Plot the location point
        location_point.plot(ax=ax, color='red', markersize=100, marker='o')

        # Add a circle around the point for emphasis
        circle = Circle((coords[0], coords[1]), 0.2, fill=False, color='red', linewidth=2, transform=ax.transData)
        ax.add_patch(circle)

        # Customize the plot
        ax.set_title(f"Location: {location}", fontsize=16, fontweight='bold')
        ax.text(coords[0], coords[1]-0.3, location, fontsize=12, ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        # Remove axis labels and ticks
        ax.set_axis_off()

        # Adjust the map extent to focus on Sri Lanka
        ax.set_xlim(sri_lanka.total_bounds[0]-0.5, sri_lanka.total_bounds[2]+0.5)
        ax.set_ylim(sri_lanka.total_bounds[1]-0.5, sri_lanka.total_bounds[3]+0.5)

        # Save the figure to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        
        # Convert to ImageClip
        maps[location] = ImageClip(np.array(Image.open(img_buffer)))
        plt.close()

    return maps

# Example usage
locations = {
    'Colombo': (79.8612, 6.9271),
    'Kandy': (80.6337, 7.2906),
    'Galle': (80.2170, 6.0535),
}
def create_memory_video_with_detailed_map(input_data, background_music, intro_video, outro_video, output_file="memory_video.mp4"):
    # Load intro and outro videos
    intro = VideoFileClip(intro_video)
    outro = VideoFileClip(outro_video)

    # Create location maps
    locations = {location: (random.uniform(79.5, 81.5), random.uniform(5.5, 9.5)) for location in input_data.keys()}
    location_maps = create_location_maps(locations)

    # Prepare main content with map transitions
    main_content = []
    for i, (location, files) in enumerate(input_data.items()):
        # Prepare location content
        location_content = prepare_media_files({location: files})
        location_content_with_transitions = apply_transitions(location_content)

        # Create map to location transition
        map_clip = location_maps[location].set_duration(3)
        map_to_location = create_zoom_transition(map_clip, location_content_with_transitions[0])

        # Add map to location transition and location content
        main_content.append(map_to_location)
        main_content.extend(location_content_with_transitions)

        # Create location to map transition
        location_to_map = create_zoom_transition(location_content_with_transitions[-1], map_clip).fx(vfx.time_mirror)
        main_content.append(location_to_map)

        # If not the last location, add map movement to next location
        if i < len(locations) - 1:
            next_location = list(locations.keys())[i + 1]
            map_movement = animate_map_movement(location, next_location, location_maps)
            main_content.append(map_movement)

    # Combine everything
    final_video = concatenate_videoclips([intro] + main_content + [outro])

    # Add background music
    audio = AudioFileClip(background_music)
    final_audio = afx.audio_loop(audio, duration=final_video.duration)
    final_video = final_video.set_audio(final_audio)

    # Write the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
location_maps = create_location_maps(locations)