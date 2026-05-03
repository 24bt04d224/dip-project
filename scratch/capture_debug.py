import cv2
import os

def capture_debug_frame():
    print("Attempting to capture debug frame...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera 0")
        return
    
    # Wait for camera to warm up
    for _ in range(10):
        cap.read()
    
    success, frame = cap.read()
    if success:
        save_path = os.path.join(r"C:\Users\lenovo\.gemini\antigravity\brain\5526c46f-2049-41b4-a233-e152eebd48ba", "debug_frame.jpg")
        cv2.imwrite(save_path, frame)
        print(f"Frame saved to {save_path}")
    else:
        print("Error: Could not read frame")
    
    cap.release()

if __name__ == "__main__":
    capture_debug_frame()
