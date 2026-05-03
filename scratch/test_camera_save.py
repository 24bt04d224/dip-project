import cv2
import os

def test_save():
    print("Trying to capture a frame from Index 0...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera 0.")
        return
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("camera_test_0.jpg", frame)
        print("Success! Saved camera_test_0.jpg")
    else:
        print("Could not read frame from camera 0.")
    cap.release()

if __name__ == "__main__":
    test_save()
