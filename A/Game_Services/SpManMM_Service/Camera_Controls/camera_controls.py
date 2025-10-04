#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Camera Controls
This module provides camera controls for Spider-Man: Miles Morales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls

class SpiderManCamera(SpiderManKeyboardControls):
    """Spider-Man camera controls"""
    
    def __init__(self, gamepad=None):
        super().__init__()
        self.gamepad = gamepad  # Keep gamepad for backward compatibility
    
    # === CAMERA CONTROL ===
    
    def look_left(self, duration=0.5):
        """Look left with keyboard"""
        self._hold_key(self.KEYS['camera_left'], duration)
        print("Looking left")
    
    def look_right(self, duration=0.5):
        """Look right with keyboard"""
        self._hold_key(self.KEYS['camera_right'], duration)
        print("Looking right")
    
    def look_up(self, duration=0.5):
        """Look up with keyboard"""
        self._hold_key(self.KEYS['camera_up'], duration)
        print("Looking up")
    
    def look_down(self, duration=0.5):
        """Look down with keyboard"""
        self._hold_key(self.KEYS['camera_down'], duration)
        print("Looking down")

def get_spiderman_camera_commands(gamepad):
    """Get camera command mappings for Spider-Man"""
    spiderman = SpiderManCamera(gamepad)
    
    return {
        "look left": lambda: spiderman.look_left(),
        "look right": lambda: spiderman.look_right(),
        "look up": lambda: spiderman.look_up(),
        "look down": lambda: spiderman.look_down(),
    }
