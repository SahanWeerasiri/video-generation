import folium
from folium import Figure
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

# Create a Figure object
fig = Figure(width=800, height=600)

# Create a map centered at the first location
m = folium.Map(location=locations[0]["coords"], zoom_start=10, tiles='OpenStreetMap')
fig.add_child(m)

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
function startAnimation() {
    var locations = """ + str([loc["coords"] for loc in locations]) + """;
    var currentIndex = 0;
    var map = this;

    function moveToNextLocation() {
        if (currentIndex >= locations.length - 1) {
            document.body.setAttribute('data-animation-complete', 'true');
            return;
        }
        
        var start = locations[currentIndex];
        var end = locations[currentIndex + 1];
        var steps = 100;
        var step = 0;
        
        function animate() {
            if (step <= steps) {
                var lat = start[0] + (end[0] - start[0]) * (step / steps);
                var lng = start[1] + (end[1] - start[1]) * (step / steps);
                
                var zoomOut = 5;
                var zoomIn = 10;
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
                    setTimeout(moveToNextLocation, 1000);
                } else {
                    document.body.setAttribute('data-animation-complete', 'true');
                }
            }
        }
        animate();
    }

    setTimeout(moveToNextLocation, 1000);  // Start after a short delay
}

// Start the animation when the map is loaded
if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(startAnimation, 1000);
} else {
    document.addEventListener("DOMContentLoaded", function() {
        setTimeout(startAnimation, 1000);
    });
}
</script>
"""
fig.get_root().header.add_child(folium.Element(script))

# Save the map to an HTML file
fig.save('map.html')

# Set up Selenium to capture the map transition
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(f"file://{os.path.abspath('map.html')}")

# Wait for the animation to complete
wait = WebDriverWait(driver, 300)  # Wait up to 5 minutes
wait.until(EC.presence_of_element_located((By.XPATH, "//body[@data-animation-complete='true']")))

# Capture frames for the video
frames = []
try:
    while True:
        driver.save_screenshot('frame.png')
        frames.append(cv2.imread('frame.png'))
        time.sleep(0.05)
        
        # Check if animation is complete
        if driver.execute_script("return document.body.getAttribute('data-animation-complete') === 'true'"):
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