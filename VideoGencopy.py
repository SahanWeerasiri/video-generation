import MapTransitions as mt
import AudioDetector as ad
import ImageTexter as it
import ContentArranger as ca
import VideoCreator as vc
import logging  # Import logging module


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def gen():
    # Get JSON data from the request
    try:
        #logging.info('Received request for video generation')  # Log info
        data = [{
            'location':{"name": "Colombo", "coords": [79.861244, 6.927079]},
            'paths':['1.jpg','2.jpg'],
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
        }]        #logging.debug(f'Request data: {data}')  # Log debug data

        # Initialize locations list
        locations = [entry['location'] for entry in data]
        #logging.debug(f'Locations extracted: {locations}')  # Log extracted locations

        # Append the next location of the last entry to return to the start
        locations.append(data[-1]['next'])
        #logging.debug(f'Final locations list: {locations}')  # Log final locations list

        # Initialize content list
        content = []

        # Collect content directly (since it's already read into memory as image data)
        for entry in data:
            for ele in entry['paths']:
                content.append(ele)

        #logging.debug(f'Collected content: {content}')  # Log collected content

        # Assuming `map_transitions()` returns a list of 4D arrays
        split_gifs = mt.map_transitions(locations)

        print(data[0]['paths'])
        #logging.info(f'Map transitions generated: {split_gifs}')  # Log map transitions

        selected_music = ad.audio_detect(content)
        #logging.info(f'Selected music: {selected_music}')  # Log selected music

        # Add text on images
        texted_images = it.text_in_images(data)
        #logging.info(f'Text added to images: {texted_images}')  # Log texted images

        # Arrange content
        arranged_content = ca.content_arrange(texted_images, split_gifs, data)
        #logging.info(f'Content arranged: {arranged_content}')  # Log arranged content

        # Create the video
        vc.create_video_from_media(arranged_content, selected_music)
        #logging.info("Video is created successfully")  # Log video creation success

        video_path = "combined_video.mp4"  # Update with the actual path
        
        # Return success message along with the video path
    except Exception as e:
        logging.error(f"Error during video generation: {e}", exc_info=True)  # Log the error with traceback
        print(e)

if __name__ == "__main__":
    gen()
