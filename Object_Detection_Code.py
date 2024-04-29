# this code is good
import cv2
import urllib.request
import numpy as np
from ultralytics import YOLO


# Replace the URL with the IP camera's stream URL
url = 'http://192.168.1.4/cam-hi.jpg'

cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)

# Create a VideoCapture object
cap = cv2.VideoCapture(url)

# Uploading Your Model
model = YOLO(r"C:\Users\PC\Desktop\video_and_model\best.pt")

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

    # Code for Detection and put labels
    results = model(im, show=True, conf=0.3)
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    confidences = np.array(result.boxes.conf.cpu(), dtype="float")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    for bbox, confi, cls in zip(bboxes, confidences, classes):
        (x, y, x2, y2) = bbox
        class_id = int(cls)
        object_name = model.names[class_id]
        cv2.rectangle(im, (x, y), (x2, y2), (0, 0, 225), 2)
        cv2.putText(im, f"{object_name} {confi:.2f}", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)

    cv2.imshow('live Cam Testing', im)

    # Add a delay to control frame update rate and wait for user input
    key = cv2.waitKey(1000)  # Delay of 1 second

    # Check if the 'q' key is pressed to exit the loop
    if key == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
