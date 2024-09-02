import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import random
import librosa

def audio_detect(image_data_list):
    # Initialize the pre-trained ResNet50 model
    model = ResNet50(weights='imagenet')

    # Analyze an image directly from its in-memory data
    def analyze_image(image_data):
        # Resize image to the expected size for ResNet50 (224x224)
        img_data = tf.image.resize(image_data, (224, 224))
        
        # Expand dimensions and preprocess for model input
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        # Predict image content
        preds = model.predict(img_data)
        return decode_predictions(preds, top=3)[0]

    def analyze_image(image_data):
        # Resize image to the expected size for ResNet50 (224x224)
        img_data = tf.image.resize(image_data, (224, 224))
        
        # Convert to a writable NumPy array and expand dimensions
        img_data = np.copy(np.expand_dims(img_data, axis=0))
        
        # Preprocess for model input
        img_data = preprocess_input(img_data)

        # Predict image content
        preds = model.predict(img_data)
        return decode_predictions(preds, top=3)[0]


    # Map content to music characteristics
    def match_music_to_content(image_analysis):
        content_to_music_map = {
            'landscape': {'tempo': 'slow', 'mood': 'calm', 'genre': 'ambient'},
            'city': {'tempo': 'moderate', 'mood': 'upbeat', 'genre': 'electronic'},
            'portrait': {'tempo': 'slow', 'mood': 'emotional', 'genre': 'classical'},
            'sports': {'tempo': 'fast', 'mood': 'energetic', 'genre': 'rock'},
            'nature': {'tempo': 'slow', 'mood': 'peaceful', 'genre': 'acoustic'},
            'animals': {'tempo': 'moderate', 'mood': 'happy', 'genre': 'folk'},
            'lab_coat': {'tempo': 'slow', 'mood': 'thoughtful', 'genre': 'classical'},
            'maillot': {'tempo': 'upbeat', 'mood': 'lively', 'genre': 'pop'},
            'miniskirt': {'tempo': 'upbeat', 'mood': 'energetic', 'genre': 'pop'},
            'barrow': {'tempo': 'moderate', 'mood': 'steady', 'genre': 'folk'},
            'picket_fence': {'tempo': 'calm', 'mood': 'peaceful', 'genre': 'ambient'},
            'jean': {'tempo': 'casual', 'mood': 'relaxed', 'genre': 'acoustic'},
        }

        music_library = {
            'ambient': ['ambient_track_1.mp3', 'ambient_track_2.mp3'],
            'electronic': ['electronic_track_1.mp3', 'electronic_track_2.mp3'],
            'classical': ['classical_track_1.mp3', 'classical_track_2.mp3'],
            'rock': ['rock_track_1.mp3', 'rock_track_2.mp3'],
            'acoustic': ['acoustic_track_1.mp3', 'acoustic_track_2.mp3'],
            'folk': ['folk_track_1.mp3', 'folk_track_2.mp3'],
            'pop': ['pop_track_1.mp3', 'pop_track_2.mp3']
        }

        selected_music_genres = []
        for analysis in image_analysis:
            for _, label_name, _ in analysis:
                label_name_lower = label_name.lower()
                matched = False
                for label, music_characteristics in content_to_music_map.items():
                    if label in label_name_lower:
                        selected_music_genres.append(music_characteristics['genre'])
                        matched = True
                        break  # Break if a match is found
                if matched:
                    break  # Exit outer loop if a match is found

        # Default to 'ambient' if no specific genre is found
        if not selected_music_genres:
            selected_music_genres.append('ambient')

        # Randomly select a genre and track from the music library
        selected_genre = random.choice(selected_music_genres)
        selected_music = random.choice(music_library[selected_genre])

        return selected_music

    # Analyze images directly from in-memory data
    image_analysis = [analyze_image(img) for img in image_data_list]
    print("Image Analysis:", image_analysis)
    
    # Match the content to music
    selected_music = match_music_to_content(image_analysis)
    print("Selected Music:", selected_music)
    
    return selected_music
