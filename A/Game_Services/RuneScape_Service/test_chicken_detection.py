"""
Test script for chicken detection using the trained YOLO model
"""

import sys
import os
import cv2
import time
import tkinter as tk
from tkinter import messagebox
import win32gui
import win32con

# Add the Yolo Detector to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Yolo Detector'))

from runescape_yolo_detector import RuneScapeObjectDetector

def show_completion_notification(chicken_count):
    """Show popup notification when detection is completed"""
    try:
        # Create main tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Create notification message
        if chicken_count > 0:
            title = "🐔 Chicken Detection Complete!"
            message = f"Found {chicken_count} chicken(s)!\n\nDetection completed successfully.\nCheck the debug image for results."
        else:
            title = "🔍 Detection Complete"
            message = "No chickens detected.\n\nDetection completed successfully.\nCheck the debug image for results."
        
        # Force window to stay on top using multiple methods
        root.attributes('-topmost', True)
        root.lift()
        root.focus_force()
        
        # Show popup
        messagebox.showinfo(title, message)
        
        # Get the messagebox window handle and force it to front
        try:
            # Find the messagebox window by title
            def find_messagebox_windows(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if title in window_title or "Detection" in window_title:
                        windows.append(hwnd)
                return True
            
            messagebox_windows = []
            win32gui.EnumWindows(find_messagebox_windows, messagebox_windows)
            
            # Force messagebox to front using Windows API
            for hwnd in messagebox_windows:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                win32gui.SetForegroundWindow(hwnd)
                win32gui.BringWindowToTop(hwnd)
        except Exception as api_error:
            print(f"⚠️ Windows API focus failed: {api_error}")
        
        # Bring to front again using tkinter
        root.lift()
        root.focus_force()
        
        # Destroy the root window
        root.destroy()
        
    except Exception as e:
        print(f"⚠️ Could not show popup notification: {e}")

def test_chicken_detection():
    """Test chicken detection in RuneScape"""
    print("🐔 Testing Chicken Detection in RuneScape")
    print("=" * 50)
    
    try:
        # 5-second delay before starting detection
        print("⏳ Starting in 5 seconds... Get ready!")
        for i in range(5, 0, -1):
            print(f"   {i}...")
            time.sleep(1)
        print("🚀 Starting detection now!")
        print()
        
        # Initialize detector
        detector = RuneScapeObjectDetector()
        
        if detector.model is None:
            print("❌ Failed to initialize detector!")
            return
        
        # Automatically focus the game window before detection
        print("🎯 Focusing game window before detection...")
        if not detector.focus_game_window():
            print("⚠️ Could not focus game window, continuing anyway...")
        time.sleep(0.5)  # Allow time for focus to take effect
        
        print("✅ Detector initialized successfully!")
        print("📸 Capturing game screen...")
        
        # Capture game screen
        frame = detector.capture_game_screen()
        if frame is None:
            print("❌ Failed to capture game screen!")
            print("💡 Make sure RuneScape is running and visible")
            return
        
        print("✅ Game screen captured!")
        print(f"   Image size: {frame.shape}")
        
        # Detect chickens
        print("🔍 Detecting chickens...")
        detections = detector.detect_objects(frame, confidence_threshold=0.3)
        
        # Filter for chickens only
        chicken_detections = detector.filter_detections_by_category(detections, 'chicken')
        
        print(f"📊 Detection Results:")
        print(f"   Total detections: {len(detections)}")
        print(f"   Chicken detections: {len(chicken_detections)}")
        
        if chicken_detections:
            print("🐔 Chickens found:")
            for i, detection in enumerate(chicken_detections):
                print(f"   {i+1}. {detection['class_name']} - Confidence: {detection['confidence']:.3f}")
                print(f"      Position: ({detection['screen_x']}, {detection['screen_y']})")
                print(f"      Bounding box: {detection['bbox']}")
            
            # Get closest chicken
            closest_chicken = detector.get_closest_object(chicken_detections)
            if closest_chicken:
                print(f"\n🎯 Closest chicken:")
                print(f"   {closest_chicken['class_name']} at ({closest_chicken['screen_x']}, {closest_chicken['screen_y']})")
                print(f"   Confidence: {closest_chicken['confidence']:.3f}")
        else:
            print("❌ No chickens detected!")
            print("💡 Try:")
            print("   - Lowering confidence threshold")
            print("   - Making sure chickens are visible in the game")
            print("   - Checking if the model path is correct")
        
        # Save debug image
        print("\n💾 Saving debug image...")
        detector.save_debug_image(frame, detections, "chicken_detection_debug.png")
        
        print("\n✅ Test completed!")
        
        # Show popup notification
        show_completion_notification(len(chicken_detections))
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chicken_detection()
