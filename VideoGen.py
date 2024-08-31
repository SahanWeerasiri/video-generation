import MapTransitions as mt
import AudioDetector as ad
import ImageTexter as it
import ContentArranger as ca
import VideoCreator as vc

data = [{
    'location':{"name": "Colombo", "coords": [79.861244, 6.927079]},
    'content':['1.jpg','2.jpg'],
    'time':'Day 01',
    'next':{"name": "Galle", "coords": [80.2210, 6.0535]}
},
{
    'location':{"name": "Galle", "coords": [80.2210, 6.0535]},
    'content':['3.jpg'],
    'time':'Day 02',
    'next':{"name": "Yala National Park", "coords": [81.5016, 6.3728]}
},
{
    'location':{"name": "Yala National Park", "coords": [81.5016, 6.3728]},
    'content':['entry_clip.mp4'],
    'time':'Day 03',
    'next':{"name": "Trincomalee", "coords": [81.2330, 8.5774]}
},
{
    'location':{"name": "Trincomalee", "coords": [81.2330, 8.5774]},
    'content':['4.jpg','5.jpg'],
    'time':'Day 04',
    'next':{"name": "Colombo", "coords": [79.861244, 6.927079]}
}]


# Initialize locations list
locations = []

# Iterate through the data and collect locations
for entry in data:
    locations.append(entry['location'])

# Append the next location of the last entry to return to the start
locations.append(data[-1]['next'])

# Initialize content list
content = []

# Iterate through the data and collect content
for entry in data:
    for ele in entry['content']:
        if ele.endswith('.mp4'):
            continue
        content.append(ele)

# Assuming `map_transitions()` returns a list of 4D arrays
split_gifs = mt.map_transitions(locations)
print(split_gifs)

selected_music = ad.audio_detect(content)

#text on images
texted_images = it.text_in_images(data)
print(texted_images)

#arrange content
arranged_content = ca.content_arrange(texted_images,split_gifs,data)


#create the video
vc.create_video_from_media(arranged_content,selected_music)
print("Video is created")
