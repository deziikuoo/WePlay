#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Basic Movement Controls
This module provides basic movement controls for Spider-Man: Miles Morales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls

class SpiderManMovement(SpiderManKeyboardControls):
    """Spider-Man basic movement controls"""
    
    def __init__(self, gamepad=None):
        super().__init__()
        self.gamepad = gamepad  # Keep gamepad for backward compatibility
    
    # === BASIC MOVEMENT ===
    
    def _move_forward(self, speed, duration=1.0, walk_mode=False):
        """Generic forward movement with specified speed using keyboard"""
        print(f"[DEBUG] _move_forward called: speed={speed}, duration={duration}, walk_mode={walk_mode}")
        
        # Use walk key (Alt) if in walk mode, otherwise use W
        if walk_mode:
            print(f"[DEBUG] Using walk mode (Alt + W) for {duration}s")
            self._key_combo([self.KEYS['walk'], self.KEYS['forward']], duration)
        else:
            print(f"[DEBUG] Holding forward key for {duration}s")
            self._hold_key(self.KEYS['forward'], duration)
        
        print(f"Moving forward (speed: {speed:.1f})")
        print(f"[DEBUG] _move_forward completed")
    
    def jog_forward(self, duration=1.0):
        """Jog forward with keyboard (60% speed)"""
        self._move_forward(0.6, duration)
    
    def walk_backward(self, duration=1.0):
        """Walk backward with keyboard (Alt + S)"""
        self._key_combo([self.KEYS['walk'], self.KEYS['backward']], duration)
        print(f"Walking backward ({duration:.1f}s)")
    
    def walk_left(self, duration=1.0):
        """Walk left with keyboard (Alt + A)"""
        self._key_combo([self.KEYS['walk'], self.KEYS['left']], duration)
        print(f"Walking left ({duration:.1f}s)")
    
    def walk_right(self, duration=1.0):
        """Walk right with keyboard (Alt + D)"""
        self._key_combo([self.KEYS['walk'], self.KEYS['right']], duration)
        print(f"Walking right ({duration:.1f}s)")
    
    def jog_backward(self, duration=1.0):
        """Jog backward with keyboard (60% speed)"""
        self._hold_key(self.KEYS['backward'], duration)
        print(f"Jogging backward ({duration:.1f}s)")
    
    def jog_left(self, duration=1.0):
        """Jog left with keyboard (60% speed)"""
        self._hold_key(self.KEYS['left'], duration)
        print(f"Jogging left ({duration:.1f}s)")
    
    
    def jog_right(self, duration=1.0):
        """Jog right with keyboard (60% speed)"""
        self._hold_key(self.KEYS['right'], duration)
        print(f"Jogging right ({duration:.1f}s)")
    
    def sprint(self, duration=1.0):
        """Sprint with Shift key (100% speed)"""
        self._hold_key(self.KEYS['swing'], duration)
        print(f"Sprinting ({duration:.1f}s)")

def get_spiderman_movement_commands(gamepad):
    """Get movement command mappings for Spider-Man"""
    spiderman = SpiderManMovement(gamepad)
    
    return {
        "walk forward": lambda: spiderman._move_forward(0.3, 3.0, walk_mode=True),  # Alt + W for 3 seconds
        "walk backward": lambda: spiderman.walk_backward(3.0),      # Alt + S for 3 seconds
        "walk left": lambda: spiderman.walk_left(3.0),              # Alt + A for 3 seconds
        "walk right": lambda: spiderman.walk_right(3.0),            # Alt + D for 3 seconds
        "run forward": lambda: spiderman._move_forward(0.8),        # W key
        "jog forward": lambda: spiderman.jog_forward(),
        "jog backward": lambda: spiderman.jog_backward(),
        "jog left": lambda: spiderman.jog_left(),
        "jog right": lambda: spiderman.jog_right(),
        "sprint": lambda: spiderman.sprint(),
    }
