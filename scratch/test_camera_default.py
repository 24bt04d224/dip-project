import cv2

def test_camera_default(index):
    print(f"Testing camera {index} default...")
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"Camera {index} (default) is working!")
            cap.release()
            return True
        cap.release()
    print(f"Camera {index} (default) failed.")
    return False

test_camera_default(0)
