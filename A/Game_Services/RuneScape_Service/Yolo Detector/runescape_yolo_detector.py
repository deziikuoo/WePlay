"""
RuneScape YOLO Object Detector
Detects OSRS objects (trees, rocks, NPCs, items, etc.) using YOLOv8
"""

import cv2
import numpy as np
import pyautogui
import time
import sys
import os
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
import win32gui
import win32con
import win32api

# Add Windows Management to path
# Go up 4 levels from Yolo Detector -> RuneScape_Service -> Game_Services -> A -> We-Play, then to B
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
windows_mgmt_path = os.path.join(project_root, 'B', 'Windows Managment', 'Window_Management_Controls')
sys.path.append(windows_mgmt_path)
from Windows_Management_Controls import GameWindowManager


class RuneScapeObjectDetector:
    """YOLO-based object detection for Old School RuneScape"""
    
    def __init__(self):
        self.model = None
        # Initialize centralized window manager
        self.window_manager = GameWindowManager()
        self.game_window = self.window_manager.get_game_window_handle()
        self.game_window_title = self.window_manager.get_game_title()
        
        # OSRS specific object classes we want to detect
        self.target_classes = {
            # Chickens for Combat/Training
            'chicken': ['chicken'],
            
            # Trees for Woodcutting (for future models)
            'tree': ['tree', 'oak tree', 'willow tree', 'maple tree', 'yew tree', 'magic tree'],
            
            # Rocks for Mining (for future models)
            'rock': ['rock', 'tin rock', 'copper rock', 'iron rock', 'coal rock', 'gold rock', 'mithril rock'],
            
            # NPCs for Combat/Quests (for future models)
            'person': ['person', 'man', 'woman', 'goblin', 'cow', 'rat', 'spider'],
            
            # Items/Ground objects (for future models)
            'item': ['bottle', 'coin', 'sword', 'bow', 'arrow', 'potion', 'food'],
            
            # Buildings/Structures (for future models)
            'building': ['house', 'bank', 'shop', 'altar', 'furnace', 'anvil'],
        }
        
        # Initialize YOLO model
        self._initialize_model()
        
        # Game window is already found by centralized manager
    
    def _initialize_model(self):
        """Initialize YOLOv8 model"""
        try:
            print("🔧 Initializing YOLOv8 for RuneScape object detection...")
            # Try to load trained chicken model first, fallback to generic
            trained_model_path = os.path.join(os.path.dirname(__file__), '..', 'Yolo_Training', 'Chicken_Training', 'runs', 'train', 'yolov8n.pt', 'weights', 'best.pt')
            
            if os.path.exists(trained_model_path):
                self.model = YOLO(trained_model_path)
                print("✅ Trained RuneScape chicken detection model loaded successfully!")
                print(f"   Model: {trained_model_path}")
                print("   Classes: chicken")
            else:
                self.model = YOLO('yolov8n.pt')  # Fallback to generic model
                print("⚠️ Using generic YOLO model (trained chicken model not found)")
                print(f"   Expected trained model at: {trained_model_path}")
        except Exception as e:
            print(f"❌ Failed to initialize YOLOv8: {e}")
            self.model = None
    
    
    def capture_game_screen(self) -> Optional[np.ndarray]:
        """Capture screenshot of the RuneScape game window"""
        try:
            if not self.game_window:
                print("❌ No game window detected")
                return None
            
            # Focus the game window before capturing (same as command processor)
            print("🎯 Focusing game window before detection...")
            if not self.window_manager.is_game_focused():
                if not self.window_manager.focus_game():
                    print("⚠️ Could not focus game window, proceeding anyway...")
                else:
                    time.sleep(0.3)  # Allow time for focus to take effect
            
            # Get window rectangle
            rect = win32gui.GetWindowRect(self.game_window)
            
            # Adjust for window borders
            x = rect[0] + 8  # Left border
            y = rect[1] + 31  # Title bar
            width = rect[2] - rect[0] - 16  # Right border
            height = rect[3] - rect[1] - 39  # Bottom border
            
            # Capture screenshot
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Convert to OpenCV format
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            print(f"❌ Error capturing game screen: {e}")
            return None
    
    def detect_objects(self, frame: np.ndarray, confidence_threshold: float = 0.5) -> List[Dict]:
        """Detect objects in the game frame"""
        try:
            if self.model is None:
                return []
            
            # Run YOLO detection
            results = self.model(frame, conf=confidence_threshold)
            
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get detection info
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[class_id]
                        
                        # Calculate center point
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)
                        
                        # Convert to screen coordinates
                        screen_x, screen_y = self._game_to_screen_coords(center_x, center_y)
                        
                        # Categorize object
                        object_category = self._categorize_object(class_name)
                        
                        detection = {
                            'class_name': class_name,
                            'category': object_category,
                            'confidence': float(confidence),
                            'center_x': center_x,
                            'center_y': center_y,
                            'screen_x': screen_x,
                            'screen_y': screen_y,
                            'bbox': (int(x1), int(y1), int(x2), int(y2))
                        }
                        
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"❌ Error detecting objects: {e}")
            return []
    
    def _game_to_screen_coords(self, game_x: int, game_y: int) -> Tuple[int, int]:
        """Convert game coordinates to screen coordinates"""
        try:
            if self.game_window:
                rect = win32gui.GetWindowRect(self.game_window)
                screen_x = rect[0] + 8 + game_x  # Add window position + border
                screen_y = rect[1] + 31 + game_y  # Add window position + title bar
                return screen_x, screen_y
            return game_x, game_y
        except Exception as e:
            print(f"❌ Error converting coordinates: {e}")
            return game_x, game_y
    
    def _categorize_object(self, class_name: str) -> str:
        """Categorize detected object into OSRS categories"""
        class_name_lower = class_name.lower()
        
        for category, keywords in self.target_classes.items():
            for keyword in keywords:
                if keyword in class_name_lower:
                    return category
        
        return 'unknown'
    
    def filter_detections_by_category(self, detections: List[Dict], category: str) -> List[Dict]:
        """Filter detections by object category"""
        return [det for det in detections if det['category'] == category]
    
    def focus_game_window(self) -> bool:
        """Focus the game window using the same methods as command processor"""
        try:
            print("🎯 Focusing RuneScape game window...")
            
            # Refresh game detection to ensure we have the right window
            print("🔄 Refreshing game window detection...")
            if self.window_manager.refresh_game_detection():
                self.game_window = self.window_manager.game_window
                self.game_window_title = self.window_manager.game_window_title
                print(f"🎮 Updated game window: {self.game_window_title}")
            
            if not self.game_window:
                print("❌ No game window detected")
                return False
            
            # Use the same robust focusing methods as command processor
            if self.window_manager.focus_game():
                print(f"✅ Game window focused: {self.game_window_title}")
                return True
            else:
                print("❌ Failed to focus game window")
                return False
                
        except Exception as e:
            print(f"❌ Error focusing game window: {e}")
            return False
    
    def get_closest_object(self, detections: List[Dict], reference_x: int = None, reference_y: int = None) -> Optional[Dict]:
        """Get the closest object to a reference point (default: screen center)"""
        if not detections:
            return None
        
        if reference_x is None or reference_y is None:
            # Use screen center as reference
            reference_x = 640  # Approximate screen center
            reference_y = 360
        
        closest_detection = None
        min_distance = float('inf')
        
        for detection in detections:
            distance = np.sqrt(
                (detection['screen_x'] - reference_x) ** 2 + 
                (detection['screen_y'] - reference_y) ** 2
            )
            
            if distance < min_distance:
                min_distance = distance
                closest_detection = detection
        
        return closest_detection
    
    def detect_and_get_object(self, object_type: str, confidence_threshold: float = 0.5) -> Optional[Dict]:
        """Detect objects and return the closest one of specified type"""
        try:
            # Capture current screen
            frame = self.capture_game_screen()
            if frame is None:
                return None
            
            # Detect all objects
            detections = self.detect_objects(frame, confidence_threshold)
            
            # Filter by object type
            filtered_detections = self.filter_detections_by_category(detections, object_type)
            
            if not filtered_detections:
                print(f"❌ No {object_type} objects detected")
                return None
            
            # Get closest object
            closest_object = self.get_closest_object(filtered_detections)
            
            if closest_object:
                print(f"🎯 Found closest {object_type}: {closest_object['class_name']} at ({closest_object['screen_x']}, {closest_object['screen_y']})")
            
            return closest_object
            
        except Exception as e:
            print(f"❌ Error detecting {object_type}: {e}")
            return None
    
    def save_debug_image(self, frame: np.ndarray, detections: List[Dict], filename: str = "runescape_debug.png"):
        """Save debug image with detection boxes"""
        try:
            debug_frame = frame.copy()
            
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                class_name = detection['class_name']
                confidence = detection['confidence']
                category = detection['category']
                
                # Draw bounding box
                color = self._get_category_color(category)
                cv2.rectangle(debug_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_name} ({category}) {confidence:.2f}"
                cv2.putText(debug_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Draw center point
                center_x, center_y = detection['center_x'], detection['center_y']
                cv2.circle(debug_frame, (center_x, center_y), 5, color, -1)
            
            cv2.imwrite(filename, debug_frame)
            print(f"💾 Saved debug image: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving debug image: {e}")
    
    def _get_category_color(self, category: str) -> Tuple[int, int, int]:
        """Get color for drawing detection boxes by category"""
        colors = {
            'chicken': (255, 165, 0),  # Orange for chickens
            'tree': (0, 255, 0),       # Green
            'rock': (255, 0, 0),       # Blue
            'person': (0, 0, 255),     # Red
            'item': (255, 255, 0),     # Cyan
            'building': (255, 0, 255), # Magenta
            'unknown': (128, 128, 128) # Gray
        }
        return colors.get(category, (128, 128, 128))
