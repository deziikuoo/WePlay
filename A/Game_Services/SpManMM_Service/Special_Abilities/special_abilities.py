#!/usr/bin/env python3
"""
Spider-Man: Miles Morales - Special Abilities
This module provides special ability controls for Spider-Man: Miles Morales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spiderman_keyboard_controls import SpiderManKeyboardControls
import time

class SpiderManSpecialAbilities(SpiderManKeyboardControls):
    """Spider-Man special ability controls"""
    
    def __init__(self, gamepad=None):
        super().__init__()
        self.gamepad = gamepad  # Keep gamepad for backward compatibility
    
    # === SPECIAL ABILITIES ===
    
    def zip_to_point(self, duration=1.0):
        """Zip to Point: C"""
        self._hold_key(self.KEYS['zip_to_point'], duration)
        print(f"Zip to Point ({duration:.1f}s)")
    
    def venom_jump(self):
        """Venom Jump: Right Mouse Button + Space"""
        self._key_combo([self.KEYS['aim'], self.KEYS['jump']])
        print("Venom Jump")
    
    def venom_punch(self):
        """Venom Punch: Right Mouse Button + Left Mouse Button"""
        self._key_combo([self.KEYS['aim'], self.KEYS['attack']])
        print("Venom Punch")
    
    def venom_dash(self):
        """Venom Dash: Right Mouse Button + Ctrl"""
        self._key_combo([self.KEYS['aim'], self.KEYS['dodge']])
        print("Venom Dash")
    
    def venom_smash(self):
        """Venom Smash: Right Mouse Button + F"""
        self._key_combo([self.KEYS['aim'], self.KEYS['web_strike']])
        print("Venom Smash")
    
    def mega_venom_blast(self):
        """Mega Venom Blast: Right Mouse Button + multiple actions"""
        self._key_combo([self.KEYS['aim'], self.KEYS['attack'], self.KEYS['jump']])
        print("Mega Venom Blast")
    
    def finisher(self):
        """Finisher: 2 key (when Focus bar is full)"""
        self._press_key(self.KEYS['finisher'])
        print("Finisher")

def get_spiderman_special_abilities_commands(gamepad):
    """Get special ability command mappings for Spider-Man"""
    spiderman = SpiderManSpecialAbilities(None)  # No gamepad needed for keyboard
    
    return {
        "zip to point": lambda: spiderman.zip_to_point(),
        "venom jump": lambda: spiderman.venom_jump(),
        "venom punch": lambda: spiderman.venom_punch(),
        "venom dash": lambda: spiderman.venom_dash(),
        "venom smash": lambda: spiderman.venom_smash(),
        "mega venom blast": lambda: spiderman.mega_venom_blast(),
        "finisher": lambda: spiderman.finisher(),
    }
