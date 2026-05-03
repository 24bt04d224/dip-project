from ultralytics import YOLO
import os
import torch

def train_properly():
    # 1. Hardware Check
    device = '0' if torch.cuda.is_available() else 'cpu'
    print(f"--- Training on {device.upper()} ---")

    # 2. Configuration
    # Ensure paths are absolute for YOLO
    root_dir = os.path.abspath('.')
    data_yaml = os.path.join(root_dir, 'dataset', 'data_expert.yaml')
    
    # Create the expert data.yaml
    with open(data_yaml, 'w') as f:
        f.write(f"path: {os.path.join(root_dir, 'dataset', 'processed')}\n")
        f.write("train: train/images\n")
        f.write("val: val/images\n")
        f.write("\nnames:\n  0: license_plate\n")

    # 3. Load Model
    # Use 'yolov8n.pt' for fast training, 'yolov8s.pt' for better accuracy
    model = YOLO('yolov8n.pt')

    # 4. Train with Expert Hyperparameters
    print("--- Starting Expert Training ---")
    results = model.train(
        data=data_yaml,
        epochs=100,           # Increased for better convergence
        imgsz=640,           # Standard high-quality size
        batch=16,            # Adjust based on memory
        patience=10,         # Early stopping if no improvement
        save=True,           # Save checkpoints
        device=device,
        name='expert_plate_detector',
        exist_ok=True,       # Overwrite existing run with same name
        augment=True,        # Use data augmentation
        lr0=0.01,            # Initial learning rate
        lrf=0.01             # Final learning rate factor
    )

    print("\n--- Training Complete ---")
    best_model_path = os.path.join('runs', 'detect', 'expert_plate_detector', 'weights', 'best.pt')
    print(f"Best model saved at: {best_model_path}")

if __name__ == "__main__":
    train_properly()
