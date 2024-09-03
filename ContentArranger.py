def content_arrange(images,maps,data):
    i = 0
    loc_in_images = 0
    full_content =[]
    for entry in data:
        loc = []
        loc.append(maps[i])
        for image_file in entry['paths']:
            # Skip non-image files (e.g., video files)
            if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                loc.append(image_file)
            else:
                loc.append(images[loc_in_images])
                loc_in_images+=1
        i+=1
        full_content.extend(loc)
    return full_content