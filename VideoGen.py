import MapTransitions as mt
import AudioDetector as ad
import ImageTexter as it
import ContentArranger as ca
import VideoCreator as vc
from flask import Flask, jsonify, request
import logging  # Import logging module

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def gen():
    # Get JSON data from the request
    try:
        logging.info('Received request for video generation')  # Log info
        data = request.get_json()['data']  # Access 'data' from the JSON payload
        logging.debug(f'Request data: {data}')  # Log debug data
        print(data)

        # Initialize locations list
        locations = [entry['location'] for entry in data]
        logging.debug(f'Locations extracted: {locations}')  # Log extracted locations

        # Append the next location of the last entry to return to the start
        locations.append(data[-1]['next'])
        logging.debug(f'Final locations list: {locations}')  # Log final locations list

        # Initialize content list
        content = []

        # Collect content directly (since it's already read into memory as image data)
        for entry in data:
            for ele in entry['content']:
                content.append(ele)

        logging.debug(f'Collected content: {content}')  # Log collected content

        # Assuming `map_transitions()` returns a list of 4D arrays
        split_gifs = mt.map_transitions(locations)
        logging.info(f'Map transitions generated: {split_gifs}')  # Log map transitions

        selected_music = ad.audio_detect(content)
        logging.info(f'Selected music: {selected_music}')  # Log selected music

        # Add text on images
        texted_images = it.text_in_images(data)
        logging.info(f'Text added to images: {texted_images}')  # Log texted images

        # Arrange content
        arranged_content = ca.content_arrange(texted_images, split_gifs, data)
        logging.info(f'Content arranged: {arranged_content}')  # Log arranged content

        # Create the video
        vc.create_video_from_media(arranged_content, selected_music)
        logging.info("Video is created successfully")  # Log video creation success

        video_path = "video.mp4"  # Update with the actual path
        
        # Return success message along with the video path
        return jsonify({'message': "Video is created", 'video_path': video_path}), 200
    except Exception as e:
        logging.error(f"Error during video generation: {e}", exc_info=True)  # Log the error with traceback
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
