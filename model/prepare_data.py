import os
import xml.etree.ElementTree as ET
from glob import glob
import shutil
from sklearn.model_selection import train_test_split

def convert_xml_to_yolo(xml_file, classes):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    
    yolo_data = []
    for obj in root.findall('object'):
        cls = obj.find('name').text
        if cls not in classes: continue
        cls_id = classes.index(cls)
        
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        
        # Normalize coordinates
        bb = ( (b[0] + b[1]) / (2.0 * w), (b[2] + b[3]) / (2.0 * h), 
               (b[1] - b[0]) / w, (b[3] - b[2]) / h)
        yolo_data.append(f"{cls_id} {' '.join([f'{a:.6f}' for a in bb])}")
    return yolo_data

def prepare_dataset(source_dir, output_dir, test_size=0.2):
    classes = ['license_plate', 'License_Plate', 'number_plate'] # Common tags
    yolo_classes = ['license_plate'] # Target tag
    
    # Create structure
    for split in ['train', 'val']:
        os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, split, 'labels'), exist_ok=True)

    xml_files = glob(os.path.join(source_dir, '*.xml'))
    train_files, val_files = train_test_split(xml_files, test_size=test_size, random_state=42)

    def process_files(files, split):
        count = 0
        for xml_path in files:
            # Check for image (try common extensions)
            img_base = os.path.splitext(xml_path)[0]
            img_path = None
            for ext in ['.jpg', '.png', '.jpeg']:
                if os.path.exists(img_base + ext):
                    img_path = img_base + ext
                    break
            
            if img_path:
                yolo_lines = convert_xml_to_yolo(xml_path, classes)
                if yolo_lines:
                    # Copy image
                    shutil.copy(img_path, os.path.join(output_dir, split, 'images', os.path.basename(img_path)))
                    # Write label
                    label_name = os.path.splitext(os.path.basename(xml_path))[0] + '.txt'
                    with open(os.path.join(output_dir, split, 'labels', label_name), 'w') as f:
                        f.write('\n'.join(yolo_lines))
                    count += 1
        return count

    print(f"Processing {len(train_files)} train files...")
    train_count = process_files(train_files, 'train')
    print(f"Processing {len(val_files)} val files...")
    val_count = process_files(val_files, 'val')
    
    print(f"\nDone! Processed {train_count} training and {val_count} validation images.")

if __name__ == "__main__":
    prepare_dataset('Indian_vehicle_dataset', 'dataset/processed')
