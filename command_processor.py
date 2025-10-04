#!/usr/bin/env python3
"""
GTA5 Command Processor
This script handles real-time command input and processes them into vgamepad actions.
"""

import vgamepad as vg
import time
import random
import sys
import os
import threading
import queue
import win32gui
import win32con
import win32api
import win32process
import importlib.util
try:
    import readline
except ImportError:
    # Windows fallback - use pyreadline3 if available
    try:
        import pyreadline3 as readline
    except ImportError:
        # No readline available - disable advanced features
        readline = None

from typing import Dict, Callable, Optional

class GameServiceRegistry:
    """Dynamic game service registry that loads commands based on detected game"""
    
    def __init__(self, gamepad):
        self.gamepad = gamepad
        self.current_game = None
        self.current_commands = {}
        self.game_services = {
            'spider-man': self._load_spiderman_commands,
            'grand theft auto': self._load_gta5_commands,
            'gta': self._load_gta5_commands,
        }
    
    def detect_and_load_game(self, game_title):
        """Detect game and load appropriate commands"""
        if not game_title:
            return False
        
        game_title_lower = game_title.lower()
        
        # Find matching game service
        for game_key, loader_func in self.game_services.items():
            if game_key in game_title_lower:
                print(f"Loading commands for: {game_key.title()}")
                self.current_commands = loader_func()
                self.current_game = game_key
                print(f"Loaded {len(self.current_commands)} commands for {game_key.title()}")
                return True
        
        # Default to generic commands if no specific game found
        print("No specific game service found, using generic commands")
        self.current_commands = self._load_generic_commands()
        self.current_game = 'generic'
        return True
    
    def _load_spiderman_commands(self):
        """Load Spider-Man: Miles Morales commands"""
        commands = {}
        
        try:
            # Import Spider-Man modules
            spiderman_base_path = os.path.join(os.path.dirname(__file__), 'A', 'Game_Services', 'SpManMM_Service')
            
            # Load movement commands
            movement_path = os.path.join(spiderman_base_path, 'Basic_Movement', 'movement_controls.py')
            if os.path.exists(movement_path):
                spec = importlib.util.spec_from_file_location("movement_controls", movement_path)
                movement_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(movement_module)
                commands.update(movement_module.get_spiderman_movement_commands(None))  # No gamepad needed for keyboard
            
            # Load basic actions
            actions_path = os.path.join(spiderman_base_path, 'Basic_Actions', 'basic_actions.py')
            if os.path.exists(actions_path):
                spec = importlib.util.spec_from_file_location("basic_actions", actions_path)
                actions_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(actions_module)
                commands.update(actions_module.get_spiderman_basic_actions_commands(None))  # No gamepad needed for keyboard
            
            # Load camera commands
            camera_path = os.path.join(spiderman_base_path, 'Camera_Controls', 'camera_controls.py')
            if os.path.exists(camera_path):
                spec = importlib.util.spec_from_file_location("camera_controls", camera_path)
                camera_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(camera_module)
                commands.update(camera_module.get_spiderman_camera_commands(None))  # No gamepad needed for keyboard wa2    ww 
            
            # Load special abilities
            special_path = os.path.join(spiderman_base_path, 'Special_Abilities', 'special_abilities.py')
            if os.path.exists(special_path):
                spec = importlib.util.spec_from_file_location("special_abilities", special_path)
                special_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(special_module)
                commands.update(special_module.get_spiderman_special_abilities_commands(None))  # No gamepad needed for keyboard
            
            # Load additional actions
            additional_path = os.path.join(spiderman_base_path, 'Additional_Actions', 'additional_actions.py')
            if os.path.exists(additional_path):
                spec = importlib.util.spec_from_file_location("additional_actions", additional_path)
                additional_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(additional_module)
                commands.update(additional_module.get_spiderman_additional_actions_commands(None))  # No gamepad needed for keyboard
            
            # Load scenario scripts
            scenario_path = os.path.join(spiderman_base_path, 'Scenario_Scripts', 'scenario_scripts.py')
            if os.path.exists(scenario_path):
                spec = importlib.util.spec_from_file_location("scenario_scripts", scenario_path)
                scenario_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(scenario_module)
                commands.update(scenario_module.get_spiderman_scenario_scripts_commands(None))  # No gamepad needed for keyboard
                
        except Exception as e:
            print(f"Error loading Spider-Man commands: {e}")
            return self._load_generic_commands()
        
        return commands
    
    def _load_gta5_commands(self):
        """Load GTA5 commands (placeholder for future implementation)"""
        print("GTA5 service not yet implemented, using generic commands")
        return self._load_generic_commands()
    
    def _load_generic_commands(self):
        """Load generic commands that work with most games"""
        return {
            # Basic Movement
            "walk forward": lambda: self._generic_walk_forward(),
            "walk backward": lambda: self._generic_walk_backward(),
            "walk left": lambda: self._generic_walk_left(),
            "walk right": lambda: self._generic_walk_right(),
            "run forward": lambda: self._generic_run_forward(),
            
            # Camera Control
            "look left": lambda: self._generic_look_left(),
            "look right": lambda: self._generic_look_right(),
            "look up": lambda: self._generic_look_up(),
            "look down": lambda: self._generic_look_down(),
            
            # Basic Actions
            "jump": lambda: self._generic_jump(),
            "stop": lambda: self._generic_stop(),
        }
    
    def get_command(self, command_name):
        """Get a command by name"""
        command_func = self.current_commands.get(command_name.lower().strip())
        return command_func
    
    def list_available_commands(self):
        """List all available commands for current game"""
        return list(self.current_commands.keys())
    
    # Generic command implementations
    def _generic_walk_forward(self):
        print("Walking forward (generic)")
        self.gamepad.left_joystick(x_value=0, y_value=16383)
        self.gamepad.update()
        time.sleep(1.0)
        self.gamepad.left_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_walk_backward(self):
        print("Walking backward (generic)")
        self.gamepad.left_joystick(x_value=0, y_value=-16383)
        self.gamepad.update()
        time.sleep(1.0)
        self.gamepad.left_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_walk_left(self):
        print("Walking left (generic)")
        self.gamepad.left_joystick(x_value=-16383, y_value=0)
        self.gamepad.update()
        time.sleep(1.0)
        self.gamepad.left_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_walk_right(self):
        print("Walking right (generic)")
        self.gamepad.left_joystick(x_value=16383, y_value=0)
        self.gamepad.update()
        time.sleep(1.0)
        self.gamepad.left_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_run_forward(self):
        print("Running forward (generic)")
        self.gamepad.left_joystick(x_value=0, y_value=32767)
        self.gamepad.update()
        time.sleep(1.0)
        self.gamepad.left_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_look_left(self):
        print("Looking left (generic)")
        self.gamepad.right_joystick(x_value=-16383, y_value=0)
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.right_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_look_right(self):
        print("Looking right (generic)")
        self.gamepad.right_joystick(x_value=16383, y_value=0)
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.right_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_look_up(self):
        print("Looking up (generic)")
        self.gamepad.right_joystick(x_value=0, y_value=16383)
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.right_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_look_down(self):
        print("Looking down (generic)")
        self.gamepad.right_joystick(x_value=0, y_value=-16383)
        self.gamepad.update()
        time.sleep(0.5)
        self.gamepad.right_joystick(x_value=0, y_value=0)
        self.gamepad.update()
    
    def _generic_jump(self):
        print("Jumping (generic)")
        self.gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
    
    def _generic_stop(self):
        print("Stopping (generic)")
        self.gamepad.left_joystick(x_value=0, y_value=0)
        self.gamepad.right_joystick(x_value=0, y_value=0)
        self.gamepad.update()

class GameWindowManager:
    """Manages game window focus and operations"""
    
    def __init__(self):
        self.game_window = None
        self.game_window_title = None
        self.find_game_window()
    
    def find_game_window(self):
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
    
    def wait_for_game(self):
        """Wait for any game to be detected (no time limit)"""
        print("No game detected. Waiting for a game to be launched...")
        print("Please launch any game with controller support")
        
        while not self.find_game_window():
            time.sleep(3)
        
        print(f"Game detected: {self.game_window_title}")
        return True
    
    def focus_game(self):
        """Focus the game window with multiple methods for stubborn games"""
        if not self.game_window:
            if not self.find_game_window():
                return False
        
        try:
            # Validate window handle is still valid
            if not win32gui.IsWindow(self.game_window):
                print(" Window handle invalid, re-detecting game...")
                if not self.find_game_window():
                    return False
            
            # Method 1: Standard focus (works for most games)
            print(" Method 1: Trying standard focus...")
            try:
                # Restore window if minimized
                if win32gui.IsIconic(self.game_window):
                    print("    Restoring minimized window...")
                    win32gui.ShowWindow(self.game_window, win32con.SW_RESTORE)
                
                # Bring window to front
                print("    Setting foreground window...")
                win32gui.SetForegroundWindow(self.game_window)
                win32gui.BringWindowToTop(self.game_window)
                
                # Verify focus was successful
                time.sleep(0.1)
                if win32gui.GetForegroundWindow() == self.game_window:
                    print(f" Method 1 SUCCESS: Game window focused: {self.game_window_title}")
                    return True
                else:
                    print("    Method 1 failed: Window not in foreground")
            except Exception as e:
                print(f"    Method 1 failed: {e}")
            
            # Method 2: Alternative focus for stubborn games (like Spider-Man) - DISABLED
            # print(" Method 2: Trying thread attachment focus...")
            # try:
            #     # Get current thread and game thread
            #     current_thread = win32api.GetCurrentThreadId()
            #     game_thread = win32process.GetWindowThreadProcessId(self.game_window)[1]
            #     print(f"    Current thread: {current_thread}, Game thread: {game_thread}")
            #     
            #     # Attach to game thread
            #     if current_thread != game_thread:
            #         print("    Attaching to game thread...")
            #         win32gui.AttachThreadInput(current_thread, game_thread, True)
            #     
            #     # Force focus
            #     print("    Forcing window focus...")
            #     win32gui.SetForegroundWindow(self.game_window)
            #     win32gui.SetActiveWindow(self.game_window)
            #     win32gui.BringWindowToTop(self.game_window)
            #     
            #     # Detach from game thread
            #     if current_thread != game_thread:
            #         print("    Detaching from game thread...")
            #         win32gui.AttachThreadInput(current_thread, game_thread, False)
            #     
            #     # Verify focus
            #     time.sleep(0.2)
            #     if win32gui.GetForegroundWindow() == self.game_window:
            #         print(f" Method 2 SUCCESS: Game window focused: {self.game_window_title}")
            #         return True
            #     else:
            #         print("    Method 2 failed: Window not in foreground")
            # except Exception as e:
            #     print(f"    Method 2 failed: {e}")
            
            # Method 3: Enhanced click-to-focus method
            print(" Method 3: Trying enhanced click-to-focus method...")
            try:
                # Get window rectangle
                rect = win32gui.GetWindowRect(self.game_window)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                
                # Try multiple click positions for better success rate
                click_positions = [
                    ((rect[0] + rect[2]) // 2, (rect[1] + rect[3]) // 2),  # Center
                    (rect[0] + width // 4, rect[1] + height // 4),         # Top-left quarter
                    (rect[0] + 3 * width // 4, rect[1] + height // 4),     # Top-right quarter
                ]
                
                for i, (click_x, click_y) in enumerate(click_positions):
                    print(f"    Attempt {i+1}: Clicking at ({click_x}, {click_y})")
                    
                    # Move cursor and click
                    win32api.SetCursorPos((click_x, click_y))
                    time.sleep(0.1)  # Brief pause
                    
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, click_x, click_y, 0, 0)
                    time.sleep(0.05)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, click_x, click_y, 0, 0)
                
                time.sleep(0.3)
                if win32gui.GetForegroundWindow() == self.game_window:
                    print(f" Method 3 SUCCESS: Game window focused: {self.game_window_title}")
                    return True
                
                print("    Method 3 failed: All click attempts failed")
            except Exception as e:
                print(f"    Method 3 failed: {e}")
            
            print(f" All focus methods failed for: {self.game_window_title}")
            return False
            
        except Exception as e:
            print(f" Failed to focus game: {e}")
            return False
    
    def is_game_focused(self):
        """Check if game is currently focused"""
        if not self.game_window:
            return False
        
        try:
            active_window = win32gui.GetForegroundWindow()
            return active_window == self.game_window
        except:
            return False

class GameCommandProcessor:
    """Processes commands and executes vgamepad actions"""
    
    def __init__(self):
        # Initialize window manager
        self.window_manager = GameWindowManager()
        
        # Initialize game service registry (no gamepad for keyboard)
        self.service_registry = GameServiceRegistry(None)
        
        # Command queue for processing
        self.command_queue = queue.Queue()
        self.is_running = False
        
        # Command history for auto-completion
        self.command_history = []
        self.history_index = 0
        
        # Setup readline for command history and completion
        self._setup_readline()
        
        print("Game Command Processor Ready!")
    
    def _setup_readline(self):
        """Setup readline for command history and auto-completion"""
        if readline is None:
            print("  Advanced features disabled: readline not available")
            print("   Install with: pip install pyreadline3")
            return
        
        # Enable history and completion
        readline.parse_and_bind("tab: complete")
        readline.parse_and_bind("set editing-mode emacs")
        
        # Set up completion function
        readline.set_completer(self._completer)
        
        # Enable history search
        readline.parse_and_bind("\\C-r: reverse-search-history")
        readline.parse_and_bind("\\C-s: forward-search-history")
        
        # Set up history length
        readline.set_history_length(100)
        
        # Test readline functionality
        print("Testing readline functionality...")
        try:
            # Add a test command to history
            readline.add_history("test_command")
            history_count = readline.get_current_history_length()
            print(f"Readline test successful - history count: {history_count}")
        except Exception as e:
            print(f"Readline test failed: {e}")
        
        # Set up history file with 100 command limit
        history_file = os.path.join(os.path.expanduser("~"), ".game_command_history")
        print(f"History file path: {history_file}")
        
        try:
            if os.path.exists(history_file):
                readline.read_history_file(history_file)
                # Limit history to last 100 commands
                readline.set_history_length(100)
                history_count = readline.get_current_history_length()
                if history_count > 0:
                    print(f" Loaded {history_count} commands from previous session")
                else:
                    print(" History file found but empty")
            else:
                print(" No previous command history found - starting fresh")
                # Create empty history file
                with open(history_file, 'w') as f:
                    pass
        except Exception as e:
            print(f"  Error loading history: {e}")
            pass
        
        # Save history on exit (only last 100 commands)
        import atexit
        atexit.register(self._save_history)
        
        # Also save history periodically during session
        self.history_save_counter = 0
    
    def _save_history(self):
        """Save only the last 100 commands to history file"""
        if readline is None:
            return
            
        history_file = os.path.join(os.path.expanduser("~"), ".game_command_history")
        try:
            # Get current history length
            history_length = readline.get_current_history_length()
            
            if history_length > 0:
                # If we have more than 100 commands, trim to last 100
                if history_length > 100:
                    # Remove oldest commands, keeping only last 100
                    for i in range(history_length - 100):
                        readline.remove_history_item(0)
                
                # Save the trimmed history
                readline.write_history_file(history_file)
                print(f" Saved {min(history_length, 100)} commands to history")
        except Exception as e:
            print(f"  Could not save command history: {e}")
            pass
    
    def _completer(self, text, state):
        """Auto-completion function for readline"""
        if readline is None:
            return None
            
        # Get all available commands (with error handling)
        try:
            available_commands = self.service_registry.list_available_commands()
        except:
            available_commands = []
        
        # Filter commands that start with the input text
        matches = [cmd for cmd in available_commands if cmd.startswith(text.lower())]
        
        # Add basic commands
        basic_commands = ['help', 'exit', 'quit', 'q', 'wait', 'refocus', 'history', 'save']
        matches.extend([cmd for cmd in basic_commands if cmd.startswith(text.lower())])
        
        # Remove duplicates and sort
        matches = sorted(list(set(matches)))
        
        if state < len(matches):
            return matches[state]
        else:
            return None
    
    def _focus_game(self):
        """Focus the game window"""
        print("Focusing game window...")
        success = self.window_manager.focus_game()
        if success:
            print(f"Game window focused: {self.window_manager.game_window_title}")
        else:
            print("Failed to focus game window")
        return success
    
    
    def _show_help(self):
        """Show available commands"""
        print("\nGame Command Help:")
        print("=" * 30)
        
        if self.service_registry.current_game:
            print(f"Current Game: {self.service_registry.current_game.title()}")
            commands = self.service_registry.list_available_commands()
            if commands:
                print(f"Commands Available: {len(commands)}")
                print("Sample commands:")
                
                # Show a few example commands from each category
                movement_cmds = [cmd for cmd in commands if any(word in cmd for word in ['walk', 'jog', 'run', 'sprint', 'jump', 'left', 'right', 'forward', 'backward'])]
                action_cmds = [cmd for cmd in commands if any(word in cmd for word in ['attack', 'dodge', 'web', 'swing', 'aim', 'shoot', 'venom', 'camouflage', 'heal'])]
                
                if movement_cmds:
                    print(f"  Movement: {', '.join(movement_cmds[:5])}{'...' if len(movement_cmds) > 5 else ''}")
                if action_cmds:
                    print(f"  Actions: {', '.join(action_cmds[:5])}{'...' if len(action_cmds) > 5 else ''}")
                
                if readline is not None:
                    print("   Use TAB for auto-completion, / for command history")
                else:
                    print("   Install pyreadline3 for auto-completion and history")
            else:
                print("No commands loaded")
        else:
            print("No game detected - load a game to see commands")
        
        print("\nSpecial Commands:")
        print("  help - Show this help")
        print("  refocus - Refocus game window")
        print("  history - Show command history stats")
        print("  save - Manually save command history")
        print("  exit/quit/q - Exit program")
        print()
    
    def _show_history_stats(self):
        """Show command history statistics"""
        if readline is None:
            print("  Command history not available (readline not installed)")
            return
            
        history_count = readline.get_current_history_length()
        history_file = os.path.join(os.path.expanduser("~"), ".game_command_history")
        
        print("\nCommand History Statistics:")
        print("=" * 30)
        print(f"Current session commands: {history_count}")
        print(f"History file: {history_file}")
        print(f"History limit: 100 commands")
        
        if os.path.exists(history_file):
            file_size = os.path.getsize(history_file)
            print(f"History file size: {file_size} bytes")
            print(" History will persist between sessions")
        else:
            print(" No history file yet - will be created on exit")
        
        print("\nNavigation:")
        print("  / arrows - Browse command history")
        print("  TAB - Auto-complete commands")
        print()
    
    def process_command(self, command: str) -> bool:
        """Process a single command"""
        command = command.lower().strip()
        
        # Handle special commands
        if command in ['help', 'commands', 'list']:
            self._show_help()
            return True
        elif command == 'refocus':
            return self._focus_game()
        elif command == 'history':
            self._show_history_stats()
            return True
        elif command == 'save':
            self._save_history()
            print(" Command history saved!")
            return True
        
        # Get command from registry
        command_func = self.service_registry.get_command(command)
        
        if command_func:
            try:
                # Check if game is available before executing command
                if not self.window_manager.game_window:
                    print(" No game detected. Please launch a game first.")
                    return False
                
                # Focus game before executing command
                if not self.window_manager.is_game_focused():
                    # Try focusing with retries for stubborn games
                    focus_attempts = 0
                    max_attempts = 3
                    
                    while focus_attempts < max_attempts:
                        focus_attempts += 1
                        print(f"Focus attempt {focus_attempts}/{max_attempts}...")
                        
                        if self.window_manager.focus_game():
                            break
                        
                        if focus_attempts < max_attempts:
                            print(f"Focus failed, waiting 1 second before retry...")
                            time.sleep(1.0)
                    else:
                        print("Failed to focus game after multiple attempts. Make sure it's running.")
                        return False
                    
                    time.sleep(0.5)  # Delay for game to recognize input
                
                # Execute command
                command_func()
                
                # Add command to history immediately
                if readline is not None:
                    readline.add_history(command)
                    self.history_save_counter += 1
                    
                    # Save history every 5 commands
                    if self.history_save_counter >= 5:
                        self._save_history()
                        self.history_save_counter = 0
                
                return True
            except Exception as e:
                print(f"Error executing command '{command}': {e}")
                return False
        else:
            print(f"Unknown command: {command}")
            print(f"Type 'help' to see available commands")
            return False
    
    def start_command_loop(self):
        """Start the command processing loop"""
        self.is_running = True
        
        # Check if game is already running
        if not self.window_manager.game_window:
            print("Game Command Processor")
            print("=" * 40)
            self.window_manager.wait_for_game()
        else:
            print("Game Command Processor")
            print("=" * 40)
            print(f"Game detected: {self.window_manager.game_window_title}")
        
        # Load commands for detected game
        if self.window_manager.game_window_title:
            self.service_registry.detect_and_load_game(self.window_manager.game_window_title)
        
        print("Command processor started. Type commands or 'exit' to quit.")
        print("Type 'help' for available commands")
        if readline is not None:
            print(" Features: Tab completion, Command history (/ arrows), History saved between sessions")
        else:
            print(" Install pyreadline3 for enhanced features: pip install pyreadline3")
        
        # Give the game window a moment to stabilize
        print(" Waiting for game window to stabilize...")
        time.sleep(2.0)
        
        while self.is_running:
            try:
                command = input("Game> ").strip()
                
                if command.lower() in ['exit', 'quit', 'q']:
                    print(" Goodbye!")
                    # Save history before exiting
                    if readline is not None:
                        self._save_history()
                    break
                elif command.lower() == 'help':
                    self._show_help()
                elif command.lower() == 'wait':
                    print(" No game detected. Waiting for a game to be launched...")
                    print(" Checking for games every 3 seconds...")
                    self.window_manager.wait_for_game()
                    # Load commands for newly detected game
                    if self.window_manager.game_window_title:
                        self.service_registry.detect_and_load_game(self.window_manager.game_window_title)
                elif command:
                    self.process_command(command)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        self.is_running = False

def main():
    """Main function"""
    print("Game Command Processor")
    print("=" * 40)
    
    try:
        processor = GameCommandProcessor()
        processor.start_command_loop()
    except Exception as e:
        print(f"Failed to start command processor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
