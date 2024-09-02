import MapTransitions as mt
import AudioDetector as ad
import ImageTexter as it
import ContentArranger as ca
import VideoCreator as vc
import cv2

data = [{
    'location': {"name": "Colombo", "coords": [79.861244, 6.927079]},
    'content': [cv2.imread('1.jpg'), cv2.imread('2.jpg')],  # Read images directly
    'time': 'Day 01',
    'next': {"name": "Galle", "coords": [80.2210, 6.0535]}
},
{
    'location': {"name": "Galle", "coords": [80.2210, 6.0535]},
    'content': [cv2.imread('3.jpg')],
    'time': 'Day 02',
    'next': {"name": "Yala National Park", "coords": [81.5016, 6.3728]}
},
{
    'location': {"name": "Yala National Park", "coords": [81.5016, 6.3728]},
    'content': [cv2.imread('4.jpg')],
    'time': 'Day 03',
    'next': {"name": "Trincomalee", "coords": [81.2330, 8.5774]}
},
{
    'location': {"name": "Trincomalee", "coords": [81.2330, 8.5774]},
    'content': [cv2.imread('5.jpg')],
    'time': 'Day 04',
    'next': {"name": "Colombo", "coords": [79.861244, 6.927079]}
}]

# Initialize locations list
locations = [entry['location'] for entry in data]

# Append the next location of the last entry to return to the start
locations.append(data[-1]['next'])

# Initialize content list
content = []

# Collect content directly (since it's already read into memory as image data)
for entry in data:
    for ele in entry['content']:
        content.append(ele)

# Assuming `map_transitions()` returns a list of 4D arrays
split_gifs = mt.map_transitions(locations)
print(split_gifs)

selected_music = ad.audio_detect(content)

# Add text on images
texted_images = it.text_in_images(data)
print(texted_images)

# Arrange content
arranged_content = ca.content_arrange(texted_images, split_gifs, data)

# Create the video
vc.create_video_from_media(arranged_content, selected_music)
print("Video is created")
