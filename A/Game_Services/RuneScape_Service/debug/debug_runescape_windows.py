#!/usr/bin/env python3
"""
Debug script to see what window titles RuneScape is actually using
"""

import win32gui
import win32con
import win32api

def list_all_windows():
    """List all visible windows to see what RuneScape titles are available"""
    print("🔍 Scanning all visible windows for RuneScape...")
    print("=" * 60)
    
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title:  # Only show windows with titles
                windows.append((hwnd, window_title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    
    # Filter for RuneScape-related windows
    runescape_windows = []
    for hwnd, title in windows:
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in ['runescape', 'osrs', 'old school']):
            runescape_windows.append((hwnd, title))
    
    print(f"📊 Found {len(windows)} total visible windows")
    print(f"🎯 Found {len(runescape_windows)} RuneScape-related windows:")
    print()
    
    if runescape_windows:
        for i, (hwnd, title) in enumerate(runescape_windows, 1):
            print(f"{i}. '{title}'")
            
            # Check if it matches our detection criteria
            matches = []
            detection_terms = [
                'runescape', 'osrs', 'old school runescape',
                'old school runescape client', 'runescape client'
            ]
            
            for term in detection_terms:
                if term in title.lower():
                    matches.append(term)
            
            if matches:
                print(f"   ✅ Matches detection terms: {matches}")
            else:
                print(f"   ❌ No detection terms match")
            
            # Show window properties
            try:
                rect = win32gui.GetWindowRect(hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                print(f"   📐 Size: {width}x{height}")
                print(f"   🆔 Handle: {hwnd}")
            except:
                print(f"   ❌ Could not get window properties")
            print()
    else:
        print("❌ No RuneScape windows found!")
        print("💡 Make sure RuneScape is running and visible")
        
        # Show all windows for debugging
        print("\n📋 All visible windows (first 20):")
        for i, (hwnd, title) in enumerate(windows[:20], 1):
            print(f"   {i}. '{title}'")
        if len(windows) > 20:
            print(f"   ... and {len(windows) - 20} more windows")

def test_detection_logic():
    """Test our current detection logic"""
    print("\n🧪 Testing Detection Logic")
    print("=" * 40)
    
    # Test titles we expect to see
    test_titles = [
        "Old School RuneScape Client",
        "Old School RuneScape", 
        "RuneScape Client",
        "RuneScape",
        "OSRS",
        "Old School RuneScape - Chrome",
        "Old School RuneScape - Firefox"
    ]
    
    detection_terms = [
        'runescape', 'osrs', 'old school runescape',
        'old school runescape client', 'runescape client'
    ]
    
    print("Testing detection terms against expected titles:")
    for title in test_titles:
        title_lower = title.lower()
        matches = [term for term in detection_terms if term in title_lower]
        
        if matches:
            print(f"✅ '{title}' -> Matches: {matches}")
        else:
            print(f"❌ '{title}' -> No matches")

def main():
    """Main debug function"""
    print("🌳 RuneScape Window Detection Debug")
    print("=" * 50)
    print("This script will show what window titles RuneScape is using")
    print("and test our detection logic against them.")
    print()
    
    list_all_windows()
    test_detection_logic()
    
    print("\n💡 If RuneScape is not detected:")
    print("1. Make sure RuneScape is running and visible")
    print("2. Check if the window title matches our detection terms")
    print("3. If not, we may need to add more detection terms")

if __name__ == "__main__":
    main()
