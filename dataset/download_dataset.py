import os
from datasets import load_dataset
from PIL import Image
from tqdm import tqdm

def download_and_prepare_dataset():
    print("Loading dataset from Hugging Face Hub...")
    # Using a small and high-quality license plate dataset
    try:
        ds = load_dataset("keremberke/license-plate-object-detection", "full")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # YOLO directory structure
    base_dir = "dataset"
    splits = {
        'train': ds['train'],
        'val': ds['validation']
    }

    print("Preparing images and labels for YOLOv8...")
    
    for split_name, split_data in splits.items():
        images_dir = os.path.join(base_dir, split_name, "images")
        labels_dir = os.path.join(base_dir, split_name, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        # Process first 150 images per split for better accuracy
        max_images = 150 
        
        for i in tqdm(range(min(len(split_data), max_images)), desc=f"Processing {split_name}"):
            item = split_data[i]
            img = item['image']
            image_id = f"plate_{split_name}_{i}"
            
            # 1. Save Image
            img_path = os.path.join(images_dir, f"{image_id}.jpg")
            img.convert("RGB").save(img_path)
            
            # 2. Save Labels (YOLO format: class x_center y_center width height)
            # Hugging Face format usually: [xmin, ymin, width, height]
            label_path = os.path.join(labels_dir, f"{image_id}.txt")
            
            img_w, img_h = img.size
            with open(label_path, "w") as f:
                for obj in item['objects']:
                    bbox = obj['bbox'] # [xmin, ymin, width, height]
                    cls_id = 0 # License Plate
                    
                    # Normalize coordinates
                    x_center = (bbox[0] + bbox[2]/2) / img_w
                    y_center = (bbox[1] + bbox[3]/2) / img_h
                    w = bbox[2] / img_w
                    h = bbox[3] / img_h
                    
                    f.write(f"{cls_id} {x_center} {y_center} {w} {h}\n")

    print(f"\nSuccess! Sample dataset downloaded to '{base_dir}/'.")
    print("You can now run 'python model/train.py' to train your model.")

if __name__ == "__main__":
    # Check for dependencies
    try:
        import datasets
    except ImportError:
        print("Installing required library: datasets...")
        os.system("pip install datasets")
        
    download_and_prepare_dataset()
