import threading
import time
import serial
from datetime import datetime
import json
import requests
from bluetooth import *
from knn import *


SERVER = '' #Optional HTTP Path to POST Updates

ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_9573632373235101F032-if00', 9600) # Arduino Serial Path
last_serial_message = time.time()
time.sleep(2)

users = {
            'bob': {
                'bluetooth_mac' : 'xx:xx:xx:xx:xx:xx',
                'rssi_thres' : 0,
                'bluetooth_detected' : False,
                'face_detected' : False
            },
            'joe': {
                'bluetooth_mac' : 'xx:xx:xx:xx:xx:xx',
                'rssi_thres' : 0,
                'bluetooth_detected' : False,
                'face_detected' : False
            }        
        }


def _any_bluetooth_detected():
    for user in users:
        if users[user]['bluetooth_detected'] == True:
            return True
    return False


def poll_bluetooth():
    while True:
        for user in users:
            bluetooth_mac = users[user]['bluetooth_mac']
            rssi_thres = users[user]['rssi_thres']
            bluetooth_status = bluetooth_ping(bluetooth_mac)

            if (bluetooth_status[0] == True and bluetooth_status[1] >= users[user]['rssi_thres']):
                users[user]['bluetooth_detected'] = True
            elif (bluetooth_status[0] == False):
                users[user]['bluetooth_detected'] = False
        time.sleep(0.1)

def face_detect():
    while True:
        if (_any_bluetooth_detected() == True):   # Only Run if Bluetooth Detected
            print("capturing")
            
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.45, fy=0.45)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all people in the image using a trained classifier model
            # Note: You can pass in either a classifier file name or a classifier model instance
            predictions = predict(rgb_small_frame)

            detected_users = []

            # Print results on the console
            for name, (top, right, bottom, left) in predictions:
                detected_users.append(name)

            for user in users:
                if user in detected_users:
                    users[user]['face_detected'] = True
                else:
                    users[user]['face_detected'] = False
                
        else:
            time.sleep(0.2)

def send_to_arduino():
    global last_serial_message
    while True:
        for user in users:
            if (users[user]['face_detected'] == True and users[user]['bluetooth_detected'] == True and (time.time() - last_serial_message > 4)):
                print(user + " detected")
                threading.Thread(target=send_to_azure, args=(user,)).start()
                ser.write(("1"+user).encode('utf-8'))
                last_serial_message = time.time()
                break;
        time.sleep(0.001)


def send_to_azure(u):
    postMsg = json.loads('{"person": "", "time" : ""}')
    postMsg['person'] = u
    postMsg['time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    try:
        response = requests.post(SERVER, json=postMsg, timeout=5)
        print("   POST SENT")
    except Exception as e:
        print(e)

    return

if __name__ == "__main__":
    try:
        # Start Bluetooth Ping
        threading.Thread(target=poll_bluetooth, args=()).start()
        # Start Face Detection Thread
        threading.Thread(target=face_detect, args=()).start()
        # Start Arduino Communication
        send_to_arduino()
        
    except Exception as e:
        print(e)
        
    finally:
        video_capture.release()
        ser.close()
    

    
    

        
