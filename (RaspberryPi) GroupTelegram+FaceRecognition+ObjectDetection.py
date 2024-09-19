from picamera2 import Picamera2
from ultralytics import YOLO
import face_recognition
import numpy as np
import cv2
import requests
import time

# Telegram bot parameters
TOKEN = "7290187905:AAHp7vnjffhKLlAW23e0Z7IoEQ37tEPf_SE"  # Replace with your bot token
CHAT_IDS = ['955629733', 'CHAT_ID_2']  # List of chat IDs (can be group or individual chat IDs)
message_count = 0  # Counter for the number of detections

# Function to send message and image to Telegram groups or multiple people
def send_telegram_message(count, message, image_path=None):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        r = requests.get(url)
        print(f"Message to {chat_id}: ", r.json())

        if image_path:
            files = {'photo': open(image_path, 'rb')}
            url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
            r = requests.post(url, files=files)
            print(f"Image to {chat_id}: ", r.json())

# Initialize PiCamera2
picam2 = Picamera2()

# Load the YOLO model for object detection
yolo_model = YOLO("best.pt")

# Load known face encodings for face detection
known_face_encodings = []
known_face_names = []

# Load and encode known faces
known_person1_image = face_recognition.load_image_file("/home/rasp/Desktop/Salah.jpg")
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]

known_person2_image = face_recognition.load_image_file("/home/rasp/Desktop/Seif.jpg")
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]

known_face_encodings.append(known_person1_encoding)
known_face_names.append("Salah")

known_face_encodings.append(known_person2_encoding)
known_face_names.append("Seif")

def run_object_detection():
    global message_count
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()
    try:
        while True:
            # Capture a frame from the camera
            frame = picam2.capture_array()

            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform detection using YOLO
            results = yolo_model(frame_rgb, show=True, conf=0.3)
            result = results[0]

            # Get bounding boxes, confidence, and class names
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            confidences = np.array(result.boxes.conf.cpu(), dtype="float")
            classes = np.array(result.boxes.cls.cpu(), dtype="int")

            # Draw bounding boxes and labels on the frame
            for bbox, confi, cls in zip(bboxes, confidences, classes):
                (x, y, x2, y2) = bbox
                class_id = int(cls)
                object_name = yolo_model.names[class_id]

                # If an infected plant is detected, send the image to Telegram
                if object_name.lower() == 'infected':
                    message_count += 1
                    # Save the detected infected plant image
                    image_path = f"infected_plant_{message_count}.jpg"
                    cv2.imwrite(image_path, frame[y:y2, x:x2])

                    # Send message and image to Telegram groups/people
                    send_telegram_message(message_count, f"Detected {object_name}!", image_path)

                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"{object_name} {confi:.2f}", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

            # Show the processed frame
            cv2.imshow("Object Detection", frame)

            # Check if the 'q' key is pressed to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupt received. Closing...")
    finally:
        time.sleep(0.1)  # Add a small delay
        picam2.stop()
        cv2.destroyAllWindows()

def run_face_detection():
    global message_count
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    picam2.start()
    
    try:
        while True:
            # Capture an image from the camera
            im = picam2.capture_array()

            # Convert the XRGB8888 image to RGB format
            im_rgb = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.uint8)
            im_rgb[:, :, 0] = im[:, :, 1]  # Red channel
            im_rgb[:, :, 1] = im[:, :, 2]  # Green channel
            im_rgb[:, :, 2] = im[:, :, 3]  # Blue channel

            # Find face locations and encodings
            face_locations = face_recognition.face_locations(im_rgb)
            face_encodings = face_recognition.face_encodings(im_rgb, face_locations)
            
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    
                # Draw a rectangle around the face and label it
                cv2.rectangle(im, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(im, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                # If a known person is detected, send the image to Telegram
                if name != "Unknown":
                    message_count += 1
                    image_path = f"detected_face_{message_count}.jpg"
                    cv2.imwrite(image_path, im)

                    # Send message and image to Telegram groups/people
                    send_telegram_message(message_count, f"Detected {name}!", image_path)

            # Display the image
            cv2.imshow("Face Detection", im)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupt received. Closing...")
    finally:
        time.sleep(0.1)  # Add a small delay
        picam2.stop()
        cv2.destroyAllWindows()

# Main loop to ask which model to run
while True:
    print("\nWhich model do you want to run?")
    print("1. Object Detection")
    print("2. Face Detection")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        print("Starting Object Detection...")
        run_object_detection()
    elif choice == "2":
        print("Starting Face Detection...")
        run_face_detection()
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
