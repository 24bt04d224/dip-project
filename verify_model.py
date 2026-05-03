from ultralytics import YOLO
import easyocr
import cv2
import os

model_path = 'license_plate_best.pt'
image_path = 'test_plate.png'

print(f"--- Testing Model: {model_path} ---")
if not os.path.exists(model_path):
    print("Model not found!")
    exit()

model = YOLO(model_path)
reader = easyocr.Reader(['en'], gpu=False)

img = cv2.imread(image_path)
if img is None:
    print("Image not found!")
    exit()

results = model(img, conf=0.05)[0]
print(f"Boxes found: {len(results.boxes)}")

for i, box in enumerate(results.boxes):
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    conf = float(box.conf[0])
    print(f"Box {i}: Conf={conf:.2f}, Coords={(x1,y1,x2,y2)}")
    
    roi = img[y1:y2, x1:x2]
    if roi.size > 0:
        ocr_res = reader.readtext(roi, detail=0)
        print(f"  OCR Text: {ocr_res}")
