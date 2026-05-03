import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
import requests
import time
import os
import pyttsx3
import threading
import re

# Model Config
MODEL_PATH = 'yolov8n.pt'
reader = easyocr.Reader(['en'])
API_URL = "http://localhost:5000/detect"

# REGEX for Indian Plates
STANDARD_PLATE = r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$'
BHARAT_SERIES = r'^[0-9]{2}BH[0-9]{4}[A-Z]{2}$'

def get_plate_type(img):
    """Simple heuristic to detect plate type based on dominant color"""
    try:
        # Resize for faster processing
        small = cv2.resize(img, (50, 20))
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        
        # Calculate mean values
        avg_color = np.mean(small, axis=(0, 1))
        b, g, r = avg_color
        
        # Green Plate (EV)
        if g > r + 20 and g > b + 20:
            return "Electric"
        # Yellow Plate (Commercial)
        if r > 180 and g > 180 and b < 150:
            return "Commercial"
        # Red Plate (Temporary)
        if r > 180 and g < 100 and b < 100:
            return "Temporary"
        
        return "Private"
    except:
        return "Private"

def validate_plate(text):
    clean = "".join(e for e in text if e.isalnum()).upper()
    # Normalize common OCR errors
    clean = clean.replace('O', '0').replace('I', '1').replace('Z', '2').replace('S', '5')
    
    if re.match(STANDARD_PLATE, clean) or re.match(BHARAT_SERIES, clean):
        return True, clean
    return False, clean

# TTS Setup
def speak(text):
    def _run():
        try:
            # Initialize engine inside the thread to avoid COM/threading issues
            local_engine = pyttsx3.init()
            local_engine.say(f"Plate detected {text}")
            local_engine.runAndWait()
            # Clean up the engine instance
            local_engine.stop()
        except Exception as e:
            print(f"TTS Error: {e}")
            
    threading.Thread(target=_run, daemon=True).start()

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(cv2.medianBlur(gray, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return gray

def run_pipeline():
    # Try different backends and indices if 0 fails
    print("Opening camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Warning: Camera index 0 with DSHOW failed. Trying index 0 default...")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera. Please check if your webcam is connected or used by another app.")
        return

    last_detected = {}
    COOLDOWN = 60
    
    print("AI Surveillance Active... (Press 'q' to quit)")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            print("Failed to grab frame")
            break

        results = model(frame, verbose=False)[0]
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            if cls in [2, 3, 5, 7] or conf > 0.5: # Vehicle or high conf
                roi = frame[y1:y2, x1:x2]
                if roi.size == 0: continue
                
                # Detect plate color
                p_type = get_plate_type(roi)
                
                # OCR
                results_ocr = reader.readtext(preprocess(roi))
                full_text = "".join([res[1] for res in results_ocr])
                valid, plate = validate_plate(full_text)
                
                if valid:
                    ocr_conf = max([res[2] for res in results_ocr]) if results_ocr else 0
                    
                    # Visuals
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{plate} ({p_type})", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    curr = time.time()
                    if plate not in last_detected or (curr - last_detected[plate] > COOLDOWN):
                        try:
                            requests.post(API_URL, json={
                                "plate_number": plate,
                                "confidence": ocr_conf,
                                "type": p_type
                            }, timeout=1)
                        except:
                            pass
                        last_detected[plate] = curr
                        speak(plate)

        cv2.imshow("Detection Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Loading models...")
    model = YOLO('yolov8n.pt')
    run_pipeline()
