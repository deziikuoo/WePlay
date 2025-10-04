#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Basic Actions
This module provides basic action controls for Spider-Man: Miles Morales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls
import vgamepad as vg

class SpiderManBasicActions(SpiderManKeyboardControls):
    """Spider-Man basic action controls"""
    
    def __init__(self, gamepad=None):
        super().__init__()
        self.gamepad = gamepad  # Keep gamepad for backward compatibility
    
    # === BASIC ACTIONS ===
    
    def jump(self):
        """Jump with Space key"""
        self._press_key(self.KEYS['jump'])
        print("Jumping")
    
    def attack(self):
        """Melee attack with Left Mouse Button"""
        self._press_key(self.KEYS['attack'])
        print("Melee attack")
    
    def dodge(self):
        """Dodge with Left Ctrl"""
        self._press_key(self.KEYS['dodge'])
        print("Dodging")
    
    def web_strike(self):
        """Web-strike with F"""
        self._press_key(self.KEYS['web_strike'])
        print("Web-strike")
    
    def swing(self, duration=1.0):
        """Swing with Left Shift"""
        self._hold_key(self.KEYS['swing'], duration)
        print(f"Swinging ({duration:.1f}s)")
    
    def aim(self, duration=1.0):
        """Aim with Right Mouse Button"""
        self._hold_key(self.KEYS['aim'], duration)
        print(f"Aiming ({duration:.1f}s)")
    
    def shoot_gadget(self):
        """Use gadget with E"""
        self._press_key(self.KEYS['gadget_use'])
        print("Using gadget")
    
    def gadget_select(self, duration=0.5):
        """Select gadget with E (hold)"""
        self._hold_key(self.KEYS['gadget_use'], duration)
        print("Selecting gadget")
    
    def venom_attack(self):
        """Venom attack with Right Mouse Button + action"""
        self._press_key(self.KEYS['aim'])  # Hold Right Mouse Button
        print("Venom attack")
    
    def camouflage(self):
        """Camouflage with R"""
        self._press_key(self.KEYS['camouflage'])
        print("Camouflage")
    
    def heal(self):
        """Heal with 1"""
        self._press_key(self.KEYS['heal'])
        print("Healing")
    
    def shortcut_1(self):
        """Shortcut 1 with P"""
        self._press_key(self.KEYS['shortcut_1'])
        print("Shortcut 1")
    
    def shortcut_2(self):
        """Shortcut 2 with G"""
        self._press_key(self.KEYS['shortcut_2'])
        print("Shortcut 2")
    
    def objective_scan(self):
        """Objective/Scan with Tab"""
        self._press_key(self.KEYS['map'])
        print("Objective/Scan")
    
    def perch_dive(self):
        """Perch/Dive with X"""
        self._press_key(self.KEYS['perch_dive'])
        print("Perch/Dive")

def get_spiderman_basic_actions_commands(gamepad):
    """Get basic action command mappings for Spider-Man"""
    spiderman = SpiderManBasicActions(gamepad)
    
    return {
        "jump": lambda: spiderman.jump(),
        "attack": lambda: spiderman.attack(),
        "dodge": lambda: spiderman.dodge(),
        "web strike": lambda: spiderman.web_strike(),
        "swing": lambda: spiderman.swing(),
        "aim": lambda: spiderman.aim(),
        "shoot gadget": lambda: spiderman.shoot_gadget(),
        "gadget select": lambda: spiderman.gadget_select(),
        "venom": lambda: spiderman.venom_attack(),
        "camouflage": lambda: spiderman.camouflage(),
        "heal": lambda: spiderman.heal(),
        "shortcut 1": lambda: spiderman.shortcut_1(),
        "shortcut 2": lambda: spiderman.shortcut_2(),
        "scan": lambda: spiderman.objective_scan(),
        "perch": lambda: spiderman.perch_dive(),
        "dive": lambda: spiderman.perch_dive(),
    }
