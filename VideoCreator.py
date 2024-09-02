from moviepy.editor import ImageSequenceClip, VideoFileClip, ImageClip, concatenate_videoclips, AudioFileClip
import numpy as np
from PIL import Image
import Transitions as ts  # Ensure this module is implemented correctly
import random

def gif_to_video_clip(gif_path):
    """Convert a GIF file to a video clip."""
    with Image.open(gif_path) as gif:
        # Extract frames from the GIF
        frames = []
        try:
            while True:
                # Convert each frame to a numpy array
                frame = gif.copy()
                frame = frame.convert('RGB')  # Convert to RGB if not already
                frames.append(np.array(frame))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        
        # Create a video clip from the frames
        fps = 1000 / gif.info['duration']  # Duration is in milliseconds
        video_clip = ImageSequenceClip(frames, fps=fps)
        return video_clip.resize((854, 480))  # Resize to 480p

def create_video_from_media(image_paths, music_path=None, output_file='combined_video.mp4'):
    """Create a video from a list of media files (images, GIFs, videos) with optional background music."""
    all_clips = []
    num_files = len(image_paths)

    for i, media in enumerate(image_paths):
        if isinstance(media, str) and media.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Handle image file paths
            image_clip = ImageClip(media).set_duration(3)  # Display image for 3 seconds
            image_clip = image_clip.resize((854, 480))  # Resize to 480p
            all_clips.append(image_clip)
        
        elif isinstance(media, str) and media.lower().endswith(('.mp4', '.avi', '.mov')):
            # Handle video file paths
            video_clip = VideoFileClip(media).resize((854, 480))  # Resize to 480p
            all_clips.append(video_clip)

        elif isinstance(media, str) and media.lower().endswith('.gif'):
            # Handle GIF file paths
            video_clip = gif_to_video_clip(media)
            all_clips.append(video_clip)
        
        elif isinstance(media, np.ndarray):
            # Handle image arrays
            image_clip = ImageClip(media).set_duration(3)  # Display image for 3 seconds
            image_clip = image_clip.resize((854, 480))  # Resize to 480p
            all_clips.append(image_clip)
        
        else:
            print(f"Unsupported media type: {media}")

        print(f"Processed {i+1}/{num_files} media files.")

        if i > 0:
            # Apply transitions if needed
            all_clips[i] = ts.fadein_transition(all_clips[i], duration=2)

    # Concatenate video clips
    final_clip = concatenate_videoclips(all_clips, method="compose")

    # Load and set audio if music_path is provided
    if music_path:
        audio_clip = AudioFileClip(music_path)
        # Adjust audio length to match the video duration
        audio_clip = audio_clip.subclip(0, final_clip.duration)
        final_clip = final_clip.set_audio(audio_clip)

    # Write the result to a file with 480p resolution
    final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24, preset='medium', threads=4)
    print("Video created successfully!")

# Example usage:
# create_video_from_media(arranged_content, selected_music)
