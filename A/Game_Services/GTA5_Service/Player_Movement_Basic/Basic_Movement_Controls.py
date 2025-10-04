#!/usr/bin/env python3
"""
GTA5 Basic Movement Controls
This module provides basic movement and camera controls for Grand Theft Auto V using vgamepad.
"""

import vgamepad as vg
import time
import random
from typing import Dict, Callable

class GTA5BasicMovement:
    """GTA5 specific basic movement controls using vgamepad"""
    
    def __init__(self, gamepad):
        self.gamepad = gamepad
        
        # Movement constants
        self.FORWARD_MAX = 32767
        self.BACKWARD_MAX = -32767
        self.RIGHT_MAX = 32767
        self.LEFT_MAX = -32767
        self.NEUTRAL = 0
        
        # Speed settings
        self.SLOW_SPEED = 0.3
        self.NORMAL_SPEED = 0.6
        self.FAST_SPEED = 0.9
        self.FULL_SPEED = 1.0
        
        # Duration settings
        self.WALK_DURATION = 1.0
        self.RUN_DURATION = 0.8
        self.SPRINT_DURATION = 1.2
        self.CAMERA_DURATION = 0.5
    
    def _add_human_delay(self):
        """Add human-like delay between inputs"""
        delay = random.uniform(0.05, 0.15)
        time.sleep(delay)
    
    def _move_stick(self, x_value, y_value, duration):
        """Move left stick to specified position for duration"""
        self._add_human_delay()
        
        print(f"🎯 Moving stick: X={x_value}, Y={y_value} for {duration:.1f}s")
        
        # Set stick position
        self.gamepad.left_joystick(x_value=x_value, y_value=y_value)
        self.gamepad.update()
        
        # Hold for duration
        time.sleep(duration)
        
        # Return to neutral
        self.gamepad.left_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        self.gamepad.update()
        
        # Post-movement delay
        time.sleep(random.uniform(0.1, 0.3))
        print("✅ Movement completed")
    
    def _move_camera(self, x_value, y_value, duration):
        """Move right stick for camera control"""
        self._add_human_delay()
        
        print(f"📷 Moving camera: X={x_value}, Y={y_value} for {duration:.1f}s")
        
        # Set camera position
        self.gamepad.right_joystick(x_value=x_value, y_value=y_value)
        self.gamepad.update()
        
        # Hold for duration
        time.sleep(duration)
        
        # Return to neutral
        self.gamepad.right_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        self.gamepad.update()
        
        # Post-movement delay
        time.sleep(random.uniform(0.1, 0.2))
        print("✅ Camera movement completed")
    
    # === BASIC MOVEMENT ===
    
    def walk_forward(self, speed=None, duration=None):
        """Walk forward with specified speed and duration"""
        if duration is None:
            duration = self.WALK_DURATION
        if speed is None:
            speed = self.NORMAL_SPEED
        
        print(f"🚶 Walking forward (speed: {speed:.1f}, duration: {duration:.1f}s)")
        y_value = int(self.FORWARD_MAX * speed)
        self._move_stick(self.NEUTRAL, y_value, duration)
    
    def walk_backward(self, speed=None, duration=None):
        """Walk backward with specified speed and duration"""
        if duration is None:
            duration = self.WALK_DURATION
        if speed is None:
            speed = self.NORMAL_SPEED
        
        print(f"🚶 Walking backward (speed: {speed:.1f}, duration: {duration:.1f}s)")
        y_value = int(self.BACKWARD_MAX * speed)
        self._move_stick(self.NEUTRAL, y_value, duration)
    
    def walk_left(self, speed=None, duration=None):
        """Walk left with specified speed and duration"""
        if duration is None:
            duration = self.WALK_DURATION
        if speed is None:
            speed = self.NORMAL_SPEED
        
        print(f"🚶 Walking left (speed: {speed:.1f}, duration: {duration:.1f}s)")
        x_value = int(self.LEFT_MAX * speed)
        self._move_stick(x_value, self.NEUTRAL, duration)
    
    def walk_right(self, speed=None, duration=None):
        """Walk right with specified speed and duration"""
        if duration is None:
            duration = self.WALK_DURATION
        if speed is None:
            speed = self.NORMAL_SPEED
        
        print(f"🚶 Walking right (speed: {speed:.1f}, duration: {duration:.1f}s)")
        x_value = int(self.RIGHT_MAX * speed)
        self._move_stick(x_value, self.NEUTRAL, duration)
    
    def run_forward(self, duration=None):
        """Run forward with full speed"""
        if duration is None:
            duration = self.RUN_DURATION
        
        print(f"🏃 Running forward (duration: {duration:.1f}s)")
        y_value = self.FORWARD_MAX
        self._move_stick(self.NEUTRAL, y_value, duration)
    
    def sprint_forward(self, duration=None):
        """Sprint forward with A button"""
        if duration is None:
            duration = self.SPRINT_DURATION
        
        print(f"💨 Sprinting forward (duration: {duration:.1f}s)")
        self._add_human_delay()
        
        # Press A button and move forward
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.left_joystick(x_value=self.NEUTRAL, y_value=self.FORWARD_MAX)
        self.gamepad.update()
        
        # Hold for duration
        time.sleep(duration)
        
        # Release A button and return to neutral
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.left_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        self.gamepad.update()
        
        # Post-movement delay
        time.sleep(random.uniform(0.1, 0.3))
        print("✅ Sprint completed")
    
    # === CAMERA CONTROL ===
    
    def look_left(self, duration=None, sensitivity=None):
        """Look left with camera"""
        if duration is None:
            duration = self.CAMERA_DURATION
        if sensitivity is None:
            sensitivity = 0.8
        
        print(f"👀 Looking left (sensitivity: {sensitivity:.1f})")
        x_value = int(self.LEFT_MAX * sensitivity)
        self._move_camera(x_value, self.NEUTRAL, duration)
    
    def look_right(self, duration=None, sensitivity=None):
        """Look right with camera"""
        if duration is None:
            duration = self.CAMERA_DURATION
        if sensitivity is None:
            sensitivity = 0.8
        
        print(f"👀 Looking right (sensitivity: {sensitivity:.1f})")
        x_value = int(self.RIGHT_MAX * sensitivity)
        self._move_camera(x_value, self.NEUTRAL, duration)
    
    def look_up(self, duration=None, sensitivity=None):
        """Look up with camera"""
        if duration is None:
            duration = self.CAMERA_DURATION
        if sensitivity is None:
            sensitivity = 0.8
        
        print(f"👀 Looking up (sensitivity: {sensitivity:.1f})")
        y_value = int(self.FORWARD_MAX * sensitivity)
        self._move_camera(self.NEUTRAL, y_value, duration)
    
    def look_down(self, duration=None, sensitivity=None):
        """Look down with camera"""
        if duration is None:
            duration = self.CAMERA_DURATION
        if sensitivity is None:
            sensitivity = 0.8
        
        print(f"👀 Looking down (sensitivity: {sensitivity:.1f})")
        y_value = int(self.BACKWARD_MAX * sensitivity)
        self._move_camera(self.NEUTRAL, y_value, duration)
    
    def center_camera(self):
        """Center the camera"""
        print("🎯 Centering camera")
        self._move_camera(self.NEUTRAL, self.NEUTRAL, 0.1)
    
    # === BASIC ACTIONS ===
    
    def jump(self):
        """Jump with X button"""
        print("🦘 Jumping")
        self._add_human_delay()
        
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
        
        time.sleep(random.uniform(0.1, 0.3))
        print("✅ Jump completed")
    
    def crouch(self):
        """Crouch with B button"""
        print("🦆 Crouching")
        self._add_human_delay()
        
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        
        time.sleep(random.uniform(0.1, 0.3))
        print("✅ Crouch completed")
    
    def stop(self):
        """Stop all movement"""
        print("🛑 Stopping all movement")
        self.gamepad.left_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        self.gamepad.right_joystick(x_value=self.NEUTRAL, y_value=self.NEUTRAL)
        self.gamepad.update()
        print("✅ Stopped")

def get_gta5_basic_movement_commands(gamepad):
    """Get the complete command mapping for GTA5 basic movement"""
    gta5 = GTA5BasicMovement(gamepad)
    
    return {
        # Basic Movement
        "walk forward": lambda: gta5.walk_forward(),
        "walk backward": lambda: gta5.walk_backward(),
        "walk left": lambda: gta5.walk_left(),
        "walk right": lambda: gta5.walk_right(),
        "run forward": lambda: gta5.run_forward(),
        "sprint forward": lambda: gta5.sprint_forward(),
        
        # Speed Control
        "slow walk forward": lambda: gta5.walk_forward(speed=gta5.SLOW_SPEED),
        "normal walk forward": lambda: gta5.walk_forward(speed=gta5.NORMAL_SPEED),
        "fast walk forward": lambda: gta5.walk_forward(speed=gta5.FAST_SPEED),
        
        # Camera Control
        "look left": lambda: gta5.look_left(),
        "look right": lambda: gta5.look_right(),
        "look up": lambda: gta5.look_up(),
        "look down": lambda: gta5.look_down(),
        "center camera": lambda: gta5.center_camera(),
        
        # Actions
        "jump": lambda: gta5.jump(),
        "crouch": lambda: gta5.crouch(),
        "stop": lambda: gta5.stop(),
    }

if __name__ == "__main__":
    # Test the GTA5 basic movement controls
    import vgamepad as vg
    
    print("🎮 GTA5 Basic Movement Controls Test")
    print("=" * 50)
    
    try:
        gamepad = vg.VX360Gamepad()
        gta5 = GTA5BasicMovement(gamepad)
        
        print("✅ GTA5 basic movement controls initialized")
        print("🧪 Testing basic movement...")
        
        gta5.walk_forward(duration=0.5)
        gta5.jump()
        gta5.look_left(duration=0.3)
        gta5.sprint_forward(duration=0.5)
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
