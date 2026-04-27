from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pymongo
from datetime import datetime, timedelta
import re
import cv2
import time
import numpy as np
import os
import json
import queue

app = Flask(__name__)
CORS(app)

# MongoDB setup
MONGO_URI = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URI)
db = client["smart_cctv"]
vehicles_col = db["vehicles"]
logs_col = db["logs"]

notification_queue = queue.Queue()

# REGEX Patterns (India)
STANDARD_PLATE = r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$'

def clean_plate(text):
    """
    Expert AI Logic for Indian Number Plates.
    Format: SS DD LL NNNN (e.g., GJ01AB1234)
    """
    # 1. Strip all noise
    text = "".join(re.findall(r'[A-Z0-9]', text.upper()))
    if len(text) < 10: return text # Return as is for further validation check

    # Character mapping for common confusion
    char_to_num = {'O': '0', 'I': '1', 'Z': '2', 'S': '5', 'B': '8', 'G': '6', 'D': '0', 'Q': '0'}
    num_to_char = {'0': 'G', '1': 'I', '2': 'Z', '5': 'S', '8': 'B', '6': 'G', '4': 'A'}

    res = list(text)
    for i in range(min(len(res), 10)):
        # Positions that MUST be Letters: 0, 1 (State) and 4, 5 (Series)
        if i in [0, 1, 4, 5]:
            if res[i] in num_to_char: res[i] = num_to_char[res[i]]
        # Positions that MUST be Numbers: 2, 3 (District) and 6, 7, 8, 9 (Unique)
        elif i in [2, 3] or i >= 6:
            if res[i] in char_to_num: res[i] = char_to_num[res[i]]
                
    return "".join(res)

def is_valid_plate(plate):
    return bool(re.match(STANDARD_PLATE, plate))

# --- AI Loading ---
try:
    from ultralytics import YOLO
    import easyocr
    model = YOLO('model/best.pt')
    reader = easyocr.Reader(['en'])
    print("--- AI Engine Loaded ---")
except Exception as e:
    model = None
    reader = None
    print(f"AI Error: {e}")

def preprocess_plate(roi):
    """Advanced preprocessing for better OCR accuracy"""
    try:
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    except:
        return roi

import threading

# Shared state for threaded AI
latest_frame = None
latest_results = []
ai_lock = threading.Lock()

def ai_worker():
    """Background thread for heavy AI processing"""
    global latest_frame, latest_results
    last_detect_time = {}
    
    while True:
        frame_to_process = None
        with ai_lock:
            if latest_frame is not None:
                frame_to_process = latest_frame.copy()
        
        if frame_to_process is not None and model:
            # Optimize: Resize for YOLO
            small_frame = cv2.resize(frame_to_process, (640, 480))
            results = model(small_frame, conf=0.4, verbose=False)[0]
            
            # Scale coordinates back to original size
            h, w = frame_to_process.shape[:2]
            scale_x, scale_y = w/640, h/480
            
            temp_results = []
            for box in results.boxes:
                bx1, by1, bx2, by2 = map(int, box.xyxy[0])
                x1, y1, x2, y2 = int(bx1*scale_x), int(by1*scale_y), int(bx2*scale_x), int(by2*scale_y)
                
                roi = frame_to_process[y1:y2, x1:x2]
                if roi.size > 0 and reader:
                    processed_roi = preprocess_plate(roi)
                    ocr_results = reader.readtext(processed_roi)
                    if ocr_results:
                        raw_text = "".join([res[1] for res in ocr_results])
                        plate_text = clean_plate(raw_text)
                        
                        if is_valid_plate(plate_text):
                            temp_results.append({'box': (x1, y1, x2, y2), 'text': plate_text})
                            
                            curr_time = time.time()
                            if plate_text not in last_detect_time or (curr_time - last_detect_time[plate_text] > 5):
                                result = log_plate_internal(plate_text, ocr_results[0][2])
                                if result.get("status") == "success":
                                    notification_queue.put(result)
                                last_detect_time[plate_text] = curr_time
            
            with ai_lock:
                latest_results = temp_results
        
        time.sleep(0.05) # Small sleep to prevent CPU hogging

# Start AI thread
threading.Thread(target=ai_worker, daemon=True).start()

def gen_frames(idx=0):
    global latest_frame, latest_results
    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
    if not cap.isOpened(): cap = cv2.VideoCapture(idx, cv2.CAP_MSMF)
    
    # Increase buffer size for smoothness
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    while True:
        success, frame = cap.read()
        if not success or frame is None:
            time.sleep(0.01)
            continue

        # Update latest frame for AI thread
        with ai_lock:
            latest_frame = frame.copy()
            current_results = latest_results.copy()

        # Draw CACHED results on current live frame
        for res in current_results:
            x1, y1, x2, y2 = res['box']
            plate_text = res['text']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"VALID: {plate_text}", (x1, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def log_plate_internal(plate_number, confidence):
    if not is_valid_plate(plate_number):
        return {"status": "ignore"}

    timestamp = datetime.now()
    log_entry = {
        "status": "success",
        "plate_number": plate_number,
        "confidence": round(float(confidence) * 100, 1),
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "time_only": timestamp.strftime("%I:%M %p"),
        "date_only": timestamp.strftime("%b %d, %Y"),
        "type": "Private",
        "found": False, "owner_name": "Unknown"
    }
    
    # Match with MongoDB
    vehicle = vehicles_col.find_one({"plate_number": plate_number})
    if vehicle:
        log_entry.update({
            "owner_name": vehicle["owner_name"],
            "status_text": vehicle["status"], 
            "found": True
        })
    else:
        log_entry["status_text"] = "Unknown"

    # Avoid duplicate logs within 5 seconds
    five_seconds_ago = (datetime.now() - timedelta(seconds=5)).strftime("%Y-%m-%d %H:%M:%S")
    if not logs_col.find_one({"plate_number": plate_number, "timestamp": {"$gte": five_seconds_ago}}):
        logs_col.insert_one(log_entry.copy())
        print(f"✅ Valid Plate Logged: {plate_number}")
        return log_entry
    
    return {"status": "ignore"}

@app.route('/events')
def events():
    def stream():
        while True:
            log = notification_queue.get()
            yield f"data: {json.dumps(log)}\n\n"
    return Response(stream(), mimetype='text/event-stream')

@app.route('/video_feed')
def video_feed():
    idx = int(request.args.get('index', 0))
    return Response(gen_frames(idx), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def get_logs():
    # Only return successful logs
    logs = list(logs_col.find({"status": "success"}).sort("timestamp", -1).limit(50))
    for log in logs: log["_id"] = str(log["_id"])
    return jsonify(logs)

@app.route('/stats')
def get_stats():
    return jsonify({
        "total": logs_col.count_documents({"status": "success"}), 
        "unknown": logs_col.count_documents({"status": "success", "found": False}), 
        "alerts": logs_col.count_documents({"status": "success", "status_text": "Blacklisted"}), 
        "active": 1
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
