#!/usr/bin/env python3
"""
Dataset Verification Script
Checks for common issues in YOLO training datasets
"""

import os
from pathlib import Path
import yaml

def verify_dataset(activity_name: str = None):
    """Verify any activity dataset for common issues"""
    
    print("🔍 Verifying YOLO Dataset")
    print("=" * 60)
    
    # Get activity name if not provided
    if activity_name is None:
        activity_name = input("Activity name (e.g., woodcutting, chicken, mining): ").strip().lower()
        if not activity_name:
            print("❌ Activity name is required!")
            return
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.parent
    dataset_path = script_dir / f"{activity_name.title()}_Training" / "runescape_dataset"
    
    # Check if dataset exists
    if not dataset_path.exists():
        print(f"❌ Dataset directory not found: {dataset_path}")
        return
    
    # Load configuration
    config_file = f"{activity_name}.yaml"
    configs = {}
    
    config_path = dataset_path / config_file
    if config_path.exists():
        with open(config_path, 'r') as f:
            configs[config_file] = yaml.safe_load(f)
        print(f"✅ Found config: {config_file}")
        print(f"   Classes: {configs[config_file]['names']}")
        print(f"   Number of classes: {configs[config_file]['nc']}")
    else:
        print(f"⚠️ Config not found: {config_file}")
    
    print()
    
    # Check training set
    print("📊 Training Set:")
    print("-" * 60)
    
    train_img_dir = dataset_path / "images" / "train"
    train_lbl_dir = dataset_path / "labels" / "train"
    
    if train_img_dir.exists():
        train_images = list(train_img_dir.glob("*.jpg"))
        print(f"   Images: {len(train_images)}")
    else:
        print(f"   ❌ Training images directory not found")
        train_images = []
    
    if train_lbl_dir.exists():
        train_labels = list(train_lbl_dir.glob("*.txt"))
        # Remove cache files
        train_labels = [l for l in train_labels if not l.name.endswith('.cache')]
        print(f"   Labels: {len(train_labels)}")
    else:
        print(f"   ❌ Training labels directory not found")
        train_labels = []
    
    # Check for missing labels
    if train_images:
        missing_labels = []
        for img in train_images:
            label_path = train_lbl_dir / (img.stem + ".txt")
            if not label_path.exists():
                missing_labels.append(img.name)
        
        if missing_labels:
            print(f"   ⚠️ Missing labels: {len(missing_labels)} images")
            print(f"   ❌ {len(missing_labels)} images have NO annotations!")
            if len(missing_labels) <= 10:
                for img_name in missing_labels[:10]:
                    print(f"      - {img_name}")
            else:
                print(f"      (showing first 10)")
                for img_name in missing_labels[:10]:
                    print(f"      - {img_name}")
        else:
            print(f"   ✅ All images have labels")
    
    # Check for empty labels
    if train_labels:
        empty_labels = []
        total_annotations = 0
        class_counts = {}
        
        for label_file in train_labels:
            with open(label_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    empty_labels.append(label_file.name)
                else:
                    total_annotations += len(lines)
                    # Count classes
                    for line in lines:
                        parts = line.strip().split()
                        if parts:
                            class_id = int(parts[0])
                            class_counts[class_id] = class_counts.get(class_id, 0) + 1
        
        print(f"   Total annotations: {total_annotations}")
        print(f"   Avg annotations per labeled image: {total_annotations / len(train_labels):.2f}")
        
        if empty_labels:
            print(f"   ⚠️ Empty label files: {len(empty_labels)}")
        
        if class_counts:
            print(f"   Class distribution:")
            for class_id, count in sorted(class_counts.items()):
                # Try to get class name from config
                class_name = "unknown"
                for config in configs.values():
                    if class_id < len(config['names']):
                        class_name = config['names'][class_id]
                        break
                print(f"      Class {class_id} ({class_name}): {count} annotations")
    
    print()
    
    # Check validation set
    print("📊 Validation Set:")
    print("-" * 60)
    
    val_img_dir = dataset_path / "images" / "val"
    val_lbl_dir = dataset_path / "labels" / "val"
    
    if val_img_dir.exists():
        val_images = list(val_img_dir.glob("*.jpg"))
        print(f"   Images: {len(val_images)}")
    else:
        print(f"   ❌ Validation images directory not found")
        val_images = []
    
    if val_lbl_dir.exists():
        val_labels = list(val_lbl_dir.glob("*.txt"))
        val_labels = [l for l in val_labels if not l.name.endswith('.cache')]
        print(f"   Labels: {len(val_labels)}")
    else:
        print(f"   ❌ Validation labels directory not found")
        val_labels = []
    
    # Check for missing labels
    if val_images:
        missing_labels = []
        for img in val_images:
            label_path = val_lbl_dir / (img.stem + ".txt")
            if not label_path.exists():
                missing_labels.append(img.name)
        
        if missing_labels:
            print(f"   ⚠️ Missing labels: {len(missing_labels)} images")
            print(f"   ❌ {len(missing_labels)} images have NO annotations!")
        else:
            print(f"   ✅ All images have labels")
    
    # Check for empty labels
    if val_labels:
        total_annotations = 0
        for label_file in val_labels:
            with open(label_file, 'r') as f:
                lines = f.readlines()
                total_annotations += len(lines)
        
        print(f"   Total annotations: {total_annotations}")
        if val_labels:
            print(f"   Avg annotations per labeled image: {total_annotations / len(val_labels):.2f}")
    
    print()
    print("=" * 60)
    print("📋 Summary:")
    print("-" * 60)
    
    total_images = len(train_images) + len(val_images)
    total_labels = len(train_labels) + len(val_labels)
    
    print(f"Total images: {total_images}")
    print(f"Total labels: {total_labels}")
    print(f"Images without labels: {total_images - total_labels}")
    
    if total_labels < total_images * 0.8:
        print()
        print("❌ CRITICAL ISSUE: Less than 80% of images have labels!")
        print("   This will cause very poor training performance.")
        print()
        print("   Solutions:")
        print("   1. Annotate the remaining images")
        print("   2. Delete images without labels")
        print("   3. Check if labels are in the wrong directory")
    elif total_labels < total_images:
        print()
        print("⚠️ WARNING: Some images don't have labels")
        print("   Consider annotating them for better performance")
    else:
        print()
        print("✅ All images have labels - dataset looks good!")
    
    print()
    print("🎯 Recommendations:")
    print("-" * 60)
    
    if len(train_images) < 100:
        print("⚠️ Training set is small (<100 images)")
        print("   Consider collecting more training data")
    
    if len(val_images) < 20:
        print("⚠️ Validation set is small (<20 images)")
        print("   Consider adding more validation images")
    
    if total_labels > 0:
        ratio = len(val_labels) / (len(train_labels) + len(val_labels))
        if ratio < 0.15:
            print(f"⚠️ Validation set is too small ({ratio*100:.1f}% of total)")
            print("   Recommended: 15-20% of data for validation")
        elif ratio > 0.30:
            print(f"⚠️ Validation set is too large ({ratio*100:.1f}% of total)")
            print("   Recommended: 15-20% of data for validation")

if __name__ == "__main__":
    verify_dataset()
