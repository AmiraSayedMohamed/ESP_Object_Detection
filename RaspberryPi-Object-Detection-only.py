from picamera2 import Picamera2
from ultralytics import YOLO
import numpy as np
import cv2

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()q

# Load the YOLO model
model = YOLO("best.pt")

try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform detection using YOLO
        results = model(frame_rgb, show=True, conf=0.3)
        result = results[0]

        # Get bounding boxes, confidence, and class names
        bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
        confidences = np.array(result.boxes.conf.cpu(), dtype="float")
        classes = np.array(result.boxes.cls.cpu(), dtype="int")

        # Draw bounding boxes and labels on the frame
        for bbox, confi, cls in zip(bboxes, confidences, classes):
            (x, y, x2, y2) = bbox
            class_id = int(cls)
            object_name = model.names[class_id]

            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"{object_name} {confi:.2f}", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

        # Show the processed frame
        cv2.imshow("Camera", frame)

        # Check if the 'q' key is pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    # Handle interrupt from Jupyter notebook
    print("Interrupt received. Closing...")
finally:
    # Release the camera and close any OpenCV windows
    picam2.stop()
    cv2.destroyAllWindows()
