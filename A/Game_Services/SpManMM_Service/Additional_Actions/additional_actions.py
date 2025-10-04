#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Additional Actions
This module provides additional action controls for Spider-Man: Miles Morales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls

class SpiderManAdditionalActions(SpiderManKeyboardControls):
    """Spider-Man additional action controls"""
    
    def __init__(self, gamepad=None):
        super().__init__()
        self.gamepad = gamepad  # Keep gamepad for backward compatibility
    
    # === ADDITIONAL ACTIONS ===
    
    def scan_environment(self):
        """Scan Environment: Tab key"""
        self._press_key(self.KEYS['map'])
        print("Scanning environment")
    
    def web_yank(self, duration=1.0):
        """Web-Yank: Hold Q (Yank and Throw Environment)"""
        self._hold_key(self.KEYS['yank_throw'], duration)
        print(f"Web-Yank ({duration:.1f}s)")
    
    def trick_mode(self):
        """Trick Mode (Air Tricks): T (when airborne)"""
        self._press_key(self.KEYS['air_trick'])
        print("Trick Mode (Air Tricks)")
    
    def stop(self):
        """Stop all movement and actions"""
        # For keyboard, we can't really "stop" all keys, but we can print a message
        print("Stopped all actions")

def get_spiderman_additional_actions_commands(gamepad):
    """Get additional action command mappings for Spider-Man"""
    spiderman = SpiderManAdditionalActions(None)  # No gamepad needed for keyboard
    
    return {
        "scan environment": lambda: spiderman.scan_environment(),
        "web yank": lambda: spiderman.web_yank(),
        "trick mode": lambda: spiderman.trick_mode(),
        "stop": lambda: spiderman.stop(),
    }
