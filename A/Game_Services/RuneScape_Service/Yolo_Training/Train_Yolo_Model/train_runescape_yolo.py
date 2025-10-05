#!/usr/bin/env python3
"""
RuneScape YOLO Training Script
Dynamic training script for any RuneScape activity (woodcutting, chicken hunting, etc.)
"""

import os
import sys
import yaml
from pathlib import Path
from ultralytics import YOLO
import torch


class RuneScapeYOLOTrainer:
    """Dynamic YOLO trainer for different RuneScape activities"""
    
    def __init__(self, activity_name: str, dataset_path: str = None):
        self.activity_name = activity_name.lower()
        
        # Set dataset path based on activity
        if dataset_path is None:
            # Use absolute path to Yolo_Training directory
            base_path = Path(r"C:\Users\dawan\OneDrive\Documents\Coding Files\We-Play\A\Game_Services\RuneScape_Service\Yolo_Training")
            self.dataset_path = base_path / f"{self.activity_name.title()}_Training" / "runescape_dataset"
        else:
            self.dataset_path = Path(dataset_path)
            
        self.config_path = self.dataset_path / f"{self.activity_name}.yaml"
        self.model = None
        
    def create_dataset_config(self, class_names: list):
        """Create YAML configuration file for the dataset"""
        config = {
            'path': str(self.dataset_path.absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'nc': len(class_names),  # number of classes
            'names': class_names
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"✅ Created dataset config: {self.config_path}")
        return config
    
    def validate_dataset(self):
        """Validate that the dataset is properly structured"""
        print("🔍 Validating dataset structure...")
        
        required_dirs = [
            self.dataset_path / "images" / "train",
            self.dataset_path / "images" / "val",
            self.dataset_path / "labels" / "train", 
            self.dataset_path / "labels" / "val"
        ]
        
        for directory in required_dirs:
            if not directory.exists():
                print(f"❌ Missing directory: {directory}")
                return False
            print(f"✅ Found: {directory}")
        
        # Check for images and labels
        train_images = list((self.dataset_path / "images" / "train").glob("*.jpg"))
        train_labels = list((self.dataset_path / "labels" / "train").glob("*.txt"))
        val_images = list((self.dataset_path / "images" / "val").glob("*.jpg"))
        val_labels = list((self.dataset_path / "labels" / "val").glob("*.txt"))
        
        print(f"📊 Dataset statistics:")
        print(f"   Training images: {len(train_images)}")
        print(f"   Training labels: {len(train_labels)}")
        print(f"   Validation images: {len(val_images)}")
        print(f"   Validation labels: {len(val_labels)}")
        
        if len(train_images) == 0:
            print("❌ No training images found!")
            return False
        
        if len(val_images) == 0:
            print("⚠️ No validation images found - consider adding some")
        
        return True
    
    def train_model(self, epochs: int = 100, imgsz: int = 640, batch: int = 16, 
                   model_size: str = "n", device: str = "cuda", model_name: str = None):
        """Train the YOLO model"""
        if model_name is None:
            model_name = f"{self.activity_name}_custom"
            
        print(f"🏋️ Starting YOLO training for {self.activity_name.title()}...")
        print(f"📊 Parameters:")
        print(f"   Activity: {self.activity_name}")
        print(f"   Epochs: {epochs}")
        print(f"   Image size: {imgsz}")
        print(f"   Batch size: {batch}")
        print(f"   Model size: yolov8{model_size}")
        print(f"   Device: {device}")
        print(f"   Model name: {model_name}")
        print()
        
        # Check if dataset config exists
        if not self.config_path.exists():
            print("❌ Dataset config not found!")
            print(f"   Expected: {self.config_path}")
            print("   Please create the config file first or use create_dataset_config()")
            return None
        
        # Validate dataset
        if not self.validate_dataset():
            print("❌ Dataset validation failed!")
            return None
        
        try:
            # Load pre-trained model
            model_name = f"yolov8{model_size}.pt"
            print(f"🔄 Loading pre-trained model: {model_name}")
            self.model = YOLO(model_name)
            
            # Force GPU usage only - no CPU fallback
            if not torch.cuda.is_available():
                raise RuntimeError("❌ GPU not available! Training requires CUDA-capable GPU. No CPU fallback allowed.")
            
            print(f"🖥️ Using device: {device} (GPU-only mode)")
            print(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"💾 GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Start training
            print("🚀 Starting training...")
            results = self.model.train(
                data=str(self.config_path),
                epochs=epochs,
                imgsz=imgsz,
                batch=batch,
                device=device,
                name=model_name,  # Use custom model name
                project=f'{self.activity_name.title()}_Training/runs/train',
                save=True,
                save_period=10,  # Save checkpoint every 10 epochs
                patience=20,     # Early stopping patience
                verbose=True
            )
            
            print("✅ Training completed!")
            return results
            
        except RuntimeError as e:
            print(f"❌ GPU Error: {e}")
            print("💡 Solutions:")
            print("   1. Ensure you have a CUDA-capable GPU")
            print("   2. Install CUDA toolkit and cuDNN")
            print("   3. Install PyTorch with CUDA support: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
            return None
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return None
    
    def test_model(self, model_path: str = None, model_name: str = None):
        """Test the trained model"""
        if model_path is None:
            # Find the best model from training - use the actual model name that YOLO saves
            if model_name is None:
                model_name = "yolov8n.pt"  # Default model name
            model_path = f"{self.activity_name.title()}_Training/runs/train/{model_name}/weights/best.pt"
        
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            return
        
        print(f"🧪 Testing model: {model_path}")
        
        try:
            # Load trained model
            model = YOLO(model_path)
            
            # Test on validation set
            val_path = self.dataset_path / "images" / "val"
            if val_path.exists():
                val_images = list(val_path.glob("*.jpg"))
                if val_images:
                    print(f"📊 Testing on {len(val_images)} validation images...")
                    
                    # Run validation
                    results = model.val(data=str(self.config_path))
                    
                    print("📈 Validation Results:")
                    print(f"   mAP@0.5: {results.box.map50:.3f}")
                    print(f"   mAP@0.5:0.95: {results.box.map:.3f}")
                    print(f"   Precision: {results.box.mp:.3f}")
                    print(f"   Recall: {results.box.mr:.3f}")
                else:
                    print("⚠️ No validation images found for testing")
            else:
                print("⚠️ No validation directory found")
                
        except Exception as e:
            print(f"❌ Testing failed: {e}")
    
    def export_model(self, model_path: str = None, model_name: str = None, format: str = "onnx"):
        """Export trained model to different formats"""
        if model_path is None:
            if model_name is None:
                model_name = "yolov8n.pt"  # Default model name
            model_path = f"{self.activity_name.title()}_Training/runs/train/{model_name}/weights/best.pt"
        
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            return
        
        print(f"📦 Exporting model to {format.upper()} format...")
        
        try:
            model = YOLO(model_path)
            exported_path = model.export(format=format)
            print(f"✅ Model exported to: {exported_path}")
            return exported_path
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None


def create_activity_config(activity_name: str, class_names: list):
    """Helper function to create activity-specific config"""
    trainer = RuneScapeYOLOTrainer(activity_name)
    trainer.create_dataset_config(class_names)
    print(f"✅ Created config for {activity_name.title()} with classes: {class_names}")


def main():
    """Main training function"""
    print("🎮 RuneScape Dynamic YOLO Training Script")
    print("=" * 50)
    print("This script will train a custom YOLO model for any RuneScape activity")
    print()
    
    # Get training parameters
    try:
        activity_name = input("Activity name (e.g., woodcutting, chicken, mining): ").strip().lower()
        if not activity_name:
            print("❌ Activity name is required!")
            return
            
        epochs = int(input("Number of epochs [100]: ") or "100")
        batch_size = int(input("Batch size [16]: ") or "16")
        model_size = input("Model size (n/s/m/l/x) [n]: ").strip() or "n"
        
        # Check GPU availability before starting
        if not torch.cuda.is_available():
            print("❌ GPU not available! This script requires CUDA-capable GPU.")
            print("💡 Install PyTorch with CUDA: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
            return
        
        # Create trainer
        trainer = RuneScapeYOLOTrainer(activity_name)
        
        # Start training
        results = trainer.train_model(
            epochs=epochs,
            batch=batch_size,
            model_size=model_size
        )
        
        if results:
            print("\n🎉 Training completed successfully!")
            
            # Test the model
            test_model = input("\nTest the trained model? (y/n) [y]: ").strip().lower() or "y"
            if test_model == 'y':
                trainer.test_model(model_name=f"yolov8{model_size}.pt")
            
            # Export model
            export_model = input("\nExport model to ONNX? (y/n) [n]: ").strip().lower() or "n"
            if export_model == 'y':
                trainer.export_model(model_name=f"yolov8{model_size}.pt")
            
            print(f"\n🎯 Next steps for {activity_name.title()}:")
            print(f"1. Copy the trained model to your RuneScape service")
            print(f"2. Update runescape_yolo_detector.py to use the new {activity_name} model")
            print(f"3. Test the improved detection in RuneScape")
        
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
