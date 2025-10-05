#!/usr/bin/env python3
"""
RuneScape Data Collection Tool
Automatically captures screenshots of RuneScape for YOLO training dataset
"""

import cv2
import numpy as np
import os
import time
import sys
from datetime import datetime
from typing import Optional

# Add Windows Management to path - absolute path approach
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..', '..', '..', '..')
windows_mgmt_path = os.path.join(project_root, 'B', 'Windows Managment', 'Window_Management_Controls')
sys.path.append(windows_mgmt_path)

try:
    from Windows_Management_Controls import GameWindowManager
except ImportError:
    print(f"❌ Could not import Windows_Management_Controls")
    print(f"📁 Tried path: {windows_mgmt_path}")
    print(f"📁 Current dir: {current_dir}")
    print(f"📁 Project root: {project_root}")
    sys.exit(1)


class RuneScapeDataCollector:
    """Collects RuneScape screenshots for YOLO training"""
    
    def __init__(self, activity_name: str = "runescape", output_dir: str = None):
        self.activity_name = activity_name.lower()
        if output_dir is None:
            # Always save to the main Yolo_Training folder, not relative to current script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_training_dir = os.path.join(script_dir, '..')  # Go up one level to Yolo_Training
            self.output_dir = os.path.join(main_training_dir, f"{self.activity_name.title()}_Training", "runescape_dataset")
        else:
            self.output_dir = output_dir
        self.window_manager = GameWindowManager()
        self.collected_count = 0
        self.start_time = None
        
        # Create directory structure
        self._create_directories()
        
    def _create_directories(self):
        """Create the dataset directory structure"""
        directories = [
            os.path.join(self.output_dir, "images", "train"),
            os.path.join(self.output_dir, "images", "val"),
            os.path.join(self.output_dir, "labels", "train"),
            os.path.join(self.output_dir, "labels", "val"),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
    
    def capture_screenshot(self) -> Optional[np.ndarray]:
        """Capture a screenshot of RuneScape"""
        try:
            if not self.window_manager.game_window:
                print("❌ No RuneScape window found")
                return None
            
            # Get window rectangle directly
            import win32gui
            rect = win32gui.GetWindowRect(self.window_manager.game_window)
            if not rect:
                print("❌ Could not get window rectangle")
                return None
            
            # Adjust for window borders
            x = rect[0] + 8  # Left border
            y = rect[1] + 31  # Title bar
            width = rect[2] - rect[0] - 16  # Right border
            height = rect[3] - rect[1] - 39  # Bottom border
            
            # Capture screenshot
            import pyautogui
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Convert to OpenCV format
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            print(f"❌ Error capturing screenshot: {e}")
            return None
    
    def save_screenshot(self, frame: np.ndarray, split: str = "train") -> str:
        """Save screenshot to appropriate directory"""
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
            filename = f"runescape_{timestamp}.jpg"
            
            # Determine save path (80% train, 20% val)
            if self.collected_count % 5 == 0:  # Every 5th image goes to validation
                split = "val"
            
            save_path = os.path.join(self.output_dir, "images", split, filename)
            
            # Save image
            cv2.imwrite(save_path, frame)
            
            print(f"✅ Saved: {save_path}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving screenshot: {e}")
            return ""
    
    def collect_data(self, target_count: int = 100, interval: float = 2.0):
        """Collect screenshots for training dataset"""
        print(f"🌳 Starting {self.activity_name.title()} data collection...")
        print(f"📊 Target: {target_count} screenshots")
        print(f"⏱️ Interval: {interval} seconds between captures")
        print(f"📁 Output: {self.output_dir}")
        print()
        
        # 5 second delay before starting
        print("⏳ Starting in 5 seconds...")
        time.sleep(5)
        print("🚀 Starting data collection!")
        print()
        
        # Check if RuneScape is running
        if not self.window_manager.game_window:
            print("❌ RuneScape not detected!")
            print("💡 Please launch RuneScape and try again")
            return
        
        print(f"✅ RuneScape detected: {self.window_manager.game_window_title}")
        print()
        
        self.start_time = time.time()
        
        try:
            while self.collected_count < target_count:
                print(f"📸 Capturing screenshot {self.collected_count + 1}/{target_count}...")
                
                # Capture screenshot
                frame = self.capture_screenshot()
                if frame is None:
                    print("❌ Failed to capture screenshot, retrying...")
                    time.sleep(1.0)
                    continue
                
                # Save screenshot
                filename = self.save_screenshot(frame)
                if filename:
                    self.collected_count += 1
                    
                    # Show progress
                    elapsed = time.time() - self.start_time
                    rate = self.collected_count / elapsed if elapsed > 0 else 0
                    eta = (target_count - self.collected_count) / rate if rate > 0 else 0
                    
                    print(f"📊 Progress: {self.collected_count}/{target_count} ({self.collected_count/target_count*100:.1f}%)")
                    print(f"⏱️ Rate: {rate:.1f} images/sec, ETA: {eta/60:.1f} minutes")
                    print()
                
                # Wait before next capture
                if self.collected_count < target_count:
                    print(f"⏳ Waiting {interval} seconds...")
                    time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n⏹️ Data collection interrupted by user")
        
        # Final summary
        elapsed = time.time() - self.start_time
        print(f"\n📊 Collection Complete!")
        print(f"✅ Collected: {self.collected_count} screenshots")
        print(f"⏱️ Time taken: {elapsed/60:.1f} minutes")
        print(f"📁 Saved to: {self.output_dir}")
        print()
        print("🎯 Next steps:")
        print("1. Use LabelImg to annotate the images")
        print("2. Run the training script")
        print("3. Test the custom model")
        
        # Show completion notification over game window
        self._show_completion_notification()
    
    def collect_manual(self):
        """Manual collection mode - press Enter to capture"""
        print(f"🌳 Manual {self.activity_name.title()} data collection mode")
        print("📸 Press ENTER to capture screenshot, 'q' to quit")
        print()
        
        if not self.window_manager.game_window:
            print("❌ RuneScape not detected!")
            return
        
        print(f"✅ RuneScape detected: {self.window_manager.game_window_title}")
        print()
        
        try:
            while True:
                user_input = input("Press ENTER to capture (or 'q' to quit): ").strip().lower()
                
                if user_input == 'q':
                    break
                
                print("📸 Capturing screenshot...")
                frame = self.capture_screenshot()
                
                if frame is not None:
                    filename = self.save_screenshot(frame)
                    if filename:
                        self.collected_count += 1
                        print(f"✅ Screenshot {self.collected_count} saved!")
                else:
                    print("❌ Failed to capture screenshot")
                
                print()
        
        except KeyboardInterrupt:
            print("\n⏹️ Manual collection stopped")
        
        print(f"\n📊 Manual collection complete! Collected {self.collected_count} screenshots")
    
    def _show_completion_notification(self):
        """Show a completion notification over the game window"""
        try:
            import win32gui
            import win32con
            import win32api
            
            if not self.window_manager.game_window:
                print("⚠️ Cannot show notification - no game window found")
                return
            
            # Get game window rectangle
            rect = win32gui.GetWindowRect(self.window_manager.game_window)
            if not rect:
                print("⚠️ Cannot show notification - cannot get window rectangle")
                return
            
            # Calculate center position for notification
            center_x = (rect[0] + rect[2]) // 2
            center_y = (rect[1] + rect[3]) // 2
            
            # Create a simple notification by clicking in the center multiple times
            # This will create a visual "flash" effect
            print("🔔 Showing completion notification over game window...")
            
            for i in range(3):
                # Move cursor to center and click
                win32api.SetCursorPos((center_x, center_y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0)
                time.sleep(0.2)
            
            # Also try to bring the terminal window to front
            try:
                import subprocess
                subprocess.run(['powershell', '-Command', 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("Data collection complete! Checked ' + str(self.collected_count) + ' screenshots collected.", "RuneScape Data Collection", "OK", "Information")'], 
                             capture_output=True, timeout=5)
            except:
                pass  # Fallback if PowerShell notification fails
                
        except Exception as e:
            print(f"⚠️ Could not show notification: {e}")
            print("💡 Check the terminal window for completion status")


def main():
    """Main function"""
    print("🌳 Dynamic RuneScape YOLO Training Data Collector")
    print("=" * 50)
    print("This tool will help you collect screenshots for any activity")
    print()
    
    # Get collection parameters
    try:
        activity_name = input("Activity name (e.g., woodcutting, chicken, mining): ").strip().lower()
        if not activity_name:
            print("❌ Activity name is required!")
            return
            
        mode = input("Collection mode (auto/manual) [auto]: ").strip().lower() or "auto"
        
        if mode == "auto":
            target_count = int(input("Number of screenshots to collect [100]: ") or "100")
            interval = float(input("Interval between captures in seconds [2.0]: ") or "2.0")
            
            collector = RuneScapeDataCollector(activity_name)
            collector.collect_data(target_count, interval)
        
        elif mode == "manual":
            collector = RuneScapeDataCollector(activity_name)
            collector.collect_manual()
        
        else:
            print("❌ Invalid mode. Use 'auto' or 'manual'")
    
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
