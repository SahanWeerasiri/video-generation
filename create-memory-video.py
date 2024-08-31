from moviepy.editor import *
import random

def create_memory_video(input_data, background_music, intro_video, outro_video, output_file="memory_video.mp4"):
    # Load intro and outro videos
    intro = VideoFileClip(intro_video)
    outro = VideoFileClip(outro_video)

    # Prepare main content
    main_content = prepare_media_files(input_data)

    # Apply transitions to the main content
    main_content_with_transitions = apply_transitions(main_content)

    # Combine everything
    final_video = concatenate_videoclips([intro] + [main_content_with_transitions] + [outro])

    # Add background music
    audio = AudioFileClip(background_music)
    final_audio = afx.audio_loop(audio, duration=final_video.duration)
    final_video = final_video.set_audio(final_audio)

    # Write the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

def apply_transitions(clips, transition_duration=2):
    transitions = [
        'fade', 'fade_in', 'fade_out', 'slide_in', 'slide_out',
        'wipe_left', 'wipe_right', 'wipe_up', 'wipe_down'
    ]
    
    final_clips = [clips[0]]
    for i in range(1, len(clips)):
        transition = random.choice(transitions)
        current_clip = clips[i]
        previous_clip = clips[i-1]

        if transition == 'fade':
            clip = current_clip.crossfadein(transition_duration)
        elif transition == 'fade_in':
            clip = current_clip.fadein(transition_duration)
        elif transition == 'fade_out':
            clip = current_clip.fadeout(transition_duration)
        elif transition == 'slide_in':
            clip = CompositeVideoClip([
                previous_clip,
                current_clip.set_start(previous_clip.duration - transition_duration)
                    .set_position(lambda t: ('center', min(0, 1080*(t-1)/transition_duration)))
            ]).set_duration(previous_clip.duration)
        elif transition == 'slide_out':
            clip = CompositeVideoClip([
                current_clip,
                previous_clip.set_end(current_clip.start + transition_duration)
                    .set_position(lambda t: ('center', max(0, 1080*(1-t)/transition_duration)))
            ]).set_duration(current_clip.duration)
        elif transition == 'wipe_left':
            clip = CompositeVideoClip([
                previous_clip,
                current_clip.set_start(previous_clip.duration - transition_duration)
                    .set_position(lambda t: (min(1920, 1920*t/transition_duration), 'center'))
            ]).set_duration(previous_clip.duration)
        elif transition == 'wipe_right':
            clip = CompositeVideoClip([
                current_clip,
                previous_clip.set_end(current_clip.start + transition_duration)
                    .set_position(lambda t: (max(-1920, -1920*(1-t)/transition_duration), 'center'))
            ]).set_duration(current_clip.duration)
        elif transition == 'wipe_up':
            clip = CompositeVideoClip([
                previous_clip,
                current_clip.set_start(previous_clip.duration - transition_duration)
                    .set_position(lambda t: ('center', min(1080, 1080*t/transition_duration)))
            ]).set_duration(previous_clip.duration)
        elif transition == 'wipe_down':
            clip = CompositeVideoClip([
                current_clip,
                previous_clip.set_end(current_clip.start + transition_duration)
                    .set_position(lambda t: ('center', max(-1080, -1080*(1-t)/transition_duration)))
            ]).set_duration(current_clip.duration)
        
        final_clips.append(clip)
    
    return concatenate_videoclips(final_clips)

def prepare_media_files(input_data):
    clips = []
    for location, files in input_data.items():
        location_clips = []
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                clip = ImageClip(file).set_duration(3)  # Set each image to appear for 3 seconds
                clip = clip.resize(height=720)  # Resize to lower resolution (e.g., height=720)
            elif file.endswith(('.mp4', '.avi', '.mov')):
                clip = VideoFileClip(file).resize(height=720)  # Resize to lower resolution (e.g., height=720)
            else:
                continue
            location_clips.append(clip)
        clips.append(concatenate_videoclips(location_clips))
    return clips


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

    print("Maps are taken")

    maps = {}

    for location, coords in locations.items():
        print("A map is creating...")
        # Create a GeoDataFrame for the location point
        location_point = gpd.GeoDataFrame({'name': [location]}, geometry=[Point(coords)], crs="EPSG:4326")

        # Set up the plot
        fig, ax = plt.subplots(figsize=(8, 8))  # Use a square figure size to maintain aspect ratio

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

        # Adjust the map extent to focus on Sri Lanka and maintain aspect ratio
        ax.set_aspect('equal')  # Preserve aspect ratio
        ax.set_xlim(sri_lanka.total_bounds[0]-0.5, sri_lanka.total_bounds[2]+0.5)
        ax.set_ylim(sri_lanka.total_bounds[1]-0.5, sri_lanka.total_bounds[3]+0.5)

        # Save the figure to a BytesIO object
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        
        # Convert to ImageClip while preserving aspect ratio
        pil_image = Image.open(img_buffer)
        maps[location] = ImageClip(np.array(pil_image)).set_duration(3)  # Preserve aspect ratio by not resizing here
        plt.close()
        print("A map is done!")
    print("Maps are submitted")
    return maps

def animate_map_movement(start_location, end_location, location_maps, duration=2):
    start_map = location_maps[start_location].img  # Access the underlying image
    end_map = location_maps[end_location].img

    # Ensure they are PIL images
    if isinstance(start_map, np.ndarray):
        start_map = Image.fromarray(start_map)
    if isinstance(end_map, np.ndarray):
        end_map = Image.fromarray(end_map)
    
    # Resize and convert both images to the same size and mode
    size = (max(start_map.width, end_map.width), max(start_map.height, end_map.height))
    start_map = start_map.resize(size).convert("RGBA")
    end_map = end_map.resize(size).convert("RGBA")

    def make_frame(t):
        progress = t / duration
        blended_image = Image.blend(start_map, end_map, progress)
        return np.array(blended_image).astype(np.uint8)  # Convert to np.uint8

    print("Map movements are done!")
    return VideoClip(make_frame, duration=duration)




def create_zoom_transition(start_clip, end_clip, duration=3):
    w, h = start_clip.w, start_clip.h
    cropped_start_clips = []

    # Set fps for start_clip if it's an ImageClip or if fps is not set
    if not hasattr(start_clip, 'fps') or start_clip.fps is None:
        start_clip = start_clip.set_fps(24)  # Set FPS to 24 or any desired value

    # Set fps for end_clip if it's an ImageClip or if fps is not set
    if not hasattr(end_clip, 'fps') or end_clip.fps is None:
        end_clip = end_clip.set_fps(24)  # Set FPS to 24 or any desired value

    for t in np.linspace(0, 1, int(duration * start_clip.fps)):
        zoom_factor = 1 + 2 * t  # Adjust this value to control zoom speed
        crop_w = int(w / zoom_factor)
        crop_h = int(h / zoom_factor)
        x1 = int((w - crop_w) / 2)
        y1 = int((h - crop_h) / 2)
        cropped = (start_clip
                   .crop(x1=x1, y1=y1, width=crop_w, height=crop_h)
                   .resize(newsize=(w, h))
                   .set_duration(1/start_clip.fps))
        cropped_start_clips.append(cropped)
    
    zoomed_start = concatenate_videoclips(cropped_start_clips)
    
    def fade(t):
        return min(1, 2 * t / duration)
    
    faded_end = end_clip.set_start(duration/2).crossfadein(duration/2)
    
    return CompositeVideoClip([zoomed_start, faded_end]).set_duration(duration)


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
        map_to_location = create_zoom_transition(map_clip, location_content_with_transitions)

        # Add map to location transition and location content
        main_content.append(map_to_location)
        main_content.append(location_content_with_transitions)

        # Create location to map transition
        location_to_map = create_zoom_transition(location_content_with_transitions, map_clip).fx(vfx.time_mirror)
        main_content.append(location_to_map)

        # If not the last location, add map movement to next location
        if i < len(locations) - 1:
            next_location = list(locations.keys())[i + 1]
            map_movement = animate_map_movement(location, next_location, location_maps)
            main_content.append(map_movement)

    final_video = concatenate_videoclips([intro] + main_content + [outro])

    # Add background music
    audio = AudioFileClip(background_music)
    final_audio = afx.audio_loop(audio, duration=final_video.duration)
    final_video = final_video.set_audio(final_audio)

    # Resize final video to reduce memory usage
    final_video = final_video.resize(height=720)  # Resize output video to a smaller resolution (e.g., height=720)

    # Write the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

input_data = {
    'Colombo': ['1.jpg', '2.jpg'],
    'Galle': ['3.jpg', 'entry_clip.mp4'],
    'Kandy': ['4.jpg', '5.jpg']
}

background_music = "pop_track_1.mp3"
intro_video = "entry_clip.mp4"
outro_video = "end_clip.mp4"

locations = {
    'Colombo': (79.8612, 6.9271),
    'Kandy': (80.6337, 7.2906),
    'Galle': (80.2170, 6.0535),
}

location_maps = create_location_maps(locations)


create_memory_video_with_detailed_map(input_data, background_music, intro_video, outro_video)
