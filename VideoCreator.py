from moviepy.editor import ImageSequenceClip, VideoFileClip,ImageClip, concatenate_videoclips, AudioFileClip
import numpy as np
from PIL import Image
import Transitions as ts  # Make sure this module is correctly implemented
import random

def gif_to_video_clip(gif_path):
    # Open the GIF file
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
        video_clip = ImageSequenceClip(frames, fps=1000 / gif.info['duration'])  # Duration in seconds
        return video_clip.resize((854, 480))  # Resize to 480p

def create_video_from_media(image_paths, music_path=None, output_file='combined_video.mp4'):
    all_clips = []
    i = 0
    temp = None

    for img_path in image_paths:
        if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Handle image files
            image_clip = ImageClip(img_path).set_duration(3)  # Display image for 3 seconds
            image_clip = image_clip.resize((854, 480))  # Resize to 480p
            all_clips.append(image_clip)
        
        elif img_path.lower().endswith(('.mp4', '.avi', '.mov')):
            # Handle video files
            video_clip = VideoFileClip(img_path).resize((854, 480))  # Resize to 480p
            all_clips.append(video_clip)

        elif img_path.lower().endswith('.gif'):
            # Handle GIF files
            video_clip = gif_to_video_clip(img_path)
            all_clips.append(video_clip)
        
        else:
            print(f"Unsupported file type: {img_path}")

        print(f"Finished: {len(all_clips)}/{len(image_paths)}")

        if(i > 0):
            all_clips[i] = ts.fadein_transition(all_clips[i], duration=2)
        i += 1

        # Adding a pause for each image if needed (adjust the duration)
        #pause_clip = ImageClip(img_path).set_duration(2).resize((854, 480))  # 2 seconds pause
        #all_clips.append(pause_clip)

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
