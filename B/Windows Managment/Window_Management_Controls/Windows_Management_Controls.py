#!/usr/bin/env python3
"""
Windows Management Controls
This module provides universal window management functionality for game automation.
Handles game window detection, focusing, and management across different games.
"""

import time
import win32gui
import win32con
import win32api
from typing import Optional, List, Tuple

class GameWindowManager:
    """Manages game window focus and operations for any game"""
    
    def __init__(self):
        self.game_window = None
        self.game_window_title = None
        self.find_game_window()
    
    def find_game_window(self) -> bool:
        """Find any game window"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                # Look for actual games (not launchers)
                if (window_title and 
                    (any(game in window_title.lower() for game in [
                        'grand theft auto', 'gta', 'forza', 'assassin', 
                        'call of duty', 'fifa', 'nba', 'madden', 'minecraft',
                        'fallout', 'elder scrolls', 'witcher', 'cyberpunk',
                        'red dead', 'spider-man', 'batman', 'tomb raider',
                        'rockstar', 'steam -', 'epic games -', 'origin -',
                        'uplay -', 'battle.net -'
                    ]) and
                    # Exclude launcher-only windows
                    not any(launcher in window_title.lower() for launcher in [
                        'steam$', 'epic games launcher', 'origin launcher',
                        'uplay launcher', 'battle.net launcher'
                    ]))
                ):
                    windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            self.game_window = windows[0][0]
            self.game_window_title = win32gui.GetWindowText(self.game_window)
            return True
        else:
            self.game_window = None
            self.game_window_title = None
            return False
    
    def wait_for_game(self) -> bool:
        """Wait for any game to be detected (no time limit)"""
        print("🔍 No game detected. Waiting for a game to be launched...")
        print("💡 Please launch any game with controller support")
        
        while not self.find_game_window():
            time.sleep(3)
        
        print(f"✅ Game detected: {self.game_window_title}")
        return True
    
    def focus_game(self) -> bool:
        """Focus the game window with multiple methods for stubborn games"""
        if not self.game_window:
            if not self.find_game_window():
                return False
        
        try:
            # Validate window handle is still valid
            if not win32gui.IsWindow(self.game_window):
                print("🔄 Window handle invalid, re-detecting game...")
                if not self.find_game_window():
                    return False
            
            # Method 1: Standard focus (works for most games)
            print("🔄 Method 1: Trying standard focus...")
            try:
                # Restore window if minimized
                if win32gui.IsIconic(self.game_window):
                    print("   📱 Restoring minimized window...")
                    win32gui.ShowWindow(self.game_window, win32con.SW_RESTORE)
                
                # Bring window to front
                print("   🎯 Setting foreground window...")
                win32gui.SetForegroundWindow(self.game_window)
                win32gui.BringWindowToTop(self.game_window)
                
                # Verify focus was successful
                time.sleep(0.1)
                if win32gui.GetForegroundWindow() == self.game_window:
                    print(f"✅ Method 1 SUCCESS: Game window focused: {self.game_window_title}")
                    return True
                else:
                    print("   ❌ Method 1 failed: Window not in foreground")
            except Exception as e:
                print(f"   ❌ Method 1 failed: {e}")
            
            # Method 2: Alternative focus for stubborn games (like Spider-Man)
            print("🔄 Method 2: Trying thread attachment focus...")
            try:
                # Get current thread and game thread
                current_thread = win32api.GetCurrentThreadId()
                game_thread = win32gui.GetWindowThreadProcessId(self.game_window)[1]
                print(f"   🧵 Current thread: {current_thread}, Game thread: {game_thread}")
                
                # Attach to game thread
                if current_thread != game_thread:
                    print("   🔗 Attaching to game thread...")
                    win32gui.AttachThreadInput(current_thread, game_thread, True)
                
                # Force focus
                print("   🎯 Forcing window focus...")
                win32gui.SetForegroundWindow(self.game_window)
                win32gui.SetActiveWindow(self.game_window)
                win32gui.BringWindowToTop(self.game_window)
                
                # Detach from game thread
                if current_thread != game_thread:
                    print("   🔓 Detaching from game thread...")
                    win32gui.AttachThreadInput(current_thread, game_thread, False)
                
                # Verify focus
                time.sleep(0.2)
                if win32gui.GetForegroundWindow() == self.game_window:
                    print(f"✅ Method 2 SUCCESS: Game window focused: {self.game_window_title}")
                    return True
                else:
                    print("   ❌ Method 2 failed: Window not in foreground")
            except Exception as e:
                print(f"   ❌ Method 2 failed: {e}")
            
            # Method 3: Last resort - click on window
            print("🔄 Method 3: Trying click-to-focus method...")
            try:
                # Get window rectangle
                rect = win32gui.GetWindowRect(self.game_window)
                center_x = (rect[0] + rect[2]) // 2
                center_y = (rect[1] + rect[3]) // 2
                print(f"   📐 Window rect: {rect}, Click position: ({center_x}, {center_y})")
                
                # Click on window center
                print("   🖱️ Moving cursor to window center...")
                win32api.SetCursorPos((center_x, center_y))
                
                print("   🖱️ Simulating mouse click...")
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0)
                
                time.sleep(0.3)
                if win32gui.GetForegroundWindow() == self.game_window:
                    print(f"✅ Method 3 SUCCESS: Game window focused: {self.game_window_title}")
                    return True
                else:
                    print("   ❌ Method 3 failed: Window not in foreground")
            except Exception as e:
                print(f"   ❌ Method 3 failed: {e}")
            
            print(f"❌ All focus methods failed for: {self.game_window_title}")
            return False
            
        except Exception as e:
            print(f"❌ Failed to focus game: {e}")
            return False
    
    def is_game_focused(self) -> bool:
        """Check if game is currently focused"""
        if not self.game_window:
            return False
        
        try:
            active_window = win32gui.GetForegroundWindow()
            return active_window == self.game_window
        except:
            return False
    
    def get_game_title(self) -> Optional[str]:
        """Get the current game window title"""
        return self.game_window_title
    
    def get_game_window_handle(self):
        """Get the current game window handle"""
        return self.game_window
    
    def refresh_game_detection(self) -> bool:
        """Refresh game detection and return True if game found"""
        return self.find_game_window()
    
    def list_all_game_windows(self) -> List[Tuple[int, str]]:
        """List all detected game windows"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if (window_title and 
                    any(game in window_title.lower() for game in [
                        'grand theft auto', 'gta', 'forza', 'assassin', 
                        'call of duty', 'fifa', 'nba', 'madden', 'minecraft',
                        'fallout', 'elder scrolls', 'witcher', 'cyberpunk',
                        'red dead', 'spider-man', 'batman', 'tomb raider',
                        'rockstar', 'steam -', 'epic games -', 'origin -',
                        'uplay -', 'battle.net -'
                    ]) and
                    not any(launcher in window_title.lower() for launcher in [
                        'steam$', 'epic games launcher', 'origin launcher',
                        'uplay launcher', 'battle.net launcher'
                    ])
                ):
                    windows.append((hwnd, window_title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows

# Window Management Commands
def get_window_management_commands(window_manager: GameWindowManager) -> dict:
    """Get window management command mappings"""
    return {
        "focus game": lambda: window_manager.focus_game(),
        "refocus": lambda: window_manager.focus_game(),
        "refresh game": lambda: window_manager.refresh_game_detection(),
        "check focus": lambda: print(f"Game focused: {window_manager.is_game_focused()}"),
        "game title": lambda: print(f"Current game: {window_manager.get_game_title()}"),
        "list games": lambda: print(f"Available games: {window_manager.list_all_game_windows()}"),
    }

if __name__ == "__main__":
    # Test the window management
    print("🪟 Windows Management Controls Test")
    print("=" * 50)
    
    try:
        manager = GameWindowManager()
        
        if manager.game_window:
            print(f"✅ Game detected: {manager.game_window_title}")
            print(f"🎯 Focus status: {manager.is_game_focused()}")
            
            # Test focus
            print("\n🧪 Testing focus...")
            success = manager.focus_game()
            print(f"Focus result: {success}")
        else:
            print("❌ No game detected")
            print("💡 Launch a game to test window management")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
