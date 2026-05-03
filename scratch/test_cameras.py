import cv2

def test_camera(index):
    print(f"Testing camera {index}...")
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"Camera {index} is working!")
            cv2.imwrite(f"camera_test_{index}.jpg", frame)
            cap.release()
            return True
        cap.release()
    print(f"Camera {index} failed.")
    return False

for i in range(5):
    test_camera(i)
