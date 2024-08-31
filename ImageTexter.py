from PIL import Image, ImageDraw, ImageFont
import os

def text_in_images(data, output_folder='texted_images'):
    def add_text_to_image(image_path, text, output_path):
        # Load image
        with Image.open(image_path) as img:
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
            
            # Save the image
            img.save(output_path)
            return output_path

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through data and process images
    output_paths = []
    for entry in data:
        for image_file in entry['content']:
            # Skip non-image files (e.g., video files)
            if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            
            # Define input and output paths
            input_path = image_file
            output_path = os.path.join(output_folder, f"modified_{os.path.basename(image_file)}")
            
            # Add text to image
            saved_path = add_text_to_image(input_path, entry['time'], output_path)
            output_paths.append(saved_path)
            
            print(f"Processed image: {input_path}, saved as: {saved_path}")

    print("All images processed successfully.")
    return output_paths
