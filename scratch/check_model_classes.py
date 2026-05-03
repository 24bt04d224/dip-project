from ultralytics import YOLO

model = YOLO('license_plate_best.pt')
print("Model Classes:", model.names)
