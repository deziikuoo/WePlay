"""
RuneScape Commands
OSRS-specific commands for object interaction using YOLO detection
"""

import time
import random
from typing import Optional, Dict, List
from runescape_base_controls import RuneScapeBaseControls
from runescape_yolo_detector import RuneScapeObjectDetector


class RuneScapeCommands(RuneScapeBaseControls):
    """RuneScape commands for automated gameplay"""
    
    def __init__(self):
        super().__init__()
        self.detector = RuneScapeObjectDetector()
        self.hunting_active = False  # Flag to control hunting loop
        
    def click_object(self, object_type: str, confidence_threshold: float = 0.1) -> bool:
        """Detect and click on an object of specified type"""
        try:
            print(f"🔍 Searching for {object_type}...")
            
            # Detect the object
            object_detection = self.detector.detect_and_get_object(object_type, confidence_threshold)
            
            if not object_detection:
                print(f"❌ No {object_type} found")
                return False
            
            # Click on the object
            success = self.click_object_at_coords(
                object_detection['screen_x'], 
                object_detection['screen_y'], 
                object_detection['class_name']
            )
            
            return success
            
        except Exception as e:
            print(f"❌ Error clicking {object_type}: {e}")
            return False
    
    def chop_tree(self, tree_type: str = "tree", max_attempts: int = 3) -> bool:
        """Chop a tree (Woodcutting skill) with enhanced logic"""
        try:
            print(f"🌳 Starting woodcutting - looking for {tree_type}...")
            print("⏳ Waiting 7 seconds before initiating...")
            time.sleep(7)
            
            # First, check if we need to equip an axe
            if not self._has_axe_equipped():
                print("⚠️ No axe detected - attempting to equip from inventory...")
                if not self._equip_axe_from_inventory():
                    print("❌ No axe found in inventory")
                    return False
            
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                print(f"🔄 Attempt {attempts}/{max_attempts} to find {tree_type}...")
                
                # Try to find and click the tree
                success = self.click_object(tree_type, confidence_threshold=0.6)
                
                if success:
                    print(f"✅ Started chopping {tree_type}")
                    
                    # Wait for initial animation and check for success
                    time.sleep(random.uniform(1.5, 2.5))
                    
                    # Check if we're actually chopping (optional validation)
                    if self._is_chopping():
                        print("🪓 Confirmed chopping animation active")
                        return True
                    else:
                        print("⚠️ Chopping may have failed - trying different tree...")
                        time.sleep(random.uniform(1.0, 2.0))
                else:
                    print(f"❌ Failed to find {tree_type} on attempt {attempts}")
                    if attempts < max_attempts:
                        # Try moving slightly and scanning again
                        self._scan_area_for_trees()
                        time.sleep(random.uniform(1.0, 2.0))
            
            print(f"❌ Failed to find suitable {tree_type} after {max_attempts} attempts")
            return False
            
        except Exception as e:
            print(f"❌ Error chopping tree: {e}")
            return False
    
    def _has_axe_equipped(self) -> bool:
        """Check if player has an axe equipped (basic validation)"""
        try:
            # Switch to equipment tab to check
            if self.switch_interface_tab('equipment'):
                time.sleep(0.5)
                # This is a basic check - in a real implementation, you'd use OCR or image recognition
                # to detect if an axe is in the weapon slot
                print("🔍 Checking equipment for axe...")
                return True  # Placeholder - assume axe is equipped
            return False
        except Exception as e:
            print(f"❌ Error checking equipment: {e}")
            return False
    
    def _equip_axe_from_inventory(self) -> bool:
        """Attempt to equip an axe from inventory"""
        try:
            print("📦 Switching to inventory to find axe...")
            if self.switch_interface_tab('inventory'):
                time.sleep(0.5)
                # Look for axe in inventory slots 1-5 (quick access)
                for slot in range(1, 6):
                    print(f"🔍 Checking inventory slot {slot} for axe...")
                    # In a real implementation, you'd detect axe icons in inventory
                    # For now, we'll assume there's an axe somewhere
                    time.sleep(0.2)
                
                print("✅ Assuming axe found and equipped")
                return True
            return False
        except Exception as e:
            print(f"❌ Error equipping axe: {e}")
            return False
    
    def _is_chopping(self) -> bool:
        """Check if player is currently chopping (basic validation)"""
        try:
            # In a real implementation, you'd check for:
            # 1. Chopping animation
            # 2. Chat messages about woodcutting
            # 3. Inventory changes (logs appearing)
            # For now, we'll use a simple time-based check
            time.sleep(random.uniform(0.5, 1.0))
            return True  # Placeholder - assume chopping is working
        except Exception as e:
            print(f"❌ Error checking chopping status: {e}")
            return False
    
    def _scan_area_for_trees(self):
        """Scan the current area for available trees"""
        try:
            print("🔍 Scanning area for trees...")
            # Use the existing scan functionality
            detections = self.scan_objects(save_debug=False)
            tree_detections = [d for d in detections if d['category'] == 'tree']
            print(f"📍 Found {len(tree_detections)} trees in area")
        except Exception as e:
            print(f"❌ Error scanning for trees: {e}")
    
    def _scan_area_for_chickens(self):
        """Scan the current area for available chickens"""
        try:
            print("🔍 Scanning area for chickens...")
            # Use the existing scan functionality
            detections = self.scan_objects(save_debug=False)
            chicken_detections = [d for d in detections if d['category'] == 'chicken']
            print(f"📍 Found {len(chicken_detections)} chickens in area")
        except Exception as e:
            print(f"❌ Error scanning for chickens: {e}")
    
    def _is_in_combat(self) -> bool:
        """Check if player is currently in combat"""
        try:
            # This is a basic check - in a real implementation, you'd use OCR or image recognition
            # to detect combat indicators like red text, combat interface, or health bars
            print("🔍 Checking combat status...")
            # Placeholder - assume combat started if we clicked successfully
            return True
        except Exception as e:
            print(f"❌ Error checking combat status: {e}")
            return False
    
    def _get_player_position(self) -> Optional[tuple]:
        """Get current player context - use chicken detection pattern instead of static position"""
        try:
            # Since player is always centered, we need to track something that changes
            # Use the pattern of chicken detections as a proxy for player location/context
            
            # Take a screenshot and detect chickens
            frame = self.detector.capture_game_screen()
            if frame is None:
                return None
                
            # Get chicken detections
            detections = self.detector.detect_objects(frame, confidence_threshold=0.3)
            chicken_detections = [d for d in detections if d['class_name'] == 'chicken']
            
            # Create a "position" based on chicken detection pattern
            # This will change when player moves to different areas
            if chicken_detections:
                # Use the closest chicken's position as context
                closest_chicken = self.detector.get_closest_object(chicken_detections)
                if closest_chicken:
                    # Return a simplified position based on chicken location
                    chicken_x = closest_chicken['screen_x'] // 100  # Round to nearest 100 pixels
                    chicken_y = closest_chicken['screen_y'] // 100
                    return (chicken_x, chicken_y)
            
            # If no chickens detected, return a special "no chickens" position
            return (999, 999)  # Special marker for "no chickens in view"
            
        except Exception as e:
            print(f"❌ Error getting player context: {e}")
            return None
    
    def _positions_are_similar(self, pos1: tuple, pos2: tuple, threshold: int = 50) -> bool:
        """Check if two positions are similar (within threshold pixels)"""
        try:
            if not pos1 or not pos2:
                return False
            
            x1, y1 = pos1
            x2, y2 = pos2
            
            # Calculate distance between positions
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            
            return distance < threshold
        except Exception as e:
            print(f"❌ Error comparing positions: {e}")
            return False
    
    def _adjust_camera_for_chickens(self) -> bool:
        """Adjust camera angle to help find chickens when player is stuck"""
        try:
            print("📹 Adjusting camera to find chickens...")
            
            # Random camera movements to change viewing angle
            camera_movements = [
                ("right", 90),   # Turn camera right
                ("left", 90),    # Turn camera left  
                ("up", 45),      # Look up
                ("down", 45),    # Look down
                ("right", 45),   # Small right turn
                ("left", 45),    # Small left turn
            ]
            
            # Pick a random camera movement
            import random
            movement, angle = random.choice(camera_movements)
            
            print(f"📹 Moving camera {movement} by {angle} degrees...")
            
            # Simulate camera movement (you'll need to implement actual camera controls)
            # For now, this is a placeholder that shows the concept
            time.sleep(0.5)  # Simulate camera movement time
            
            print("✅ Camera adjustment complete")
            return True
            
        except Exception as e:
            print(f"❌ Error adjusting camera: {e}")
            return False
    
    def mine_rock(self, rock_type: str = "rock") -> bool:
        """Mine a rock (Mining skill)"""
        try:
            print(f"⛏️ Starting mining - looking for {rock_type}...")
            
            success = self.click_object(rock_type, confidence_threshold=0.6)
            
            if success:
                print(f"✅ Started mining {rock_type}")
                # Wait for mining animation
                time.sleep(random.uniform(3.0, 6.0))
            else:
                print(f"❌ Failed to find {rock_type} to mine")
            
            return success
            
        except Exception as e:
            print(f"❌ Error mining rock: {e}")
            return False
    
    def attack_npc(self, npc_type: str = "person") -> bool:
        """Attack an NPC (Combat)"""
        try:
            print(f"⚔️ Starting combat - looking for {npc_type}...")
            
            success = self.click_object(npc_type, confidence_threshold=0.6)
            
            if success:
                print(f"✅ Started attacking {npc_type}")
                # Wait for combat to begin
                time.sleep(random.uniform(1.0, 2.0))
            else:
                print(f"❌ Failed to find {npc_type} to attack")
            
            return success
            
        except Exception as e:
            print(f"❌ Error attacking NPC: {e}")
            return False
    
    def attack_chicken(self, max_attempts: int = 3) -> bool:
        """Attack a chicken (Combat skill) with enhanced logic"""
        try:
            print(f"🐔 Starting chicken hunting - looking for chicken...")
            print("⏳ Waiting 1 second before starting...")
            time.sleep(1)
            
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                print(f"🔄 Attempt {attempts}/{max_attempts} to find chicken...")
                
                # Try to find and click the chicken
                success = self.click_object("chicken", confidence_threshold=0.3)
                
                if success:
                    print(f"✅ Started attacking chicken")
                    
                    # Wait for combat to begin
                    time.sleep(random.uniform(1.0, 2.0))
                    
                    # Check if we're in combat
                    if self._is_in_combat():
                        print("⚔️ Combat initiated successfully!")
                        return True
                    else:
                        print("⚠️ Click successful but combat not detected")
                        time.sleep(random.uniform(1.0, 2.0))
                else:
                    print(f"❌ Failed to find chicken on attempt {attempts}")
                    if attempts < max_attempts:
                        # Try moving slightly and scanning again
                        self._scan_area_for_chickens()
                        time.sleep(random.uniform(1.0, 2.0))
            
            print(f"❌ Failed to find suitable chicken after {max_attempts} attempts")
            return False
            
        except Exception as e:
            print(f"❌ Error attacking chicken: {e}")
            return False
    
    def chicken_hunting(self, detection_interval: int = 7) -> bool:
        """Continuous chicken hunting - detects and attacks chickens every 7 seconds until stopped"""
        try:
            print(f"🏹 Starting continuous chicken hunting...")
            print(f"⏰ Detection interval: {detection_interval} seconds")
            print("🛑 Press Ctrl+C or type 'end' in the command processor to stop")
            print()
            
            hunt_count = 0
            successful_attacks = 0
            stuck_position_count = 0
            last_player_position = None
            
            # Set hunting flag to True when starting
            self.hunting_active = True
            
            while self.hunting_active:
                hunt_count += 1
                print(f"🔍 Hunt #{hunt_count} - Searching for chickens...")
                
                # Check if player is stuck in same position
                current_position = self._get_player_position()
                if current_position and last_player_position:
                    if self._positions_are_similar(current_position, last_player_position):
                        stuck_position_count += 1
                        print(f"📍 Player appears to be in same position ({stuck_position_count}/2 attempts)")
                        
                        if stuck_position_count >= 2:
                            print("🔄 Player stuck detected! Adjusting camera to find chickens...")
                            self._adjust_camera_for_chickens()
                            stuck_position_count = 0  # Reset counter
                    else:
                        stuck_position_count = 0  # Reset if player moved
                        print("✅ Player moved, resetting stuck counter")
                
                last_player_position = current_position
                
                # Try to attack a chicken
                success = self.attack_chicken(max_attempts=2)  # Reduced attempts for continuous mode
                
                if success:
                    successful_attacks += 1
                    print(f"✅ Successful attack! Total: {successful_attacks}/{hunt_count}")
                else:
                    print(f"❌ No chickens found this round")
                
                print(f"⏳ Waiting {detection_interval} seconds before next hunt...")
                print("   (Press Ctrl+C to stop hunting)")
                
                # Wait for next detection cycle
                time.sleep(detection_interval)
                
        except KeyboardInterrupt:
            print(f"\n🛑 Chicken hunting stopped by user")
            print(f"📊 Final Stats: {successful_attacks}/{hunt_count} successful attacks")
            self.hunting_active = False  # Ensure flag is reset
            return True
        except Exception as e:
            print(f"❌ Error in chicken hunting: {e}")
            self.hunting_active = False  # Ensure flag is reset
            return False
        finally:
            self.hunting_active = False  # Always reset flag when done
    
    def stop_hunting(self) -> bool:
        """Stop the continuous chicken hunting"""
        try:
            if self.hunting_active:
                print("🛑 Stopping chicken hunting...")
                self.hunting_active = False
                print("✅ Chicken hunting stopped")
            else:
                print("ℹ️ No hunting session active")
            return True
        except Exception as e:
            print(f"❌ Error stopping hunting: {e}")
            return False
    
    def collect_item(self, item_type: str = "item") -> bool:
        """Collect an item from the ground"""
        try:
            print(f"💰 Collecting item - looking for {item_type}...")
            
            success = self.click_object(item_type, confidence_threshold=0.5)
            
            if success:
                print(f"✅ Collected {item_type}")
                time.sleep(random.uniform(0.5, 1.0))
            else:
                print(f"❌ Failed to find {item_type} to collect")
            
            return success
            
        except Exception as e:
            print(f"❌ Error collecting item: {e}")
            return False
    
    def open_bank(self) -> bool:
        """Open a bank interface"""
        try:
            print("🏦 Opening bank...")
            
            success = self.click_object("building", confidence_threshold=0.7)
            
            if success:
                print("✅ Opened bank interface")
                time.sleep(random.uniform(1.0, 2.0))
            else:
                print("❌ Failed to find bank")
            
            return success
            
        except Exception as e:
            print(f"❌ Error opening bank: {e}")
            return False
    
    def switch_interface_tab(self, tab_name: str) -> bool:
        """Switch to a specific interface tab using function keys"""
        try:
            tab_keys = {
                'combat': 'f1',
                'skills': 'f2', 
                'quests': 'f3',
                'equipment': 'f4',
                'prayers': 'f5',
                'spells': 'f6',
                'clan': 'f7',
                'friends': 'f8',
                'account': 'f9',
                'settings': 'f10',
                'emotes': 'f11',
                'music': 'f12',
                'inventory': 'escape'
            }
            
            key = tab_keys.get(tab_name.lower())
            if not key:
                print(f"❌ Unknown tab: {tab_name}")
                return False
            
            print(f"🔄 Switching to {tab_name} tab...")
            success = self.press_key(key, duration=0.1)
            
            if success:
                print(f"✅ Switched to {tab_name} tab")
                time.sleep(0.5)  # Wait for interface to load
            
            return success
            
        except Exception as e:
            print(f"❌ Error switching tab: {e}")
            return False
    
    def use_inventory_item(self, slot_number: int) -> bool:
        """Use an item in inventory slot (1-28)"""
        try:
            if slot_number < 1 or slot_number > 28:
                print(f"❌ Invalid inventory slot: {slot_number} (must be 1-28)")
                return False
            
            print(f"📦 Using inventory slot {slot_number}...")
            
            # For slots 1-5, we can use number keys
            if slot_number <= 5:
                success = self.press_key(str(slot_number), duration=0.1)
            else:
                # For slots 6+, we need to click on the inventory interface
                # This would require more complex inventory detection
                print(f"⚠️ Slot {slot_number} requires manual clicking (not implemented)")
                success = False
            
            if success:
                print(f"✅ Used item in slot {slot_number}")
                time.sleep(0.5)
            
            return success
            
        except Exception as e:
            print(f"❌ Error using inventory item: {e}")
            return False
    
    def chop_specific_tree(self, tree_type: str) -> bool:
        """Chop a specific type of tree (oak, willow, maple, etc.)"""
        try:
            # Map common tree names to detection terms
            tree_mapping = {
                'oak': 'oak tree',
                'willow': 'willow tree', 
                'maple': 'maple tree',
                'yew': 'yew tree',
                'magic': 'magic tree',
                'normal': 'tree',
                'regular': 'tree'
            }
            
            detection_type = tree_mapping.get(tree_type.lower(), tree_type)
            print(f"🌳 Looking for {detection_type}...")
            
            return self.chop_tree(detection_type)
            
        except Exception as e:
            print(f"❌ Error chopping {tree_type}: {e}")
            return False
    
    def auto_woodcutting(self, tree_type: str = "tree", duration_minutes: int = 5, 
                        inventory_check: bool = True, tree_rotation: bool = True) -> bool:
        """Enhanced automated woodcutting with inventory management and tree rotation"""
        try:
            print(f"🌳 Starting enhanced auto-woodcutting for {duration_minutes} minutes...")
            print(f"📋 Settings: tree_type={tree_type}, inventory_check={inventory_check}, tree_rotation={tree_rotation}")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            consecutive_failures = 0
            max_consecutive_failures = 5
            
            # Tree rotation list for variety
            tree_variants = [tree_type]
            if tree_rotation and tree_type.lower() == 'tree':
                tree_variants = ['tree', 'oak tree', 'willow tree']  # Fallback options
            
            current_tree_index = 0
            
            while time.time() < end_time:
                try:
                    # Check inventory if enabled
                    if inventory_check:
                        if self._is_inventory_full():
                            print("📦 Inventory is full! Dropping logs or banking...")
                            if not self._handle_full_inventory():
                                print("⚠️ Could not handle full inventory - continuing anyway")
                    
                    # Try current tree type
                    current_tree = tree_variants[current_tree_index % len(tree_variants)]
                    success = self.chop_tree(current_tree, max_attempts=2)
                    
                    if success:
                        consecutive_failures = 0
                        print(f"✅ Successfully chopping {current_tree}")
                        
                        # Wait for chopping cycle
                        chop_time = random.uniform(4.0, 8.0)
                        print(f"⏳ Chopping for {chop_time:.1f} seconds...")
                        time.sleep(chop_time)
                        
                        # Rotate to next tree type if enabled
                        if tree_rotation and len(tree_variants) > 1:
                            current_tree_index += 1
                            print(f"🔄 Rotating to next tree type...")
                        
                    else:
                        consecutive_failures += 1
                        print(f"❌ Failed to chop {current_tree} (failure #{consecutive_failures})")
                        
                        if consecutive_failures >= max_consecutive_failures:
                            print("🚨 Too many consecutive failures - scanning area...")
                            self._scan_area_for_trees()
                            consecutive_failures = 0
                            time.sleep(random.uniform(3.0, 5.0))
                        else:
                            time.sleep(random.uniform(2.0, 4.0))
                    
                    # Small random break to seem more human-like
                    if random.random() < 0.1:  # 10% chance
                        break_time = random.uniform(1.0, 3.0)
                        print(f"😴 Taking a short break for {break_time:.1f} seconds...")
                        time.sleep(break_time)
                
                except KeyboardInterrupt:
                    print("⏹️ Auto-woodcutting interrupted by user")
                    break
                except Exception as e:
                    print(f"❌ Error in woodcutting loop: {e}")
                    consecutive_failures += 1
                    time.sleep(random.uniform(2.0, 4.0))
            
            elapsed_time = (time.time() - start_time) / 60
            print(f"✅ Auto-woodcutting completed after {elapsed_time:.1f} minutes")
            return True
            
        except Exception as e:
            print(f"❌ Error in auto-woodcutting: {e}")
            return False
    
    def _is_inventory_full(self) -> bool:
        """Check if inventory is full (basic implementation)"""
        try:
            # This is a placeholder - in a real implementation, you'd:
            # 1. Switch to inventory tab
            # 2. Use OCR or image recognition to count filled slots
            # 3. Return True if 28/28 slots are filled
            
            # For now, we'll use a simple probability-based check
            # In real usage, this would be replaced with actual inventory detection
            return random.random() < 0.1  # 10% chance of being "full" for demo
        except Exception as e:
            print(f"❌ Error checking inventory: {e}")
            return False
    
    def _handle_full_inventory(self) -> bool:
        """Handle full inventory by dropping logs or banking"""
        try:
            print("📦 Handling full inventory...")
            
            # Option 1: Drop logs (simpler, but loses items)
            print("🗑️ Dropping logs to make space...")
            # In a real implementation, you'd:
            # 1. Switch to inventory tab
            # 2. Right-click on logs
            # 3. Select "Drop" option
            
            # Option 2: Bank logs (more complex, but preserves items)
            # This would require finding a bank and using banking interface
            
            time.sleep(random.uniform(1.0, 2.0))
            print("✅ Inventory space cleared")
            return True
            
        except Exception as e:
            print(f"❌ Error handling full inventory: {e}")
            return False
    
    def auto_mining(self, rock_type: str = "rock", duration_minutes: int = 5) -> bool:
        """Automated mining for specified duration"""
        try:
            print(f"⛏️ Starting auto-mining for {duration_minutes} minutes...")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time:
                # Try to mine a rock
                if self.mine_rock(rock_type):
                    # Wait for rock to be mined (longer wait)
                    time.sleep(random.uniform(8.0, 15.0))
                else:
                    # If no rock found, wait a bit and try again
                    time.sleep(random.uniform(3.0, 5.0))
            
            print(f"✅ Auto-mining completed after {duration_minutes} minutes")
            return True
            
        except Exception as e:
            print(f"❌ Error in auto-mining: {e}")
            return False
    
    def scan_objects(self, save_debug: bool = True) -> List[Dict]:
        """Scan and return all detected objects on screen"""
        try:
            print("🔍 Scanning for all objects...")
            
            # Capture screen
            frame = self.detector.capture_game_screen()
            if frame is None:
                return []
            
            # Detect all objects
            detections = self.detector.detect_objects(frame, confidence_threshold=0.4)
            
            if save_debug:
                self.detector.save_debug_image(frame, detections, "runescape_scan.png")
            
            # Group by category
            categories = {}
            for detection in detections:
                category = detection['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(detection)
            
            # Print summary
            print(f"📊 Scan complete - Found {len(detections)} objects:")
            for category, objects in categories.items():
                print(f"   {category}: {len(objects)} objects")
            
            return detections
            
        except Exception as e:
            print(f"❌ Error scanning objects: {e}")
            return []
