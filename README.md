# Smart CCTV Number Plate Recognition System

A complete vehicle recognition system using YOLOv8, OCR, and a real-time dashboard.

## 🚀 Setup Instructions

### 1. Prerequisite (MongoDB)
Ensure MongoDB is installed and running on your local machine (`localhost:27017`).

### 2. Backend Setup
```bash
cd backend
# Create virtual environment (optional)
# python -m venv venv
# source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-cors pymongo ultralytics easyocr opencv-python requests torch torchvision

# Seed the database with 1000 records
python db_seed.py

# Run the Flask API
python app.py
```

### 3. AI Pipeline Setup
```bash
cd model
# Run the detection pipeline (ensure backend is running first)
python detection_pipeline.py
```
*Note: Press 'q' to stop the video feed.*

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The dashboard will be available at `http://localhost:5173`.

---

## 🏗️ Project Components

- **backend/app.py**: Flask server with MongoDB integration.
- **backend/db_seed.py**: Script to generate 1,000 fake Indian vehicle records.
- **model/detection_pipeline.py**: Real-time YOLOv8 + EasyOCR processing script.
- **model/train.py**: Script to train YOLOv8 on your own dataset.
- **frontend/**: React + Vite + Tailwind/Custom CSS dashboard.

## 📊 Dataset Sources
To train the model on more accurate data, download datasets from:
- **Roboflow**: Search for "Vehicle Number Plate Detection YOLOv8"
- **Kaggle**: "Car License Plate Detection"

## 🛠️ Troubleshooting
- **EasyOCR Error**: The first run will download model weights (approx 100MB). Ensure you have internet access.
- **YOLO Error**: If `yolov8n.pt` is not found, it will automatically download from Ultralytics.
- **MongoDB Connection**: If the script fails to connect, check if the service is running: `services.msc` -> MongoDB.
