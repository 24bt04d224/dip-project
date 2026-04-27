import cv2

def check_cameras():
    print("Checking available cameras...")
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera index {i} is working. Frame shape: {frame.shape}")
            else:
                print(f"Camera index {i} is opened but could not read frame.")
            cap.release()
        else:
            print(f"Camera index {i} could not be opened.")

if __name__ == "__main__":
    check_cameras()
