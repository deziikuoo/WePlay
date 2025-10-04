#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Keyboard Controls
This module provides keyboard-based controls for Spider-Man: Miles Morales.
"""

import time
import random
import pydirectinput

class SpiderManKeyboardControls:
    """Base class for Spider-Man keyboard controls"""
    
    def __init__(self):
        """Initialize keyboard controller"""
        # Configure pydirectinput for game compatibility
        pydirectinput.FAILSAFE = False
        pydirectinput.PAUSE = 0.01
        
        # Official PC controls for Spider-Man: Miles Morales
        self.KEYS = {
            # Core Movement
            'forward': 'w',
            'backward': 's',
            'left': 'a',
            'right': 'd',
            'jump': 'space',
            'swing': 'shift',
            'zip_to_point': 'c',
            'perch_dive': 'x',
            'air_trick': 't',
            'walk': 'alt',
            
            # Combat Controls
            'attack': 'left_click',  # Left Mouse Button
            'web_strike': 'f',
            'dodge': 'ctrl',
            'yank_throw': 'q',
            'aim': 'right_click',  # Right Mouse Button
            'camouflage': 'r',
            'blinding_light': '3',
            'finisher': '2',
            'heal': '1',
            
            # Gadget Controls
            'gadget_use': 'e',
            'gadget_prev': 'wheel_up',
            'gadget_next': 'wheel_down',
            
            # General Functions
            'map': 'tab',
            'fnsm_app': 'm',
            'objectives': 'v',
            'shortcut_1': 'p',
            'shortcut_2': 'g',
            'pause': 'esc',
            
            # Legacy mappings for backward compatibility
            'web_zip': 'space',  # Same as jump
            'interact': 'e',
        }
    
    def _add_human_delay(self):
        """Add a small random delay to make inputs more human-like"""
        delay = random.uniform(0.05, 0.15)
        time.sleep(delay)
    
    def _press_key(self, key, duration=0.1):
        """Press a key for a specified duration"""
        self._add_human_delay()
        
        # Press and hold the key
        pydirectinput.keyDown(key)
        time.sleep(duration)
        
        # Release the key
        pydirectinput.keyUp(key)
    
    def _hold_key(self, key, duration):
        """Hold a key for a specified duration"""
        self._add_human_delay()
        
        # Press and hold the key
        pydirectinput.keyDown(key)
        time.sleep(duration)
        
        # Release the key
        pydirectinput.keyUp(key)
    
    def _key_combo(self, keys, duration=0.1):
        """Press multiple keys simultaneously for a specified duration"""
        self._add_human_delay()
        
        # Press all keys
        for key in keys:
            pydirectinput.keyDown(key)
        
        time.sleep(duration)
        
        # Release all keys (in reverse order)
        for key in reversed(keys):
            pydirectinput.keyUp(key)
