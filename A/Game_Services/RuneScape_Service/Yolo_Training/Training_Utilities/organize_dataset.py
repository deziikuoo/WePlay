#!/usr/bin/env python3
"""
Dataset Organization Script
Organizes YOLO training dataset by moving annotation files and splitting into train/val sets
"""

import os
import shutil
import glob
from pathlib import Path
import random


def organize_dataset(activity_name: str = None, dataset_path: str = None):
    """Organize any activity dataset by moving files and creating train/val split"""
    
    # Get activity name if not provided
    if activity_name is None:
        activity_name = input("Activity name (e.g., woodcutting, chicken, mining): ").strip().lower()
        if not activity_name:
            print("❌ Activity name is required!")
            return
    
    # Set dataset path if not provided
    if dataset_path is None:
        script_dir = Path(__file__).parent.parent
        dataset_path = script_dir / f"{activity_name.title()}_Training" / "runescape_dataset"
    
    print(f"📁 Organizing {activity_name.title()} Dataset")
    print("=" * 40)
    
    # Define paths
    dataset_dir = Path(dataset_path)
    images_train = dataset_dir / "images" / "train"
    images_val = dataset_dir / "images" / "val"
    labels_train = dataset_dir / "labels" / "train"
    labels_val = dataset_dir / "labels" / "val"
    
    print(f"📂 Dataset path: {dataset_dir.absolute()}")
    
    # Step 1: Move .txt files from images/train to labels/train
    print("\n🔄 Step 1: Moving annotation files...")
    
    txt_files_in_images = list(images_train.glob("*.txt"))
    if txt_files_in_images:
        print(f"Found {len(txt_files_in_files)} .txt files in images/train")
        
        for txt_file in txt_files_in_images:
            dest_path = labels_train / txt_file.name
            shutil.move(str(txt_file), str(dest_path))
            print(f"   Moved: {txt_file.name}")
        
        print(f"✅ Moved {len(txt_files_in_images)} annotation files to labels/train")
    else:
        print("ℹ️ No .txt files found in images/train")
    
    # Step 2: Get list of all images and their corresponding labels
    print("\n🔄 Step 2: Preparing train/val split...")
    
    image_files = list(images_train.glob("*.jpg")) + list(images_train.glob("*.png"))
    print(f"Found {len(image_files)} images in train folder")
    
    if len(image_files) == 0:
        print("❌ No images found in train folder!")
        return
    
    # Step 3: Create train/val split (80% train, 20% val)
    print("\n🔄 Step 3: Creating train/val split...")
    
    # Shuffle the list for random split
    random.seed(42)  # For reproducible results
    random.shuffle(image_files)
    
    # Calculate split
    val_count = max(1, len(image_files) // 5)  # 20% for validation, minimum 1
    train_count = len(image_files) - val_count
    
    val_files = image_files[:val_count]
    train_files = image_files[val_count:]
    
    print(f"📊 Split: {train_count} training, {val_count} validation")
    
    # Step 4: Move files to validation folders
    print("\n🔄 Step 4: Moving files to validation folders...")
    
    for img_file in val_files:
        # Move image
        img_dest = images_val / img_file.name
        shutil.move(str(img_file), str(img_dest))
        
        # Move corresponding label if it exists
        label_file = labels_train / (img_file.stem + ".txt")
        if label_file.exists():
            label_dest = labels_val / label_file.name
            shutil.move(str(label_file), str(label_dest))
            print(f"   Moved: {img_file.name} + label")
        else:
            print(f"   Moved: {img_file.name} (no label)")
    
    # Step 5: Verify final structure
    print("\n📊 Final Dataset Structure:")
    print("=" * 30)
    
    train_images = len(list(images_train.glob("*.jpg"))) + len(list(images_train.glob("*.png")))
    train_labels = len(list(labels_train.glob("*.txt")))
    val_images = len(list(images_val.glob("*.jpg"))) + len(list(images_val.glob("*.png")))
    val_labels = len(list(labels_val.glob("*.txt")))
    
    print(f"Training images: {train_images}")
    print(f"Training labels: {train_labels}")
    print(f"Validation images: {val_images}")
    print(f"Validation labels: {val_labels}")
    
    # Step 6: Check for missing labels
    print("\n🔍 Checking for missing labels...")
    
    missing_labels = []
    for img_file in images_train.glob("*.jpg"):
        label_file = labels_train / (img_file.stem + ".txt")
        if not label_file.exists():
            missing_labels.append(img_file.name)
    
    for img_file in images_val.glob("*.jpg"):
        label_file = labels_val / (img_file.stem + ".txt")
        if not label_file.exists():
            missing_labels.append(img_file.name)
    
    if missing_labels:
        print(f"⚠️ Found {len(missing_labels)} images without labels:")
        for img in missing_labels[:5]:  # Show first 5
            print(f"   {img}")
        if len(missing_labels) > 5:
            print(f"   ... and {len(missing_labels) - 5} more")
    else:
        print("✅ All images have corresponding labels!")
    
    print("\n🎉 Dataset organization complete!")
    print("\n📋 Next steps:")
    print("1. Review the train/val split")
    print("2. Run: python train_woodcutting_model.py")
    print("3. Monitor training progress")


def main():
    """Main function"""
    print("🌳 RuneScape Dataset Organizer")
    print("=" * 40)
    print("This script will organize your dataset and create train/val split")
    print()
    
    try:
        dataset_path = input("Dataset path [runescape_dataset]: ").strip() or "runescape_dataset"
        
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset path not found: {dataset_path}")
            return
        
        organize_dataset(dataset_path)
        
    except KeyboardInterrupt:
        print("\n⏹️ Organization interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
