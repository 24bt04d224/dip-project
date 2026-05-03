import cv2
import time

def test_cameras():
    print("--- Camera Diagnostic Tool ---")
    print("Testing indices 0-5 with different backends...\n")
    
    backends = [
        ("Default", None),
        ("DSHOW (DirectShow)", cv2.CAP_DSHOW),
        ("MSMF (Media Foundation)", cv2.CAP_MSMF)
    ]
    
    found_any = False
    
    for index in range(6):
        for name, backend in backends:
            try:
                if backend is not None:
                    cap = cv2.VideoCapture(index, backend)
                else:
                    cap = cv2.VideoCapture(index)
                
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        print(f"[SUCCESS] Index {index} works with {name}")
                        found_any = True
                        cap.release()
                        break # Move to next index if one backend works
                cap.release()
            except Exception as e:
                pass
        else:
            print(f"[FAILED] Index {index} could not be opened with any backend.")

    if not found_any:
        print("\n[!] NO CAMERAS DETECTED.")
        print("Possible reasons:")
        print("1. Camera is physically disconnected.")
        print("2. Another app is using the camera (Zoom, Teams, Chrome).")
        print("3. Windows Privacy Settings: Settings -> Privacy -> Camera (Ensure 'Allow apps to access your camera' is ON).")
        print("4. Driver issues: Check Device Manager.")
    else:
        print("\n[TIP] If multiple work, the first successful one is usually your webcam.")

if __name__ == "__main__":
    test_cameras()
