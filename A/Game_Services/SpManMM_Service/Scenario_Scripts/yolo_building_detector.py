#!/usr/bin/env python3
"""
YOLOv8 Building Detection for Spider-Man: Miles Morales
Real-time building detection and automated swinging system
"""

import sys
import os
import time
import threading
import cv2
import numpy as np
import pyautogui
import pydirectinput
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
import win32gui
import win32con
from pynput import keyboard
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls

class YOLOBuildingDetector:
    """YOLOv8n building detection system for Spider-Man automation"""
    
    def __init__(self):
        print("Initializing YOLOv8 Building Detector...")
        
        # Initialize YOLOv8n model
        self.model = YOLO('yolov8n.pt')
        
        # Building-related classes in COCO dataset
        self.building_classes = [
            'person',  # Sometimes detects people on buildings
            'car',     # Vehicles near buildings
            'truck',   # Larger vehicles
            'bus',     # Public transport
            'motorcycle',  # Small vehicles
            'bicycle',     # Bikes
            # Note: COCO doesn't have explicit "building" class
            # We'll use edge detection + YOLO for better results
        ]
        
        # Detection parameters
        self.confidence_threshold = 0.5
        self.iou_threshold = 0.45
        
        # Game window detection
        self.game_window = None
        self.game_rect = None
        
        print("✅ YOLOv8 Building Detector initialized!")
    
    def find_game_window(self) -> bool:
        """Find Spider-Man: Miles Morales game window"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if 'spider-man' in window_title.lower() or 'miles morales' in window_title.lower():
                    windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            self.game_window = windows[0][0]
            self.game_rect = win32gui.GetWindowRect(self.game_window)
            print(f"✅ Found game window: {win32gui.GetWindowText(self.game_window)}")
            return True
        else:
            print("❌ Spider-Man: Miles Morales not found")
            return False
    
    def capture_game_screen(self) -> Optional[np.ndarray]:
        """Capture the game window screen"""
        if not self.game_window or not self.game_rect:
            return None
        
        try:
            # Focus game window
            win32gui.SetForegroundWindow(self.game_window)
            time.sleep(0.1)
            
            # Capture window region
            x, y, x2, y2 = self.game_rect
            screenshot = pyautogui.screenshot(region=(x, y, x2-x, y2-y))
            
            # Convert to OpenCV format
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return frame
            
        except Exception as e:
            print(f"❌ Failed to capture screen: {e}")
            return None
    
    def detect_buildings_yolo(self, frame: np.ndarray) -> List[Dict]:
        """Detect buildings using YOLOv8n"""
        try:
            # Run YOLO detection
            results = self.model(frame, conf=self.confidence_threshold, iou=self.iou_threshold)
            
            buildings = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[class_id]
                        
                        # Filter for building-related objects
                        if self._is_building_related(class_name, confidence):
                            buildings.append({
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'confidence': float(confidence),
                                'class': class_name,
                                'class_id': class_id,
                                'center': ((int(x1) + int(x2)) // 2, (int(y1) + int(y2)) // 2),
                                'size': (int(x2 - x1), int(y2 - y1))
                            })
            
            return buildings
            
        except Exception as e:
            print(f"❌ YOLO detection failed: {e}")
            return []
    
    def detect_people(self, frame: np.ndarray) -> List[Dict]:
        """Detect people specifically for super_jump trigger"""
        try:
            # Run YOLO detection
            results = self.model(frame, conf=self.confidence_threshold, iou=self.iou_threshold)
            
            people = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[class_id]
                        
                        # Check specifically for people
                        if class_name == 'person' and confidence > 0.6:  # Higher confidence for people
                            people.append({
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'confidence': float(confidence),
                                'class': class_name,
                                'class_id': class_id,
                                'center': ((int(x1) + int(x2)) // 2, (int(y1) + int(y2)) // 2),
                                'size': (int(x2 - x1), int(y2 - y1))
                            })
            
            return people
            
        except Exception as e:
            print(f"❌ People detection failed: {e}")
            return []
    
    def super_jump(self):
        """Execute super jump maneuver"""
        try:
            print("   🦘 Executing super jump...")
            
            # Super jump sequence: Forward motion + Sprint + Jump timing
            # Forward motion for 1.5 seconds
            pydirectinput.keyDown(self.KEYS['forward'])
            time.sleep(1.5)
            
            # Sprint for 2 seconds while charging jump
            pydirectinput.keyDown(self.KEYS['sprint'])
            time.sleep(2.0)
            
            # Release jump button 0.5 seconds before sprint completes
            pydirectinput.keyDown(self.KEYS['jump'])
            time.sleep(0.5)  # Jump for 0.5 seconds
            
            # Release all keys
            pydirectinput.keyUp(self.KEYS['jump'])
            pydirectinput.keyUp(self.KEYS['sprint'])
            pydirectinput.keyUp(self.KEYS['forward'])
            
            print("   ✅ Super jump completed!")
            
        except Exception as e:
            print(f"❌ Super jump error: {e}")
            # Ensure all keys are released on error
            pydirectinput.keyUp(self.KEYS['jump'])
            pydirectinput.keyUp(self.KEYS['sprint'])
            pydirectinput.keyUp(self.KEYS['forward'])
    
    def detect_buildings_edges(self, frame: np.ndarray) -> List[Dict]:
        """Detect buildings using edge detection (backup method)"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            buildings = []
            for contour in contours:
                # Filter contours by area and aspect ratio
                area = cv2.contourArea(contour)
                if area > 5000:  # Minimum building size
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if it looks like a building (taller than wide)
                    if h > w and h > 100:  # Building-like proportions
                        buildings.append({
                            'bbox': (x, y, x + w, y + h),
                            'confidence': 0.7,  # Fixed confidence for edge detection
                            'class': 'building_edge',
                            'class_id': -1,
                            'center': (x + w // 2, y + h // 2),
                            'size': (w, h)
                        })
            
            return buildings
            
        except Exception as e:
            print(f"❌ Edge detection failed: {e}")
            return []
    
    def _is_building_related(self, class_name: str, confidence: float) -> bool:
        """Check if detected object is building-related"""
        # Since COCO doesn't have explicit building class, we use context clues
        building_context = [
            'person',  # People often indicate buildings
            'car', 'truck', 'bus', 'motorcycle', 'bicycle',  # Vehicles near buildings
            'traffic light', 'stop sign',  # Street infrastructure
            'bench', 'chair',  # Street furniture
        ]
        
        return class_name in building_context and confidence > self.confidence_threshold
    
    def analyze_building_positions(self, buildings: List[Dict], frame_shape: Tuple[int, int]) -> Dict:
        """Analyze building positions relative to player with proximity filtering"""
        if not buildings:
            return {'action': 'forward', 'reason': 'no_buildings'}
        
        height, width = frame_shape[:2]
        center_x = width // 2
        
        # Spider-Man is always centered on screen by the camera
        spiderman_x = center_x
        spiderman_y = height // 2  # Spider-Man is at the vertical center
        
        # Proximity thresholds based on actual distance
        danger_distance = 150  # Very close - immediate danger
        close_distance = 250   # Close - need to avoid
        medium_distance = 400  # Medium - light steering
        
        # Filter buildings by actual distance from Spider-Man
        close_buildings = []
        medium_buildings = []
        far_buildings = []
        debug_distances = []
        
        for building in buildings:
            x, y, x2, y2 = building['bbox']
            building_center_x = (x + x2) // 2
            building_center_y = (y + y2) // 2
            
            # Calculate actual distance from Spider-Man
            distance = ((building_center_x - spiderman_x) ** 2 + (building_center_y - spiderman_y) ** 2) ** 0.5
            debug_distances.append(int(distance))
            
            if distance <= danger_distance:
                close_buildings.append(building)
            elif distance <= close_distance:
                close_buildings.append(building)
            elif distance <= medium_distance:
                medium_buildings.append(building)
            else:
                far_buildings.append(building)
        
        # Only act on close and medium buildings
        relevant_buildings = close_buildings + medium_buildings
        
        if not relevant_buildings:
            return {'action': 'forward', 'reason': 'no_close_buildings', 'buildings': len(far_buildings), 'debug_distances': debug_distances}
        
        # Categorize relevant buildings by horizontal position
        left_buildings = []
        right_buildings = []
        center_buildings = []
        
        for building in relevant_buildings:
            x, y, x2, y2 = building['bbox']
            center_building_x = (x + x2) // 2
            
            if center_building_x < center_x - 80:  # Left side (reduced from 100)
                left_buildings.append(building)
            elif center_building_x > center_x + 80:  # Right side (reduced from 100)
                right_buildings.append(building)
            else:
                center_buildings.append(building)
        
        # Enhanced decision logic with proximity weighting and turn balancing
        close_center = len([b for b in center_buildings if b in close_buildings])
        close_left = len([b for b in left_buildings if b in close_buildings])
        close_right = len([b for b in right_buildings if b in close_buildings])
        
        # Immediate danger - buildings very close in center (randomize direction)
        if close_center > 0:
            # Balance turns - if last turn was left, try right, and vice versa
            last_turn = getattr(self, 'controller', None) and self.controller.last_turn
            if last_turn == 'left_swing':
                action = 'right_swing'
                reason = 'immediate_center_danger_right'
            elif last_turn == 'right_swing':
                action = 'left_swing'
                reason = 'immediate_center_danger_left'
            else:
                # First time or no previous turn - go forward initially
                action = 'forward'
                reason = 'initial_center_danger_forward'
            return {'action': action, 'reason': reason, 'buildings': close_center, 'proximity': 'danger', 'debug_distances': debug_distances}
        
        # Center blocked by medium distance buildings (randomize direction)
        elif len(center_buildings) > 1:
            # Balance turns - if last turn was left, try right, and vice versa
            last_turn = getattr(self, 'controller', None) and self.controller.last_turn
            if last_turn == 'left_swing':
                action = 'right_swing'
                reason = 'center_blocked_right'
            elif last_turn == 'right_swing':
                action = 'left_swing'
                reason = 'center_blocked_left'
            else:
                # First time or no previous turn - go forward initially
                action = 'forward'
                reason = 'initial_center_blocked_forward'
            return {'action': action, 'reason': reason, 'buildings': len(center_buildings), 'proximity': 'medium', 'debug_distances': debug_distances}
        
        # Close buildings on one side - avoid that side
        elif close_left > close_right and close_left > 0:
            return {'action': 'right_swing', 'reason': 'avoid_close_left', 'buildings': close_left, 'proximity': 'close', 'debug_distances': debug_distances}
        elif close_right > close_left and close_right > 0:
            return {'action': 'left_swing', 'reason': 'avoid_close_right', 'buildings': close_right, 'proximity': 'close', 'debug_distances': debug_distances}
        
        # Medium distance buildings - lighter steering
        elif len(left_buildings) > len(right_buildings) + 1:
            return {'action': 'right_swing', 'reason': 'steer_away_left', 'buildings': len(left_buildings), 'proximity': 'medium', 'debug_distances': debug_distances}
        elif len(right_buildings) > len(left_buildings) + 1:
            return {'action': 'left_swing', 'reason': 'steer_away_right', 'buildings': len(right_buildings), 'proximity': 'medium', 'debug_distances': debug_distances}
        
        # Clear path or balanced obstacles
        else:
            return {'action': 'forward', 'reason': 'clear_path', 'buildings': len(relevant_buildings), 'proximity': 'safe', 'debug_distances': debug_distances}
    
    def visualize_detections(self, frame: np.ndarray, buildings: List[Dict], analysis: Dict) -> np.ndarray:
        """Visualize building detections and analysis"""
        vis_frame = frame.copy()
        
        # Draw building bounding boxes
        for building in buildings:
            x, y, x2, y2 = building['bbox']
            confidence = building['confidence']
            class_name = building['class']
            
            # Color based on confidence
            color = (0, 255, 0) if confidence > 0.7 else (0, 255, 255)
            
            # Draw bounding box
            cv2.rectangle(vis_frame, (x, y), (x2, y2), color, 2)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(vis_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw analysis result
        action = analysis['action']
        reason = analysis['reason']
        buildings_count = analysis.get('buildings', 0)
        
        info_text = f"Action: {action} | Reason: {reason} | Buildings: {buildings_count}"
        cv2.putText(vis_frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return vis_frame

class AutoSwingController(SpiderManKeyboardControls):
    """Automated swinging controller using building detection"""
    
    def __init__(self):
        super().__init__()
        self.detector = YOLOBuildingDetector()
        self.is_running = False
        self.swing_thread = None
        self.keyboard_listener = None
        self.last_turn = None  # Track last turn direction for balancing
        
        # Pass the controller reference to the detector for turn tracking
        self.detector.controller = self
        
    def start_auto_swing(self):
        """Start the automated swinging system"""
        if not self.detector.find_game_window():
            print("❌ Cannot start auto-swing: Game window not found")
            return False
        
        self.is_running = True
        
        # Start keyboard listener for End key
        self._start_keyboard_listener()
        
        self.swing_thread = threading.Thread(target=self._auto_swing_loop)
        self.swing_thread.start()
        print("🚀 Auto-swing system started!")
        print("💡 Press 'End' key to stop auto-swing")
        return True
    
    def stop_auto_swing(self):
        """Stop the automated swinging system"""
        self.is_running = False
        
        # Stop keyboard listener
        self._stop_keyboard_listener()
        
        if self.swing_thread:
            self.swing_thread.join()
        print("🛑 Auto-swing system stopped!")
    
    def _auto_swing_loop(self):
        """Main loop for automated swinging"""
        last_swing_time = 0
        swing_cooldown = 1.0  # Minimum time between swings
        
        while self.is_running:
            try:
                current_time = time.time()
                
                # Capture game screen
                frame = self.detector.capture_game_screen()
                if frame is None:
                    time.sleep(0.1)
                    continue
                
                # Check for people first - if detected, just continue swinging normally
                people = self.detector.detect_people(frame)
                if people and current_time - last_swing_time > swing_cooldown:
                    print(f"👥 Person detected - continuing normal swing... ({len(people)} people)")
                    # Continue with normal building detection instead of super_jump
                
                # Detect buildings using both methods
                yolo_buildings = self.detector.detect_buildings_yolo(frame)
                edge_buildings = self.detector.detect_buildings_edges(frame)
                
                # Combine detections
                all_buildings = yolo_buildings + edge_buildings
                
                # Analyze building positions
                analysis = self.detector.analyze_building_positions(all_buildings, frame.shape)
                
                # Execute swing if needed and cooldown allows
                if (analysis['action'] != 'forward' and 
                    current_time - last_swing_time > swing_cooldown):
                    
                    self._execute_swing_action(analysis)
                    last_swing_time = current_time
                
                # Visualize (optional - for debugging)
                if len(all_buildings) > 0:
                    vis_frame = self.detector.visualize_detections(frame, all_buildings, analysis)
                    # Uncomment to show visualization window
                    # cv2.imshow('Building Detection', vis_frame)
                    # cv2.waitKey(1)
                
                # Frame rate control
                time.sleep(1/30)  # 30 FPS processing
                
            except Exception as e:
                print(f"❌ Auto-swing loop error: {e}")
                time.sleep(1.0)
    
    def _execute_swing_action(self, analysis: Dict):
        """Execute the determined swing action"""
        action = analysis['action']
        reason = analysis['reason']
        buildings_count = analysis.get('buildings', 0)
        proximity = analysis.get('proximity', 'unknown')
        
        print(f"🎯 Executing {action} - {reason} ({proximity} proximity, {buildings_count} buildings)")
        
        # Debug: Show distance calculations for first few buildings
        if buildings_count > 0:
            debug_info = analysis.get('debug_distances', [])
            if debug_info:
                print(f"   📏 Distances: {debug_info[:3]}")  # Show first 3 distances
        
        # Track last turn for balancing
        self.last_turn = action
        
        if action == 'left_swing':
            self._swing_left()
        elif action == 'right_swing':
            self._swing_right()
        else:
            self.web_swing_combo()  # Default forward swing
    
    def _swing_left(self):
        """Execute left swing maneuver"""
        print("   Executing left swing...")
        
        # Hold left movement + swing for turn duration
        pydirectinput.keyDown(self.KEYS['left'])
        pydirectinput.keyDown(self.KEYS['swing'])
        time.sleep(1.0)  # Turn for 1 second
        pydirectinput.keyUp(self.KEYS['left'])
        
        # Continue forward motion after turn
        print("   Resuming forward motion...")
        pydirectinput.keyDown(self.KEYS['forward'])
        time.sleep(1.0)  # Forward motion for 1 second
        pydirectinput.keyUp(self.KEYS['forward'])
        pydirectinput.keyUp(self.KEYS['swing'])
    
    def _swing_right(self):
        """Execute right swing maneuver"""
        print("   Executing right swing...")
        
        # Hold right movement + swing for turn duration
        pydirectinput.keyDown(self.KEYS['right'])
        pydirectinput.keyDown(self.KEYS['swing'])
        time.sleep(1.0)  # Turn for 1 second
        pydirectinput.keyUp(self.KEYS['right'])
        
        # Continue forward motion after turn
        print("   Resuming forward motion...")
        pydirectinput.keyDown(self.KEYS['forward'])
        time.sleep(1.0)  # Forward motion for 1 second
        pydirectinput.keyUp(self.KEYS['forward'])
        pydirectinput.keyUp(self.KEYS['swing'])
    
    def _start_keyboard_listener(self):
        """Start keyboard listener for End key"""
        try:
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press
            )
            self.keyboard_listener.start()
        except Exception as e:
            print(f"⚠️ Failed to start keyboard listener: {e}")
    
    def _stop_keyboard_listener(self):
        """Stop keyboard listener"""
        try:
            if self.keyboard_listener:
                self.keyboard_listener.stop()
                self.keyboard_listener = None
        except Exception as e:
            print(f"⚠️ Failed to stop keyboard listener: {e}")
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            # Check if End key is pressed
            if hasattr(key, 'vk') and key.vk == 35:  # End key virtual key code
                print("\n🛑 End key pressed - stopping auto-swing...")
                self.stop_auto_swing()
                return False  # Stop the listener
            elif key == keyboard.Key.end:  # Alternative check for End key
                print("\n🛑 End key pressed - stopping auto-swing...")
                self.stop_auto_swing()
                return False  # Stop the listener
        except Exception as e:
            print(f"⚠️ Error handling key press: {e}")
        
        return True  # Continue listening
    
    def super_jump(self):
        """Execute super jump maneuver"""
        try:
            print("   🦘 Executing super jump...")
            
            # Super jump sequence: Forward motion + Sprint + Jump timing
            # Forward motion for 1.5 seconds
            pydirectinput.keyDown(self.KEYS['forward'])
            time.sleep(1.5)
            
            # Sprint for 2 seconds while charging jump
            pydirectinput.keyDown(self.KEYS['sprint'])
            time.sleep(2.0)
            
            # Release jump button 0.5 seconds before sprint completes
            pydirectinput.keyDown(self.KEYS['jump'])
            time.sleep(0.5)  # Jump for 0.5 seconds
            
            # Release all keys
            pydirectinput.keyUp(self.KEYS['jump'])
            pydirectinput.keyUp(self.KEYS['sprint'])
            pydirectinput.keyUp(self.KEYS['forward'])
            
            print("   ✅ Super jump completed!")
            
        except Exception as e:
            print(f"❌ Super jump error: {e}")
            # Ensure all keys are released on error
            pydirectinput.keyUp(self.KEYS['jump'])
            pydirectinput.keyUp(self.KEYS['sprint'])
            pydirectinput.keyUp(self.KEYS['forward'])

def main():
    """Main function for testing the building detection system"""
    print("YOLOv8 Building Detection for Spider-Man: Miles Morales")
    print("=" * 60)
    
    controller = AutoSwingController()
    
    try:
        if controller.start_auto_swing():
            print("Auto-swing system is running!")
            print("Press Ctrl+C to stop...")
            
            # Keep main thread alive
            while controller.is_running:
                time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping auto-swing system...")
        controller.stop_auto_swing()
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
