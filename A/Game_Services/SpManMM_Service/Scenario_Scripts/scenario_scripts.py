#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Scenario Scripts
This module provides composite scenario commands that combine multiple basic actions
into fluid gameplay sequences.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls
import time
import pydirectinput
import threading

class SpiderManScenarioScripts(SpiderManKeyboardControls):
    """Spider-Man composite scenario scripts"""
    
    def __init__(self, gamepad=None):
        super().__init__()
        self.gamepad = gamepad  # Keep gamepad for backward compatibility
        self.keyboard_listener = None
        self.auto_walk_running = False
    
    def _hold_keys_concurrent(self, keys, duration):
        """Hold multiple keys simultaneously for a specified duration"""
        def hold_key(key, duration):
            pydirectinput.keyDown(key)
            time.sleep(duration)
            pydirectinput.keyUp(key)
        
        # Create threads for each key
        threads = []
        for key in keys:
            thread = threading.Thread(target=hold_key, args=(key, duration))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    
    # === MOVEMENT & NAVIGATION SCENARIOS ===
    
    def super_jump(self):
        """Super Jump: Enhanced jump sequence with momentum building and sprint charging"""
        print("Super Jump!")
        
        # Phase 1: Initial forward motion (1.5 seconds)
        print("   Phase 1: Building initial momentum...")
        self._hold_key(self.KEYS['forward'], 1.5)
        
        # Phase 2: Start sprint + forward + jump combo for 2 seconds
        print("   Phase 2: Sprinting and charging jump...")
        # Press all three keys: Shift (sprint) + W (forward) + Space (jump)
        pydirectinput.keyDown(self.KEYS['swing'])    # Shift
        pydirectinput.keyDown(self.KEYS['forward'])  # W
        pydirectinput.keyDown(self.KEYS['jump'])     # Space
        
        # Hold for 1.5 seconds (jump will be released 0.5s before sprint ends)
        time.sleep(1.5)
        
        # Phase 3: Release jump 0.5 seconds before sprint ends
        print("   Phase 3: Releasing jump!")
        pydirectinput.keyUp(self.KEYS['jump'])  # Release Space
        
        # Continue sprint + forward for remaining 0.5 seconds
        time.sleep(0.5)
        
        # Release remaining keys
        pydirectinput.keyUp(self.KEYS['forward'])  # Release W
        pydirectinput.keyUp(self.KEYS['swing'])    # Release Shift
        
        print("   Super jump sequence completed!")
    
    def web_swing_combo(self):
        """Web-Swing Combo: Sprint charging with jump release and multiple swing sequences"""
        print("Web-Swing Combo!")
        
        # Start continuous sprint + forward movement for entire duration (17s)
        print("   Starting continuous sprint + forward movement...")
        
        # Create threads for continuous keys
        sprint_thread = threading.Thread(target=self._hold_key_threaded, args=(self.KEYS['swing'], 10))  # Sprint (Shift) for entire duration
        forward_thread = threading.Thread(target=self._hold_key_threaded, args=(self.KEYS['forward'], 10))  # Forward (W) for entire duration
        
        sprint_thread.start()
        forward_thread.start()
        
        # Create threads for timed actions
        jump_thread = threading.Thread(target=self._delayed_jump, args=(1, 1))  # Jump at 1s for 1s duration
        swing_reset_1_thread = threading.Thread(target=self._delayed_swing_reset, args=(5, 2))  # First swing reset at 5s (1s release + 1s hold)
        swing_reset_2_thread = threading.Thread(target=self._delayed_swing_reset, args=(6, 5))  # Second swing reset at 6s (1s release + 4s hold)
        
        jump_thread.start()
        swing_reset_1_thread.start()
        swing_reset_2_thread.start()
        
        # Wait for continuous threads to finish (10 seconds)
        sprint_thread.join()
        forward_thread.join()
        
        # Wait for timed action threads to finish
        jump_thread.join()
        swing_reset_1_thread.join()
        swing_reset_2_thread.join()
        
        print("   Web-swing combo completed!")
    
    def _delayed_jump(self, delay, duration):
        """Execute jump after delay for specified duration"""
        time.sleep(delay)
        print("   Phase 2: Jump charging (1 second)...")
        pydirectinput.keyDown(self.KEYS['jump'])
        time.sleep(duration)
        pydirectinput.keyUp(self.KEYS['jump'])
    
    def _delayed_swing_reset(self, delay, duration):
        """Execute swing reset after delay for specified duration"""
        time.sleep(delay)
        print(f"   Swing reset at {delay}s for {duration}s...")
        pydirectinput.keyUp(self.KEYS['swing'])      # Release Shift (swing/sprint)
        time.sleep(1)  # Brief release
        pydirectinput.keyDown(self.KEYS['swing'])    # Re-hold Shift (swing/sprint)
        time.sleep(duration - 1)  # Continue for remaining time
    
    def _hold_key_threaded(self, key, duration):
        """Helper method to hold a key in a separate thread"""
        pydirectinput.keyDown(key)
        time.sleep(duration)
        pydirectinput.keyUp(key)
    
    def _start_auto_swing(self):
        """Start YOLOv8 building detection and automated swinging"""
        try:
            import sys
            import os
            # Add the Scenario_Scripts directory to Python path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if script_dir not in sys.path:
                sys.path.append(script_dir)
            from yolo_building_detector import AutoSwingController
            
            if not hasattr(self, 'auto_swing_controller'):
                self.auto_swing_controller = AutoSwingController()
            
            if self.auto_swing_controller.start_auto_swing():
                print("✅ YOLOv8 Auto-Swing system started!")
            else:
                print("❌ Failed to start auto-swing system")
                
        except ImportError:
            print("❌ YOLOv8 dependencies not installed. Run: pip install -r requirements_yolo.txt")
        except Exception as e:
            print(f"❌ Auto-swing startup error: {e}")
    
    def _stop_auto_swing(self):
        """Stop the automated swinging system"""
        try:
            if hasattr(self, 'auto_swing_controller'):
                self.auto_swing_controller.stop_auto_swing()
                print("✅ Auto-swing system stopped!")
            else:
                print("⚠️ Auto-swing system not running")
        except Exception as e:
            print(f"❌ Auto-swing stop error: {e}")
    
    def _start_auto_walk(self):
        """Start continuous auto-walking forward"""
        try:
            print("🚶 Starting auto-walk system...")
            print("💡 Press 'End' key to stop auto-walk")
            
            # Start keyboard listener for End key
            self._start_keyboard_listener()
            
            # Start auto-walk thread
            self.auto_walk_thread = threading.Thread(target=self._auto_walk_loop)
            self.auto_walk_running = True
            self.auto_walk_thread.start()
            
        except Exception as e:
            print(f"❌ Auto-walk startup error: {e}")
    
    def _start_path_following(self):
        """Start path-following system to keep Spider-Man centered on paths"""
        try:
            print("🛤️ Starting path-following system...")
            print("💡 Press 'End' key to stop path-following")
            
            # Start keyboard listener for End key
            self._start_keyboard_listener()
            
            # Start path-following thread
            self.auto_walk_thread = threading.Thread(target=self._path_following_loop)
            self.auto_walk_running = True
            self.auto_walk_thread.start()
            
        except Exception as e:
            print(f"❌ Path-following startup error: {e}")
    
    def _stop_auto_walk(self):
        """Stop the auto-walking system"""
        try:
            self.auto_walk_running = False
            if hasattr(self, 'auto_walk_thread') and self.auto_walk_thread:
                self.auto_walk_thread.join()
            
            # Stop keyboard listener
            self._stop_keyboard_listener()
            
            print("✅ Auto-walk system stopped!")
        except Exception as e:
            print(f"❌ Auto-walk stop error: {e}")
    
    def _auto_walk_loop(self):
        """Main loop for obstacle-avoiding walking in Central Park"""
        try:
            # Import the building detector for obstacle detection
            import sys
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if script_dir not in sys.path:
                sys.path.append(script_dir)
            from yolo_building_detector import YOLOBuildingDetector
            
            detector = YOLOBuildingDetector()
            if not detector.find_game_window():
                print("❌ Cannot start auto-walk: Game window not found")
                return
            
            last_avoid_time = 0
            avoid_cooldown = 0.5  # 0.5 second cooldown between avoidance maneuvers
            
            print("🌳 Starting Central Park auto-walk with obstacle detection...")
            
            while self.auto_walk_running:
                current_time = time.time()
                
                # Capture game screen for obstacle detection
                frame = detector.capture_game_screen()
                if frame is None:
                    time.sleep(0.1)
                    continue
                
                # Detect Central Park obstacles (trees, benches, light poles, garbage cans, persons)
                obstacles = self._detect_central_park_obstacles(frame, detector)
                
                # Check if we need to avoid obstacles
                if obstacles and current_time - last_avoid_time > avoid_cooldown:
                    avoidance_action = self._determine_avoidance_action(obstacles, frame.shape)
                    if avoidance_action['action'] != 'forward':
                        print(f"🚫 Avoiding {avoidance_action['reason']} - {len(obstacles)} obstacles")
                        self._execute_avoidance_maneuver(avoidance_action)
                        last_avoid_time = current_time
                        continue  # Skip normal walking this frame
                
                # Normal forward walking
                pydirectinput.keyDown(self.KEYS['forward'])
                time.sleep(0.1)
                pydirectinput.keyUp(self.KEYS['forward'])
                time.sleep(0.05)
                
        except Exception as e:
            print(f"❌ Auto-walk loop error: {e}")
        finally:
            # Ensure forward key is released when stopping
            pydirectinput.keyUp(self.KEYS['forward'])
    
    def _detect_central_park_obstacles(self, frame, detector):
        """Detect Central Park specific obstacles"""
        try:
            # Get YOLO detections
            results = detector.model(frame, conf=0.4, iou=0.3)  # Lower confidence for more detections
            
            obstacles = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = detector.model.names[class_id]
                        
                        # Central Park obstacles to avoid
                        park_obstacles = [
                            'person',      # People walking
                            'bench',       # Park benches
                            'chair',       # Chairs/seating
                            'bottle',      # Garbage cans/trash
                            'cup',         # Trash items
                            'car',         # Vehicles (rare in park but possible)
                            'truck',       # Maintenance vehicles
                        ]
                        
                        if class_name in park_obstacles and confidence > 0.4:
                            obstacles.append({
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'confidence': float(confidence),
                                'class': class_name,
                                'class_id': class_id,
                                'center': ((int(x1) + int(x2)) // 2, (int(y1) + int(y2)) // 2),
                                'size': (int(x2 - x1), int(y2 - y1))
                            })
            
            return obstacles
            
        except Exception as e:
            print(f"❌ Obstacle detection failed: {e}")
            return []
    
    def _determine_avoidance_action(self, obstacles, frame_shape):
        """Determine sharp avoidance action based on obstacle positions"""
        height, width = frame_shape[:2]
        center_x = width // 2
        spiderman_x = center_x
        spiderman_y = height // 2
        
        # Calculate distances and categorize obstacles
        close_obstacles = []
        for obstacle in obstacles:
            x, y, x2, y2 = obstacle['bbox']
            obstacle_center_x = (x + x2) // 2
            obstacle_center_y = (y + y2) // 2
            
            # Calculate distance from Spider-Man
            distance = ((obstacle_center_x - spiderman_x) ** 2 + (obstacle_center_y - spiderman_y) ** 2) ** 0.5
            
            # Only avoid obstacles within 200 pixels (close range)
            if distance <= 200:
                obstacle['distance'] = distance
                close_obstacles.append(obstacle)
        
        if not close_obstacles:
            return {'action': 'forward', 'reason': 'no_close_obstacles'}
        
        # Categorize by horizontal position
        left_obstacles = []
        right_obstacles = []
        center_obstacles = []
        
        for obstacle in close_obstacles:
            x, y, x2, y2 = obstacle['bbox']
            obstacle_center_x = (x + x2) // 2
            
            if obstacle_center_x < center_x - 60:  # Left side
                left_obstacles.append(obstacle)
            elif obstacle_center_x > center_x + 60:  # Right side
                right_obstacles.append(obstacle)
            else:  # Center path
                center_obstacles.append(obstacle)
        
        # Sharp avoidance logic - prioritize center obstacles
        if center_obstacles:
            # Center blocked - sharp turn (randomize direction)
            import random
            action = random.choice(['left', 'right'])
            reason = f'center_blocked_{action}'
            return {'action': action, 'reason': reason, 'obstacles': len(center_obstacles)}
        elif len(left_obstacles) > len(right_obstacles):
            # More obstacles on left - sharp right turn
            return {'action': 'right', 'reason': 'avoid_left_obstacles', 'obstacles': len(left_obstacles)}
        elif len(right_obstacles) > len(left_obstacles):
            # More obstacles on right - sharp left turn
            return {'action': 'left', 'reason': 'avoid_right_obstacles', 'obstacles': len(right_obstacles)}
        else:
            # Balanced - continue forward
            return {'action': 'forward', 'reason': 'balanced_obstacles', 'obstacles': len(close_obstacles)}
    
    def _execute_avoidance_maneuver(self, avoidance_action):
        """Execute sharp turning maneuver with quick readjustment"""
        action = avoidance_action['action']
        reason = avoidance_action['reason']
        obstacle_count = avoidance_action['obstacles']
        
        print(f"   🚫 Sharp {action} turn - {reason} ({obstacle_count} obstacles)")
        
        if action == 'left':
            # Sharp left turn
            pydirectinput.keyDown(self.KEYS['left'])
            time.sleep(0.3)  # Very quick turn
            pydirectinput.keyUp(self.KEYS['left'])
        elif action == 'right':
            # Sharp right turn
            pydirectinput.keyDown(self.KEYS['right'])
            time.sleep(0.3)  # Very quick turn
            pydirectinput.keyUp(self.KEYS['right'])
        
        # Quick readjustment back to forward
        print("   ⚡ Quick readjustment to forward...")
        pydirectinput.keyDown(self.KEYS['forward'])
        time.sleep(0.2)  # Brief forward motion
        pydirectinput.keyUp(self.KEYS['forward'])
    
    def _path_following_loop(self):
        """Main loop for path-following with continuous walk mode and steering"""
        try:
            # Import the building detector for screen capture
            import sys
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if script_dir not in sys.path:
                sys.path.append(script_dir)
            from yolo_building_detector import YOLOBuildingDetector
            
            detector = YOLOBuildingDetector()
            if not detector.find_game_window():
                print("❌ Cannot start path-following: Game window not found")
                return
            
            last_correction_time = 0
            correction_cooldown = 0.3  # 0.3 second cooldown between corrections
            
            print("🛤️ Starting path-following with continuous walk mode...")
            print("🚶 Holding Left-Alt (walk mode) + W (forward) continuously...")
            
            # Start continuous walk mode: Hold Left-Alt + W for entire duration
            pydirectinput.keyDown(self.KEYS['walk'])  # Left-Alt for walk mode
            pydirectinput.keyDown(self.KEYS['forward'])  # W for forward movement
            
            while self.auto_walk_running:
                current_time = time.time()
                
                # Capture game screen for path detection
                frame = detector.capture_game_screen()
                if frame is None:
                    time.sleep(0.1)
                    continue
                
                # Detect path edges and determine correction needed
                if current_time - last_correction_time > correction_cooldown:
                    correction = self._detect_path_edges_and_correct(frame)
                    if correction['action'] != 'forward':
                        print(f"🛤️ Path correction: {correction['reason']} - offset: {correction['offset']:.1f}px")
                        self._execute_path_correction_continuous(correction)
                        last_correction_time = current_time
                        continue  # Skip normal walking this frame
                
                # Brief pause to check if still running
                time.sleep(0.1)
                
        except Exception as e:
            print(f"❌ Path-following loop error: {e}")
        finally:
            # Release all keys when stopping
            print("🛑 Releasing walk mode keys...")
            pydirectinput.keyUp(self.KEYS['walk'])
            pydirectinput.keyUp(self.KEYS['forward'])
            pydirectinput.keyUp(self.KEYS['left'])
            pydirectinput.keyUp(self.KEYS['right'])
    
    def _detect_path_edges_and_correct(self, frame):
        """Detect path edges and determine if correction is needed"""
        try:
            import cv2
            import numpy as np
            
            height, width = frame.shape[:2]
            center_x = width // 2
            
            # Spider-Man body measurements based on game images
            spiderman_body_width = 18  # Estimated torso width in pixels
            spiderman_foot_offset = 12  # Feet position below screen center
            
            # Calculate Spider-Man's actual position
            spiderman_torso_x = center_x  # Torso center at screen center
            spiderman_feet_y = (height // 2) + spiderman_foot_offset  # Feet below center
            spiderman_y = height // 2  # Use torso Y for detection
            
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define ranges for path detection (dark asphalt/concrete)
            # Lower and upper bounds for dark path material
            lower_path = np.array([0, 0, 20])    # Very dark colors
            upper_path = np.array([180, 255, 80]) # Dark to medium gray
            
            # Create mask for path areas
            path_mask = cv2.inRange(hsv, lower_path, upper_path)
            
            # Clean up the mask
            kernel = np.ones((3,3), np.uint8)
            path_mask = cv2.morphologyEx(path_mask, cv2.MORPH_CLOSE, kernel)
            path_mask = cv2.morphologyEx(path_mask, cv2.MORPH_OPEN, kernel)
            
            # Find path edges using Canny edge detection
            edges = cv2.Canny(path_mask, 50, 150)
            
            # Detect left and right path edges at Spider-Man's feet level
            left_edge = self._find_path_edge(edges, spiderman_feet_y, 'left', width, height)
            right_edge = self._find_path_edge(edges, spiderman_feet_y, 'right', width, height)
            
            # Calculate path center and Spider-Man's offset
            if left_edge is not None and right_edge is not None:
                path_center = (left_edge + right_edge) / 2
                offset = spiderman_torso_x - path_center
                
                # Determine correction needed
                if abs(offset) > 30:  # Significant offset from center
                    if offset > 0:
                        return {'action': 'left', 'reason': 'too_far_right', 'offset': offset}
                    else:
                        return {'action': 'right', 'reason': 'too_far_left', 'offset': abs(offset)}
                else:
                    return {'action': 'forward', 'reason': 'centered_on_path', 'offset': abs(offset)}
            else:
                # Fallback: try to detect path using horizontal line scanning at feet level
                return self._detect_path_fallback(frame, spiderman_torso_x, spiderman_feet_y)
            
        except Exception as e:
            print(f"❌ Path detection failed: {e}")
            return {'action': 'forward', 'reason': 'detection_error', 'offset': 0}
    
    def _find_path_edge(self, edges, y_position, direction, width, height):
        """Find path edge at specific y position"""
        try:
            import cv2
            import numpy as np
            
            # Look for edges near Spider-Man's y position (±50 pixels)
            search_range = 50
            y_start = max(0, y_position - search_range)
            y_end = min(height, y_position + search_range)
            
            # Extract horizontal slice
            edge_slice = edges[y_start:y_end, :]
            
            if direction == 'left':
                # Look from center towards left edge
                for x in range(width // 2, 0, -1):
                    if np.any(edge_slice[:, x]):
                        return x
            else:  # right
                # Look from center towards right edge
                for x in range(width // 2, width):
                    if np.any(edge_slice[:, x]):
                        return x
            
            return None
            
        except Exception as e:
            print(f"❌ Edge detection failed: {e}")
            return None
    
    def _detect_path_fallback(self, frame, spiderman_x, spiderman_y):
        """Fallback path detection using horizontal scanning"""
        try:
            import cv2
            import numpy as np
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Scan horizontal line at Spider-Man's position
            scan_line = gray[spiderman_y, :]
            
            # Find dark areas (path) vs light areas (snow/grass)
            dark_threshold = 80
            path_pixels = scan_line < dark_threshold
            
            # Find left and right boundaries of path
            path_indices = np.where(path_pixels)[0]
            
            if len(path_indices) > 50:  # Minimum path width
                left_boundary = path_indices[0]
                right_boundary = path_indices[-1]
                path_center = (left_boundary + right_boundary) / 2
                
                offset = spiderman_x - path_center
                
                if abs(offset) > 30:
                    if offset > 0:
                        return {'action': 'left', 'reason': 'fallback_too_far_right', 'offset': offset}
                    else:
                        return {'action': 'right', 'reason': 'fallback_too_far_left', 'offset': abs(offset)}
            
            return {'action': 'forward', 'reason': 'fallback_centered', 'offset': 0}
            
        except Exception as e:
            print(f"❌ Fallback detection failed: {e}")
            return {'action': 'forward', 'reason': 'fallback_error', 'offset': 0}
    
    def _execute_path_correction(self, correction):
        """Execute path correction maneuver"""
        action = correction['action']
        reason = correction['reason']
        offset = correction['offset']
        
        print(f"   🛤️ {action} correction - {reason}")
        
        # Determine correction strength based on offset
        if offset > 60:
            correction_duration = 0.4  # Strong correction
        elif offset > 40:
            correction_duration = 0.3  # Medium correction
        else:
            correction_duration = 0.2  # Light correction
        
        if action == 'left':
            # Move left to get back on path
            pydirectinput.keyDown(self.KEYS['left'])
            time.sleep(correction_duration)
            pydirectinput.keyUp(self.KEYS['left'])
        elif action == 'right':
            # Move right to get back on path
            pydirectinput.keyDown(self.KEYS['right'])
            time.sleep(correction_duration)
            pydirectinput.keyUp(self.KEYS['right'])
        
        # Brief forward motion after correction
        pydirectinput.keyDown(self.KEYS['forward'])
        time.sleep(0.1)
        pydirectinput.keyUp(self.KEYS['forward'])
    
    def _execute_path_correction_continuous(self, correction):
        """Execute path correction while maintaining walk mode (Left-Alt + W)"""
        action = correction['action']
        reason = correction['reason']
        offset = correction['offset']
        
        print(f"   🛤️ {action} correction - {reason} (maintaining walk mode)")
        
        # Determine correction strength based on offset
        if offset > 60:
            correction_duration = 0.4  # Strong correction
        elif offset > 40:
            correction_duration = 0.3  # Medium correction
        else:
            correction_duration = 0.2  # Light correction
        
        # Execute steering while maintaining Left-Alt + W
        if action == 'left':
            # Add left steering while keeping walk mode active
            pydirectinput.keyDown(self.KEYS['left'])
            time.sleep(correction_duration)
            pydirectinput.keyUp(self.KEYS['left'])
            print(f"   ↖️ Left steering for {correction_duration:.1f}s")
        elif action == 'right':
            # Add right steering while keeping walk mode active
            pydirectinput.keyDown(self.KEYS['right'])
            time.sleep(correction_duration)
            pydirectinput.keyUp(self.KEYS['right'])
            print(f"   ↗️ Right steering for {correction_duration:.1f}s")
        
        # Note: Left-Alt and W remain held throughout the entire process
    
    def _start_keyboard_listener(self):
        """Start keyboard listener for End key"""
        try:
            from pynput import keyboard
            
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press
            )
            self.keyboard_listener.start()
            
        except Exception as e:
            print(f"❌ Keyboard listener start error: {e}")
    
    def _stop_keyboard_listener(self):
        """Stop keyboard listener"""
        try:
            if hasattr(self, 'keyboard_listener') and self.keyboard_listener:
                self.keyboard_listener.stop()
                self.keyboard_listener = None
        except Exception as e:
            print(f"❌ Keyboard listener stop error: {e}")
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            from pynput.keyboard import Key
            
            if key == Key.end:
                print("\n🛑 End key pressed - stopping system...")
                self.auto_walk_running = False
                return False  # Stop the listener
            elif key == Key.esc:
                print("\n🛑 Escape key pressed - stopping system...")
                self.auto_walk_running = False
                return False  # Stop the listener
        except Exception as e:
            print(f"⚠️ Error handling key press: {e}")
        
        return True  # Continue listening

def get_spiderman_scenario_scripts_commands(gamepad):
    """Get scenario script command mappings for Spider-Man"""
    spiderman = SpiderManScenarioScripts(None)  # No gamepad needed for keyboard
    
    return {
        # Movement & Navigation Scenarios
        "super jump": lambda: spiderman.super_jump(),
        "web swing combo": lambda: spiderman.web_swing_combo(),
        
        # Auto-Walking Scenarios
        "auto walk": lambda: spiderman._start_auto_walk(),
        "stop auto walk": lambda: spiderman._stop_auto_walk(),
        
        # Path-Following Scenarios
        "path follow": lambda: spiderman._start_path_following(),
        "stop path follow": lambda: spiderman._stop_auto_walk(),  # Uses same stop method
        
        # AI-Powered Scenarios
        "auto swing": lambda: spiderman._start_auto_swing(),
        "stop auto swing": lambda: spiderman._stop_auto_swing(),
    }
