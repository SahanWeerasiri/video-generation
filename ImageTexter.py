from PIL import Image, ImageDraw, ImageFont
import io
import os

def text_in_images(data, output_folder='texted_images'):
    def add_text_to_image(image_data, text):
        # Load image from raw data
        img = Image.open(io.BytesIO(image_data))

        # Create drawing context
        draw = ImageDraw.Draw(img)

        # Define font and size
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()

        # Define text position
        text_position = (10, img.height - 40)

        # Define text color
        text_color = (255, 255, 255)  # White

        # Add text to image
        draw.text(text_position, text, font=font, fill=text_color)

        # Save image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return img_byte_arr

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process images from the data
    output_images = []
    for entry in data:
        for image_data in entry['content']:
            # Skip non-image data (e.g., video files)
            if not isinstance(image_data, bytes):
                continue
            
            # Add text to image
            modified_image = add_text_to_image(image_data, entry['time'])
            output_images.append(modified_image)
            
            print("Processed image and added text.")

    print("All images processed successfully.")
    return output_images
