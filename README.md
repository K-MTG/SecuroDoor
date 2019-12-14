# SecuroDoor
An access control system that provides secure hands-free entry using bluetooth (from smartphone) and facial recognition. 

# Features/Functionality 

Once the Raspberry Pi determines the user’s smartphone is in range (bluetooth), the USB webcam begins processing the captured image to determine if the associated user is detected. If the user is detected, the Pi will tell the Arduino (via Serial) to unlock the door. A corresponding status update is also sent to Azure. 

# Usage

1. [Python Facial API](https://github.com/ageitgey/face_recognition "Install Face Recognition API")
2. Create a folder in the "known_people" directory with user's name. Insert the user's photo into that folder (more the better).
3. Create and train the KNN classifier (python3 knn_train.py)
4. Modify the "users" dictionary in main.py with the user’s name and bluetooth Mac Address. You may also need to pair the phone to the Raspberry Pi. Edit server and serial path as/if needed. 
5. python3 main.py to launch the app


# Hardware

![alt text](https://github.com/K-MTG/SecuroDoor/blob/master/SecuroDoor.png?raw=true)

