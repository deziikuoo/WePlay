"""
Old School RuneScape Base Controls
Handles virtual mouse input and keyboard controls for OSRS
"""

import pydirectinput
import win32gui
import win32con
import win32api
import pyautogui
import time
import random
import sys
import os
from typing import Tuple, Optional

# Add Windows Management to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'B', 'Windows Managment', 'Window_Management_Controls'))
from Windows_Management_Controls import GameWindowManager


class RuneScapeBaseControls:
    """Base class for RuneScape virtual mouse and keyboard controls"""
    
    def __init__(self):
        # Initialize centralized window manager
        self.window_manager = GameWindowManager()
        
        # OSRS specific key mappings (only the keys OSRS actually uses)
        self.KEYS = {
            # Function keys for interface switching
            'f1': 'f1',   # Combat tab
            'f2': 'f2',   # Skills tab
            'f3': 'f3',   # Quests/Achievement Diary tab
            'f4': 'f4',   # Worn Equipment tab
            'f5': 'f5',   # Prayers tab
            'f6': 'f6',   # Spell book tab
            'f7': 'f7',   # Clan Chat tab
            'f8': 'f8',   # Friends List tab
            'f9': 'f9',   # Account Management tab
            'f10': 'f10', # Settings tab
            'f11': 'f11', # Emotes tab
            'f12': 'f12', # Music tab
            
            # Special keys
            'escape': 'escape',  # Switch to Inventory tab / Close interface
            'tab': 'tab',        # Reply to last private message
            'space': 'space',    # Make-X default settings / Continue dialogue
            
            # Dialogue response keys
            '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
            
            # World map shortcut
            'ctrl_m': 'ctrl+m',  # Open World Map
        }
        
        # Mouse buttons
        self.MOUSE_BUTTONS = {
            'left': 0x0001,    # MOUSEEVENTF_LEFTDOWN/UP
            'right': 0x0002,   # MOUSEEVENTF_RIGHTDOWN/UP
            'middle': 0x0004   # MOUSEEVENTF_MIDDLEDOWN/UP
        }
        
        # Get game window from centralized manager
        self.game_window = self.window_manager.get_game_window_handle()
        self.game_window_title = self.window_manager.get_game_title()
        
    def find_game_window(self) -> bool:
        """Find the RuneScape game window using centralized manager"""
        try:
            success = self.window_manager.refresh_game_detection()
            if success:
                self.game_window = self.window_manager.get_game_window_handle()
                self.game_window_title = self.window_manager.get_game_title()
                print(f"✅ Found RuneScape window: {self.game_window_title}")
                return True
            else:
                print("❌ RuneScape window not found")
                return False
                
        except Exception as e:
            print(f"❌ Error finding RuneScape window: {e}")
            return False
    
    def focus_game(self) -> bool:
        """Focus the RuneScape game window using centralized manager"""
        try:
            success = self.window_manager.focus_game()
            if success:
                # Update local references
                self.game_window = self.window_manager.get_game_window_handle()
                self.game_window_title = self.window_manager.get_game_title()
                print(f"✅ RuneScape window focused: {self.game_window_title}")
                return True
            else:
                print(f"❌ Failed to focus RuneScape window")
                return False
                
        except Exception as e:
            print(f"❌ Error focusing RuneScape window: {e}")
            return False
    
    def get_window_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """Get the game window rectangle coordinates"""
        try:
            if self.game_window:
                return win32gui.GetWindowRect(self.game_window)
            return None
        except Exception as e:
            print(f"❌ Error getting window rect: {e}")
            return None
    
    def screen_to_game_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert screen coordinates to game coordinates"""
        try:
            rect = self.get_window_rect()
            if rect:
                # Adjust for window borders and title bar
                game_x = screen_x - rect[0] + 8  # Account for window border
                game_y = screen_y - rect[1] + 31  # Account for title bar
                return game_x, game_y
            return screen_x, screen_y
        except Exception as e:
            print(f"❌ Error converting coordinates: {e}")
            return screen_x, screen_y
    
    def click_at_position(self, x: int, y: int, button: str = 'left', human_like: bool = True) -> bool:
        """Click at specific screen coordinates"""
        try:
            print(f"🔍 DEBUG: click_at_position called with ({x}, {y}), human_like={human_like}")
            
            if not self.focus_game():
                print("❌ Failed to focus game window in click_at_position")
                return False
            
            # Add human-like movement and timing
            if human_like:
                # Small random offset for human-like clicking
                x += random.randint(-2, 2)
                y += random.randint(-2, 2)
                
                # Move cursor gradually
                current_pos = win32gui.GetCursorPos()
                steps = random.randint(3, 7)
                
                for i in range(steps):
                    step_x = current_pos[0] + (x - current_pos[0]) * (i + 1) / steps
                    step_y = current_pos[1] + (y - current_pos[1]) * (i + 1) / steps
                    win32api.SetCursorPos((int(step_x), int(step_y)))
                    time.sleep(random.uniform(0.01, 0.03))
                
                # Set final cursor position with delay
                win32api.SetCursorPos((x, y))
                time.sleep(random.uniform(0.05, 0.15))
            else:
                # Fast clicking using PyAutoGUI - more reliable for game clicking
                x += random.randint(-1, 1)
                y += random.randint(-1, 1)
                
                # Use PyAutoGUI for more reliable clicking
                pyautogui.moveTo(x, y, duration=0.1)  # Move cursor to position
                time.sleep(0.1)  # Brief pause
                pyautogui.click(x, y, button=button)  # Click at position
                
                click_type = "⚡ Fast" if not human_like else "🖱️"
                print(f"{click_type} Clicked at ({x}, {y}) with {button} button")
                
                # Small delay after click to prevent rapid-fire issues
                time.sleep(0.1)
                return True
            
        except Exception as e:
            print(f"❌ Error clicking at position: {e}")
            return False
    
    def click_object_at_coords(self, x: int, y: int, object_type: str = "unknown") -> bool:
        """Click on a detected object at specified coordinates"""
        try:
            # Debug: Print coordinates and verify they're within screen bounds
            print(f"🔍 DEBUG: Attempting to click {object_type} at screen coordinates ({x}, {y})")
            
            # Check if coordinates are within reasonable screen bounds
            if x < 0 or x > 1920 or y < 0 or y > 1080:
                print(f"⚠️ WARNING: Coordinates ({x}, {y}) seem outside normal screen bounds!")
            
            # Ensure game window is focused before clicking
            if not self.focus_game():
                print("❌ Failed to focus game window")
                return False
            
            # Use fast click for combat objects (chickens, NPCs)
            if object_type.lower() in ['chicken', 'goblin', 'cow', 'person', 'npc']:
                success = self.click_at_position(x, y, 'left', human_like=False)
            else:
                success = self.click_at_position(x, y, 'left', human_like=True)
            
            if success:
                print(f"🎯 Clicked on {object_type} at ({x}, {y})")
            return success
        except Exception as e:
            print(f"❌ Error clicking object: {e}")
            return False
    
    def fast_click_at_position(self, x: int, y: int, button: str = 'left') -> bool:
        """Fast click at specific screen coordinates (optimized for combat)"""
        try:
            if not self.focus_game():
                return False
            
            # Minimal random offset to avoid bot detection
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            
            # Direct cursor positioning (no gradual movement)
            win32api.SetCursorPos((x, y))
            
            # Minimal delay before click
            time.sleep(0.01)
            
            # Perform click with direct API calls
            button_code = self.MOUSE_BUTTONS.get(button, self.MOUSE_BUTTONS['left'])
            win32api.mouse_event(button_code, x, y, 0, 0)
            time.sleep(0.005)  # Very short delay
            win32api.mouse_event(button_code << 1, x, y, 0, 0)  # Release
            
            print(f"⚡ Fast clicked at ({x}, {y})")
            return True
            
        except Exception as e:
            print(f"❌ Error in fast click: {e}")
            return False
    
    def press_key(self, key: str, duration: float = 0.1) -> bool:
        """Press and hold a key for specified duration"""
        try:
            if not self.focus_game():
                return False
            
            key_name = self.KEYS.get(key.lower(), key)
            pydirectinput.keyDown(key_name)
            time.sleep(duration)
            pydirectinput.keyUp(key_name)
            
            print(f"⌨️ Pressed key: {key_name} for {duration:.1f}s")
            return True
            
        except Exception as e:
            print(f"❌ Error pressing key: {e}")
            return False
    
    def type_text(self, text: str, delay: float = 0.1) -> bool:
        """Type text with human-like delays"""
        try:
            if not self.focus_game():
                return False
            
            for char in text:
                pydirectinput.write(char)
                time.sleep(random.uniform(0.05, delay))
            
            print(f"⌨️ Typed: {text}")
            return True
            
        except Exception as e:
            print(f"❌ Error typing text: {e}")
            return False
