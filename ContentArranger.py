def content_arrange(images, maps, data):
    i = 0
    loc_in_images = 0
    full_content = []

    for entry in data:
        loc = []
        for content_item in entry['content']:
            # Skip non-image data (e.g., video files)
            if not isinstance(content_item, bytes):
                loc.append(content_item)
            else:
                loc.append(images[loc_in_images])
                loc_in_images += 1
        i += 1
        loc.append(maps[i - 1])
        full_content.extend(loc)

    return full_content
