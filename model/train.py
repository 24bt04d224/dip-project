from ultralytics import YOLO
import os

def train_model():
    # Load a pretrained model
    model = YOLO('yolov8n.pt')

    # Define path to dataset yaml file
    # You should have a data.yaml file in your dataset folder
    # Example format of data.yaml:
    # path: ../dataset
    # train: images/train
    # val: images/val
    # names:
    #   0: license_plate
    
    yaml_path = os.path.abspath('dataset/data.yaml')

    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found!")
        print("Please download a dataset from Roboflow and place the data.yaml in the dataset folder.")
        return

    # Train the model
    print("Starting training...")
    results = model.train(
        data=yaml_path,
        epochs=50,
        imgsz=640,
        batch=16,
        name='vehicle_plate_detector'
    )
    
    print("Training complete. Model saved in runs/detect/vehicle_plate_detector/weights/best.pt")

if __name__ == "__main__":
    train_model()
