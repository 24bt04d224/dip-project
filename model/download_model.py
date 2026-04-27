import requests
import os

def download_model():
    url = "https://huggingface.co/Koushim/yolov8-license-plate-detection/resolve/main/best.pt"
    output_path = "model/best.pt"
    
    print(f"Downloading pre-trained license plate model to {output_path}...")
    print("This may take a minute (approx 6MB)...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Verify file size (should be > 1MB)
        if os.path.getsize(output_path) < 1000000:
            print("Error: Downloaded file is too small. It might be corrupted.")
            return False
            
        print("Success! Model downloaded successfully.")
        return True
    except Exception as e:
        print(f"Failed to download model: {e}")
        return False

if __name__ == "__main__":
    if download_model():
        print("\nYou can now run 'python model/detection_pipeline.py'")
