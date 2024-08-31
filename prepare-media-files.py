def prepare_media_files(input_data):
    clips = []
    for location, files in input_data.items():
        location_clips = []
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                clip = ImageClip(file).set_duration(3)  # Set each image to appear for 3 seconds
            elif file.endswith(('.mp4', '.avi', '.mov')):
                clip = VideoFileClip(file)
            else:
                continue
            location_clips.append(clip)
        clips.append(concatenate_videoclips(location_clips))
    return clips

# Load intro and outro videos
intro = VideoFileClip(intro_video)
outro = VideoFileClip(outro_video)

# Prepare main content
main_content = prepare_media_files(input_data)
