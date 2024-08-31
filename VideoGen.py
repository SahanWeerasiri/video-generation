import folium
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import cv2

# Input coordinates for two locations
location1 = [6.927079, 79.861244]  # Example: Colombo, Sri Lanka
location2 = [7.873054, 80.771797]  # Example: Kandy, Sri Lanka

# Create a map centered at the first location
m = folium.Map(location=location1, zoom_start=15, tiles='OpenStreetMap')
folium.Marker(location1, popup='Start Location', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location2, popup='End Location', icon=folium.Icon(color='red')).add_to(m)

# Add a smooth animation to transition from the first to the second location using JavaScript
script = f"""
<script>
    var start_lat = {location1[0]};
    var start_lng = {location1[1]};
    var end_lat = {location2[0]};
    var end_lng = {location2[1]};
    var current_lat = start_lat;
    var current_lng = start_lng;
    var steps = 100;
    var i = 0;
    var interval = setInterval(function() {{
        if (i <= steps) {{
            current_lat += (end_lat - start_lat) / steps;
            current_lng += (end_lng - start_lng) / steps;
            map.setView([current_lat, current_lng], 15);
            i++;
        }} else {{
            clearInterval(interval);
        }}
    }}, 50);
</script>
"""
m.get_root().html.add_child(folium.Element(script))

# Save the map to an HTML file
m.save('map.html')

# Set up Selenium to capture the map transition
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(f"file://{os.path.abspath('map.html')}")

# Wait to load the map completely
time.sleep(5)  # Increased sleep time

# Capture frames for the video
frames = []
try:
    for _ in range(100):
        if len(driver.window_handles) > 0:  # Check if window is still open
            driver.save_screenshot('frame.png')
            frames.append(cv2.imread('frame.png'))
            time.sleep(0.05)  # Adjust timing if needed
        else:
            print("Browser window closed unexpectedly.")
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

# Compile frames into a video using OpenCV
if frames:
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter('map_transition.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    print("Video created successfully: map_transition.mp4")
else:
    print("No frames captured. Video was not created.")



data = [{'location':'Colombo','content':[],'time':'Day 01','next':'Galle'},
        {'location':'Galle','content':[],'time':'Day 02','next':'Yala National Park'},
        {'location':'Yala National Park','content':[],'time':'Day 03','next':'Trincomalle'},
        {'location':'Trincomalle','content':[],'time':'Day 04','next':'Colombo'}]

