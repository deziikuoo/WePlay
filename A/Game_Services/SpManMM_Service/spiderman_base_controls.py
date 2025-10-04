#!/usr/bin/env python3
"""
Spider-Man: Miles Morales Base Controls
This module provides the base class and shared methods for Spider-Man: Miles Morales controls.
"""

import vgamepad as vg
import time
import random

class SpiderManControls:
    """Base class for Spider-Man: Miles Morales controls using vgamepad"""
    
    def __init__(self, gamepad):
        self.gamepad = gamepad
        
        # Movement constants
        self.STICK_MAX = 32767
        self.STICK_MIN = -32767
        self.NEUTRAL = 0
        
        # Speed settings
        self.WALK_SPEED = 0.3
        self.NORMAL_SPEED = 0.6
        self.RUN_SPEED = 0.9
        self.FULL_SPEED = 1.0
        
        # Duration settings
        self.ACTION_DURATION = 0.1
        self.COMBO_DURATION = 0.2
        self.HOLD_DURATION = 0.5
    
    def _add_human_delay(self):
        """Add human-like delay between inputs"""
        delay = random.uniform(0.05, 0.15)
        time.sleep(delay)
    
    def _press_button(self, button, duration=None):
        """Press and release a button"""
        if duration is None:
            duration = self.ACTION_DURATION
        
        self._add_human_delay()
        self.gamepad.press_button(button)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.release_button(button)
        self.gamepad.update()
        time.sleep(random.uniform(0.1, 0.2))
    
    def _hold_button(self, button, duration):
        """Hold a button for specified duration"""
        self._add_human_delay()
        self.gamepad.press_button(button)
        self.gamepad.update()
        time.sleep(duration)
        self.gamepad.release_button(button)
        self.gamepad.update()
        time.sleep(random.uniform(0.1, 0.2))
    
    def _move_stick(self, stick, x_value, y_value, duration):
        """Move a stick to specified position for duration"""
        print(f"[DEBUG] _move_stick called: stick={stick}, x={x_value}, y={y_value}, duration={duration}")
        
        self._add_human_delay()
        print(f"[DEBUG] Human delay completed")
        
        if stick == "left":
            print(f"[DEBUG] Setting LEFT stick: x={x_value}, y={y_value}")
            self.gamepad.left_joystick(x_value=x_value, y_value=y_value)
        elif stick == "right":
            print(f"[DEBUG] Setting RIGHT stick: x={x_value}, y={y_value}")
            self.gamepad.right_joystick(x_value=x_value, y_value=y_value)
        
        print(f"[DEBUG] Calling gamepad.update()")
        self.gamepad.update()
        print(f"[DEBUG] Gamepad updated successfully, sleeping for {duration}s")
        
        time.sleep(duration)
        print(f"[DEBUG] Sleep completed, returning to neutral")
        
        # Return to neutral
        if stick == "left":
            print(f"[DEBUG] Returning LEFT stick to neutral: x={self.NEUTRAL}, y={self.NEUTRAL}")
            self.gamepad.left_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        elif stick == "right":
            print(f"[DEBUG] Returning RIGHT stick to neutral: x={self.NEUTRAL}, y={self.NEUTRAL}")
            self.gamepad.right_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        
        print(f"[DEBUG] Final gamepad.update() call")
        self.gamepad.update()
        print(f"[DEBUG] Final update completed")
        
        time.sleep(random.uniform(0.1, 0.2))
        print(f"[DEBUG] _move_stick completed successfully")
    
    def _press_trigger(self, trigger, pressure, duration):
        """Press trigger with specified pressure"""
        self._add_human_delay()
        
        if trigger == "left":
            self.gamepad.left_trigger(pressure)
        elif trigger == "right":
            self.gamepad.right_trigger(pressure)
        
        self.gamepad.update()
        time.sleep(duration)
        
        # Release trigger
        if trigger == "left":
            self.gamepad.left_trigger(0)
        elif trigger == "right":
            self.gamepad.right_trigger(0)
        
        self.gamepad.update()
        time.sleep(random.uniform(0.1, 0.2))

if __name__ == "__main__":
    # Test the base Spider-Man controls
    import vgamepad as vg
    
    print("🕷️ Spider-Man Base Controls Test")
    print("=" * 50)
    
    try:
        gamepad = vg.VX360Gamepad()
        spiderman = SpiderManControls(gamepad)
        
        print("✅ Spider-Man base controls initialized")
        print("🧪 Testing shared methods...")
        
        # Test shared methods
        spiderman._add_human_delay()
        spiderman._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A, 0.1)
        spiderman._move_stick("left", 0, 16383, 0.5)
        
        print("✅ All base tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")