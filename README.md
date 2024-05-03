this project is about object detection (check if the plant is infected) by using yolo algorithm and connect this python code with ESP Camera

i have a previos videos to explain how to Collect data and train you model form beginning using yolovn8
check this repo:
https://github.com/AmiraSayedMohamed/Object-Detection-Using-YOLOvn8

this video will help you to test it :
https://youtu.be/7-3piBHV1W0?si=obsVstqUYoQgar22

1/ you first shoud download this library esp expressif to just test esp camera without connecting it with python to check 
that it isn't corrupted 
- first press file << Preferences <<  IN Additonal Boards Manager URLS << past this url:
https://www.youtube.com/redirect?event=comments&redir_token=QUFFLUhqblBmTk1CMTlYX2t5QzNZNG9tWFhvZGV0ejRGQXxBQ3Jtc0tsSlF1Y19hUEJHcGtoZy04SjdtQ2lEZkwwczRpLWt2NEx3NTRwRTRaMndiNjlZVXkxTDcwcmJBOVpoS21FbmgzcVNNZnhYVjRGcXFkZlVKMzJPMXhHdXNIcnhUaFBKY2UxTTB0LXMwVGtYWkRpVWFVSQ&q=https%3A%2F%2Fdl.espressif.com%2Fdl%2Fpackage_esp32_index.json
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
https://dl.espressif.com/dl/package_esp32_index.json
https://arduino.esp8266.com/stable/package_esp8266com_index.json


2/ Tools << board << board manager << Search for this library << esp32 Expressif Systems and download it 


3/ then  >> tools << Board << ESP32 Arduino << ESP32 Wrover Module  , then check  your right port is selected , you can check this by open device manager (Ports(com & LPT) and see what port you are on 
4/ then here it's the final step to check your camera is file << Example << ESP32 << Camera << CameraWebServer 
then in the code just remove comment from Ai thinker and comment any other camera type 
then write your wifi name and password
then upload the code

Every esp have a bootloader ( a way to upload your code , but the connection of it  is the same)
if you esp type have a flash button and reset button  : press the flash button before uploading this code  , and when appear at the terminal that com connected , remove your finger from the flash button and press reset button , then open the serial monitor, and check that that baud rate is 115200 and then press on the reset button again the ip address of the camera will appear to you , if it doesn't appear trying pressing reset button just one time  untill the ip address appear to you , then copy this ip address  and put it in the browser , and go down and press open video streaming and then go up again to show your video streaming , if the video appear then your camera is not corrupted 

_---------------------------------------------------------------------------------------------------------------------------------------

## Then we will now Explain How to connect Esp camera with Python code , in this repo we are explaining how to connect object detection code using yolo algorithm 

this video will help you :
https://youtu.be/npJsmbFZiMg?si=OnQ1PHTh4V9oUvbV
 and here it's the link for the material he provided:
https://www.electroniclinic.com/esp32-cam-with-python-opencv-yolo-v3-for-object-detection-and-identification

### Steps:
first download this library as a zip file form this repo:
https://github.com/yoursunny/esp32cam

and then go to arduino IDE << sketch << Include library < Add zip library
- then  go to file in in this repo and copy this code and put it into your arduino ide

- Then take the ip address and also the cam-hi or a cam-lo or cam-median , copy this two paths
we will need them to connect the esp to out python code 

- Open the file in this repo called Test_Camera_With_pthon.py:
and paste the code in this file at your pycharm ide




