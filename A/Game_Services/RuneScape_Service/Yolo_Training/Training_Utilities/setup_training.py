#!/usr/bin/env python3
"""
RuneScape YOLO Training Setup Script
Sets up the directory structure and configuration for YOLO training
"""

import os
import yaml
from pathlib import Path


def create_dataset_structure(base_path: str = "runescape_dataset"):
    """Create the complete dataset directory structure"""
    print(f"📁 Creating dataset structure at: {base_path}")
    
    directories = [
        os.path.join(base_path, "images", "train"),
        os.path.join(base_path, "images", "val"),
        os.path.join(base_path, "labels", "train"),
        os.path.join(base_path, "labels", "val"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    return base_path


def create_dataset_config(dataset_path: str, activity_name: str, class_names: list):
    """Create the YAML configuration file for YOLO training"""
    config_path = os.path.join(dataset_path, f"{activity_name}.yaml")
    
    config = {
        'path': str(Path(dataset_path).absolute()),
        'train': 'images/train',
        'val': 'images/val',
        'nc': len(class_names),  # number of classes
        'names': class_names
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"✅ Created config: {config_path}")
    return config_path


def create_annotation_template(dataset_path: str):
    """Create a template file showing the annotation format"""
    template_path = os.path.join(dataset_path, "annotation_template.txt")
    
    template_content = """# YOLO Annotation Format Template
# Each line represents one object in the image
# Format: class_id center_x center_y width height
# All coordinates are normalized (0.0 to 1.0)

# Class IDs:
# 0 = tree
# 1 = oak_tree
# 2 = willow_tree
# 3 = rock
# 4 = iron_rock
# 5 = coal_rock

# Example annotations:
# 0 0.5 0.3 0.1 0.2    # A tree in the center-left
# 1 0.8 0.6 0.15 0.25  # An oak tree in the bottom-right
# 3 0.2 0.7 0.08 0.12  # A rock in the bottom-left

# How to annotate:
# 1. Use LabelImg (pip install labelimg)
# 2. Open LabelImg and set format to YOLO
# 3. Draw bounding boxes around objects
# 4. Save annotations as .txt files with same name as images
"""
    
    with open(template_path, 'w') as f:
        f.write(template_content)
    
    print(f"✅ Created template: {template_path}")


def create_readme(dataset_path: str):
    """Create a README file with instructions"""
    readme_path = os.path.join(dataset_path, "README.md")
    
    readme_content = """# RuneScape YOLO Training Dataset

## Directory Structure
```
runescape_dataset/
├── images/
│   ├── train/          # Training images (80% of data)
│   └── val/            # Validation images (20% of data)
├── labels/
│   ├── train/          # Training annotations (.txt files)
│   └── val/            # Validation annotations (.txt files)
├── woodcutting.yaml    # Dataset configuration
├── annotation_template.txt  # Annotation format guide
└── README.md           # This file
```

## Quick Start

### 1. Collect Screenshots
```bash
python collect_runescape_data.py
```

### 2. Annotate Images
```bash
# Install LabelImg
pip install labelimg

# Start annotation tool
labelimg images/train/
```

### 3. Train Model
```bash
python train_runescape_yolo.py
```

### 4. Test Model
```bash
python test_custom_model.py
```

## Object Classes
- **tree**: Regular trees for woodcutting
- **oak_tree**: Oak trees (higher level)
- **willow_tree**: Willow trees (medium level)
- **rock**: Regular mining rocks
- **iron_rock**: Iron rocks (higher level)
- **coal_rock**: Coal rocks (higher level)

## Annotation Guidelines
1. **Draw tight bounding boxes** around objects
2. **Include the entire object** in the box
3. **Don't include background** in the box
4. **Be consistent** with labeling
5. **Quality over quantity** - 100 well-annotated images > 500 poor ones

## Tips for Better Training
- Collect images from **different areas** of RuneScape
- Include **various lighting conditions**
- Capture objects at **different angles**
- Ensure **balanced representation** of all classes
- Use **data augmentation** during training

## Expected Results
- **Minimum viable**: 200-300 annotated images
- **Good performance**: 500-1000 annotated images
- **Excellent performance**: 1000+ annotated images

## Training Time Estimates
- **Small dataset (200 images)**: 1-2 hours
- **Medium dataset (500 images)**: 2-4 hours
- **Large dataset (1000+ images)**: 4-8 hours

## Troubleshooting
- **Low accuracy**: Collect more diverse training data
- **Overfitting**: Add more validation data
- **Slow training**: Use GPU acceleration
- **Memory issues**: Reduce batch size
"""
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created README: {readme_path}")


def main():
    """Main setup function"""
    print("🎮 RuneScape Dynamic YOLO Training Setup")
    print("=" * 50)
    print("This script will set up the directory structure for any activity")
    print()
    
    # Get activity details
    activity_name = input("Activity name (e.g., woodcutting, chicken, mining): ").strip().lower()
    if not activity_name:
        print("❌ Activity name is required!")
        return
        
    # Get class names
    print(f"\nEnter class names for {activity_name} (one per line, empty line to finish):")
    class_names = []
    while True:
        class_name = input(f"Class {len(class_names)}: ").strip()
        if not class_name:
            break
        class_names.append(class_name)
    
    if not class_names:
        print("❌ At least one class is required!")
        return
    
    # Create activity-specific path
    dataset_path = f"{activity_name.title()}_Training/runescape_dataset"
    
    try:
        # Create directory structure
        create_dataset_structure(dataset_path)
        print()
        
        # Create configuration file
        create_dataset_config(dataset_path, activity_name, class_names)
        print()
        
        # Create annotation template
        create_annotation_template(dataset_path)
        print()
        
        
        print(f"🎉 {activity_name.title()} setup complete!")
        print()
        print("📋 Next steps:")
        print("1. Add images to the dataset folders")
        print("2. Annotate images with LabelImg")
        print("3. Run: python train_runescape_yolo.py")
        print(f"   (Select '{activity_name}' as activity)")
        print()
        print(f"📁 Dataset location: {os.path.abspath(dataset_path)}")
        print(f"🎯 Classes: {class_names}")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")


if __name__ == "__main__":
    main()
