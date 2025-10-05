#!/usr/bin/env python3
"""
Test script to verify RuneScape detection works with the command processor
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_runescape_detection():
    """Test RuneScape detection in the command processor"""
    print("🧪 Testing RuneScape Detection")
    print("=" * 40)
    
    try:
        # Import the command processor components
        from command_processor import GameServiceRegistry, GameWindowManager
        
        # Test 1: Window Manager Detection
        print("\n📋 Test 1: Window Manager Game Detection")
        window_manager = GameWindowManager()
        
        if window_manager.game_window:
            print(f"✅ Game detected: {window_manager.game_window_title}")
            
            # Check if RuneScape is detected
            if window_manager.game_window_title:
                title_lower = window_manager.game_window_title.lower()
                if any(keyword in title_lower for keyword in ['runescape', 'osrs', 'old school runescape']):
                    print("✅ RuneScape detected by window manager!")
                else:
                    print(f"⚠️ Game detected but not RuneScape: {window_manager.game_window_title}")
            else:
                print("❌ No game title found")
        else:
            print("❌ No game detected by window manager")
            print("💡 Launch RuneScape to test detection")
        
        # Test 2: Service Registry Game Detection
        print("\n📋 Test 2: Service Registry Game Detection")
        service_registry = GameServiceRegistry(None)  # No gamepad needed
        
        # Test RuneScape titles
        test_titles = [
            "Old School RuneScape",
            "RuneScape",
            "OSRS",
            "Old School RuneScape - Chrome",
            "RuneScape - Firefox"
        ]
        
        print("Testing RuneScape title detection:")
        for title in test_titles:
            success = service_registry.detect_and_load_game(title)
            if success:
                print(f"✅ '{title}' -> {service_registry.current_game}")
                if service_registry.current_game in ['runescape', 'osrs', 'old school runescape']:
                    print(f"   ✅ Correctly identified as RuneScape!")
                    print(f"   📋 Loaded {len(service_registry.current_commands)} commands")
                else:
                    print(f"   ❌ Incorrectly identified as: {service_registry.current_game}")
            else:
                print(f"❌ '{title}' -> Failed to detect")
        
        # Test 3: Command Loading
        print("\n📋 Test 3: RuneScape Command Loading")
        if service_registry.current_game in ['runescape', 'osrs', 'old school runescape']:
            commands = service_registry.list_available_commands()
            print(f"✅ Available commands: {len(commands)}")
            
            # Show some key commands
            key_commands = ['chop tree', 'chop oak', 'auto woodcut', 'mine rock', 'scan objects']
            print("Key commands available:")
            for cmd in key_commands:
                if cmd in commands:
                    print(f"   ✅ {cmd}")
                else:
                    print(f"   ❌ {cmd} - Missing!")
        else:
            print("❌ No RuneScape commands loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_window_enumeration():
    """Test window enumeration to see what games are detected"""
    print("\n🧪 Testing Window Enumeration")
    print("=" * 40)
    
    try:
        from command_processor import GameWindowManager
        
        window_manager = GameWindowManager()
        all_games = window_manager.list_all_game_windows()
        
        if all_games:
            print(f"✅ Found {len(all_games)} game windows:")
            for i, (hwnd, title) in enumerate(all_games, 1):
                print(f"   {i}. {title}")
                
                # Check if it's RuneScape
                if any(keyword in title.lower() for keyword in ['runescape', 'osrs', 'old school runescape']):
                    print(f"      🎯 This is RuneScape!")
        else:
            print("❌ No game windows detected")
            print("💡 Make sure RuneScape is running and visible")
        
        return True
        
    except Exception as e:
        print(f"❌ Window enumeration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🌳 RuneScape Detection Test Suite")
    print("=" * 50)
    print("This script tests if RuneScape is properly detected")
    print("Make sure RuneScape is running before running tests!")
    print()
    
    # Run tests
    success1 = test_runescape_detection()
    success2 = test_window_enumeration()
    
    print("\n📊 Test Results:")
    print("=" * 30)
    print(f"RuneScape Detection: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Window Enumeration: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! RuneScape detection is working correctly.")
        print("💡 You can now run the command processor and it should detect RuneScape.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        print("💡 Make sure RuneScape is running and visible on your screen.")

if __name__ == "__main__":
    main()
