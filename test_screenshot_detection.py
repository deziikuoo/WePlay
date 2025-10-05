#!/usr/bin/env python3
"""
Test script for RuneScape YOLO detection with screenshot saving
Takes random screenshots and saves them to root folder for analysis
"""

import os
import sys
import time
import random
import cv2
import numpy as np
from pathlib import Path

# Add the RuneScape service to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'A', 'Game_Services', 'RuneScape_Service'))

try:
    from Yolo_Detector.runescape_yolo_detector import RuneScapeObjectDetector
    print("✅ Successfully imported RuneScapeObjectDetector")
except ImportError as e:
    print(f"❌ Failed to import from Yolo_Detector: {e}")
    print("🔧 Trying alternative import path...")
    try:
        # Try with the actual folder name "Yolo Detector"
        sys.path.append(os.path.join(os.path.dirname(__file__), 'A', 'Game_Services', 'RuneScape_Service', 'Yolo Detector'))
        from runescape_yolo_detector import RuneScapeObjectDetector
        print("✅ Successfully imported RuneScapeObjectDetector with alternative path")
    except ImportError as e2:
        print(f"❌ Failed to import RuneScapeObjectDetector: {e2}")
        print("📁 Available folders in RuneScape_Service:")
        runescape_path = os.path.join(os.path.dirname(__file__), 'A', 'Game_Services', 'RuneScape_Service')
        if os.path.exists(runescape_path):
            for item in os.listdir(runescape_path):
                if os.path.isdir(os.path.join(runescape_path, item)):
                    print(f"   📁 {item}")
        sys.exit(1)

def save_screenshot_with_detections(detector, screenshot_count: int = 5):
    """Take screenshots and save them with detection overlays"""
    
    # Create screenshots folder in root directory
    screenshots_dir = Path("detection_screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    print(f"📸 Starting screenshot detection test...")
    print(f"📁 Screenshots will be saved to: {screenshots_dir.absolute()}")
    print(f"🎯 Taking {screenshot_count} screenshots with detections")
    print()
    
    for i in range(screenshot_count):
        try:
            print(f"📸 Screenshot {i+1}/{screenshot_count}...")
            
            # Capture game screen
            frame = detector.capture_game_screen()
            if frame is None:
                print(f"❌ Failed to capture screenshot {i+1}")
                continue
            
            # Detect objects with low confidence threshold
            detections = detector.detect_objects(frame, confidence_threshold=0.1)
            
            # Create a copy for drawing
            frame_with_detections = frame.copy()
            
            # Draw detection boxes and labels
            for detection in detections:
                bbox = detection['bbox']
                class_name = detection['class_name']
                confidence = detection['confidence']
                
                # Draw bounding box
                x1, y1, x2, y2 = bbox
                cv2.rectangle(frame_with_detections, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                label = f"{class_name}: {confidence:.2f}"
                cv2.putText(frame_with_detections, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Draw center point
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                cv2.circle(frame_with_detections, (center_x, center_y), 3, (255, 0, 0), -1)
                
                print(f"   🎯 Found {class_name} at ({center_x}, {center_y}) with confidence {confidence:.3f}")
            
            # Save original screenshot
            original_path = screenshots_dir / f"screenshot_{i+1:02d}_original.jpg"
            cv2.imwrite(str(original_path), frame)
            
            # Save screenshot with detections
            detection_path = screenshots_dir / f"screenshot_{i+1:02d}_with_detections.jpg"
            cv2.imwrite(str(detection_path), frame_with_detections)
            
            print(f"   💾 Saved: {original_path.name}")
            print(f"   💾 Saved: {detection_path.name}")
            print(f"   📊 Total detections: {len(detections)}")
            print()
            
            # Wait between screenshots (random interval)
            if i < screenshot_count - 1:  # Don't wait after last screenshot
                wait_time = random.uniform(2.0, 5.0)
                print(f"⏳ Waiting {wait_time:.1f} seconds before next screenshot...")
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"❌ Error taking screenshot {i+1}: {e}")
            continue
    
    print(f"✅ Screenshot detection test completed!")
    print(f"📁 Check the 'detection_screenshots' folder in your project root")
    print(f"📊 Look for files like:")
    print(f"   - screenshot_01_original.jpg (raw screenshot)")
    print(f"   - screenshot_01_with_detections.jpg (with green boxes and labels)")

def main():
    """Main function"""
    try:
        print("🔧 Initializing RuneScape Object Detector...")
        detector = RuneScapeObjectDetector()
        
        if detector.model is None:
            print("❌ Failed to initialize detector model")
            return
        
        print("✅ Detector initialized successfully!")
        print(f"🎮 Game window: {detector.game_window_title}")
        print()
        
        # Focus game window
        print("🎯 Focusing game window...")
        if detector.focus_game_window():
            print("✅ Game window focused successfully!")
        else:
            print("⚠️ Could not focus game window, proceeding anyway...")
        
        print()
        
        # Take screenshots with detections
        save_screenshot_with_detections(detector, screenshot_count=5)
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"❌ Error in main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
