"""
Test script for the new chick command
Tests the attack_chicken functionality
"""

import sys
import os
import time

# Add the current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from runescape_commands import RuneScapeCommands

def test_chick_command():
    """Test the chick command functionality"""
    print("🐔 Testing Chick Command")
    print("=" * 50)
    
    try:
        # Initialize RuneScape commands
        rs = RuneScapeCommands()
        
        print("✅ RuneScape commands initialized")
        print("🎯 Starting chicken attack test...")
        print("💡 Make sure RuneScape is running and you're near chickens!")
        print()
        
        # Test the chick command
        success = rs.attack_chicken()
        
        if success:
            print("🎉 Chick command test completed successfully!")
            print("⚔️ Combat should have started")
        else:
            print("❌ Chick command test failed")
            print("💡 Make sure:")
            print("   - RuneScape is running and visible")
            print("   - You're in an area with chickens")
            print("   - Your chicken detection model is working")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chick_with_scan():
    """Test chick command with area scanning"""
    print("\n🔍 Testing Chick Command with Area Scanning")
    print("=" * 50)
    
    try:
        rs = RuneScapeCommands()
        
        # First scan for chickens
        print("🔍 Scanning area for chickens...")
        detections = rs.scan_objects()
        chicken_detections = [d for d in detections if d['category'] == 'chicken']
        
        print(f"📍 Found {len(chicken_detections)} chickens in area")
        
        if chicken_detections:
            print("✅ Chickens detected, proceeding with attack...")
            success = rs.attack_chicken()
            return success
        else:
            print("❌ No chickens found in area")
            print("💡 Try moving to a chicken area (like Lumbridge)")
            return False
            
    except Exception as e:
        print(f"❌ Scan test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🐔 RuneScape Chick Command Test Suite")
    print("=" * 60)
    print("This script tests the new 'chick' command functionality")
    print("Make sure RuneScape is running and visible before starting tests!")
    print()
    
    print("Available tests:")
    print("1. Basic chick command test")
    print("2. Chick command with area scanning")
    print("3. Run all tests")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nSelect test to run (1-4): ").strip()
            
            if choice == '1':
                test_chick_command()
            elif choice == '2':
                test_chick_with_scan()
            elif choice == '3':
                print("\n🚀 Running all tests...")
                test_chick_command()
                time.sleep(2)
                test_chick_with_scan()
                print("\n✅ All tests completed!")
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Test interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
