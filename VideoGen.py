import folium
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import cv2

# Input coordinates for locations
locations = [
    {"name": "Colombo", "coords": [6.927079, 79.861244]},
    {"name": "Galle", "coords": [6.0535, 80.2210]},
    {"name": "Yala National Park", "coords": [6.3728, 81.5016]},
    {"name": "Trincomalee", "coords": [8.5774, 81.2330]},
    {"name": "Colombo", "coords": [6.927079, 79.861244]}  # Return to start
]

# Create a map centered at the first location
m = folium.Map(location=locations[0]["coords"], zoom_start=10, tiles='OpenStreetMap')

# Add markers for all locations
for i, loc in enumerate(locations):
    folium.Marker(
        loc["coords"], 
        popup=f'{loc["name"]} - Day {i+1}', 
        icon=folium.Icon(color='green' if i == 0 else 'red')
    ).add_to(m)

# Add a smooth animation to transition between all locations
script = """
<script>
var locations = """ + str([loc["coords"] for loc in locations]) + """;
var currentIndex = 0;
var map = this;

function moveToNextLocation() {
    if (currentIndex >= locations.length - 1) return;
    
    var start = locations[currentIndex];
    var end = locations[currentIndex + 1];
    var steps = 100;
    var step = 0;
    
    function animate() {
        if (step <= steps) {
            var lat = start[0] + (end[0] - start[0]) * (step / steps);
            var lng = start[1] + (end[1] - start[1]) * (step / steps);
            
            // Calculate zoom level (zoom out, then in)
            var zoomOut = 5;  // Minimum zoom level
            var zoomIn = 10;  // Maximum zoom level
            var zoomLevel;
            if (step <= steps / 2) {
                zoomLevel = zoomIn + (zoomOut - zoomIn) * (step / (steps / 2));
            } else {
                zoomLevel = zoomOut + (zoomIn - zoomOut) * ((step - steps / 2) / (steps / 2));
            }
            
            map.setView([lat, lng], zoomLevel);
            step++;
            setTimeout(animate, 50);
        } else {
            currentIndex++;
            if (currentIndex < locations.length - 1) {
                setTimeout(moveToNextLocation, 1000);  // Wait 1 second before next transition
            }
        }
    }
    animate();
}

setTimeout(moveToNextLocation, 2000);  // Start the animation after 2 seconds
</script>
"""
m.get_root().html.add_child(folium.Element(script))

# Save the map to an HTML file
m.save('map.html')

# Set up Selenium to capture the map transition
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(f"file://{os.path.abspath('map.html')}")

# Wait to load the map completely and for animations to finish
total_wait_time = (len(locations) - 1) * (100 * 0.05 + 1) + 2  # Calculate based on transitions
print(f"Waiting for {total_wait_time} seconds for all transitions to complete...")
time.sleep(total_wait_time)

# Capture frames for the video
frames = []
try:
    for _ in range(int(total_wait_time * 20)):  # Capture at 20 fps
        if len(driver.window_handles) > 0:
            driver.save_screenshot('frame.png')
            frames.append(cv2.imread('frame.png'))
            time.sleep(0.05)
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