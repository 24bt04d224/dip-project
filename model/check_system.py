import cv2
import easyocr
from ultralytics import YOLO
import os

def check_system():
    print("--- Diagnostic Check ---")
    
    # 1. Check OpenCV
    print(f"OpenCV Version: {cv2.__version__}")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Cannot open webcam. Check your camera connection.")
    else:
        print("✅ Webcam: OK")
        cap.release()

    # 2. Check YOLO
    print("\nChecking YOLO Model...")
    try:
        # Try to load a specialized model
        model = YOLO('keremberke/yolov8n-license-plate')
        print("✅ YOLO Model (Plate): Loaded Successfully from Hub")
    except Exception as e:
        print(f"❌ YOLO Model: Failed to load specialized model. Falling back to generic.")
        try:
            model = YOLO('yolov8n.pt')
            print("✅ YOLO Model (Generic): Loaded Successfully")
        except Exception as e2:
            print(f"❌ YOLO Model: Critical failure. {e2}")

    # 3. Check EasyOCR
    print("\nChecking EasyOCR...")
    try:
        reader = easyocr.Reader(['en'])
        print("✅ EasyOCR: Initialized Successfully")
    except Exception as e:
        print(f"❌ EasyOCR: Failed to initialize. {e}")

    print("\n--- Check Complete ---")
    print("If you see red marks (❌), please install missing dependencies or check your internet connection.")

if __name__ == "__main__":
    check_system()
