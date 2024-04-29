# this code is good
import cv2
import urllib.request
import numpy as np

# Replace the URL with the IP camera's stream URL
url = 'http://192.168.0.133/cam-lo.jpg'

cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

# Create a VideoCapture object
cap = cv2.VideoCapture(url)

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

# Read and display video frames
while True:
    # Read a frame from the video stream
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    im = cv2.imdecode(imgnp, -1)

    cv2.imshow('live Cam Testing', im)

    # Add a delay to control frame update rate and wait for user input
    key = cv2.waitKey(1000)  # Delay of 1 second

    # Check if the 'q' key is pressed to exit the loop
    if key == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
