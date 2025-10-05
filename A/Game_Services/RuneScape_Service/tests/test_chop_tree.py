#!/usr/bin/env python3
"""
Test script for enhanced RuneScape chop tree functionality
Demonstrates the improved chop_tree command with various scenarios
"""

import sys
import os
import time

# Add the current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from runescape_commands import RuneScapeCommands


def test_basic_chop_tree():
    """Test basic tree chopping functionality"""
    print("🧪 Testing basic chop tree functionality...")
    print("=" * 50)
    
    try:
        # Initialize RuneScape commands
        rs = RuneScapeCommands()
        
        # Test 1: Basic tree chopping
        print("\n📋 Test 1: Basic tree chopping")
        success = rs.chop_tree()
        print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        
        # Test 2: Specific tree type chopping
        print("\n📋 Test 2: Oak tree chopping")
        success = rs.chop_specific_tree("oak")
        print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        
        # Test 3: Willow tree chopping
        print("\n📋 Test 3: Willow tree chopping")
        success = rs.chop_specific_tree("willow")
        print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def test_auto_woodcutting():
    """Test automated woodcutting functionality"""
    print("\n🧪 Testing auto-woodcutting functionality...")
    print("=" * 50)
    
    try:
        rs = RuneScapeCommands()
        
        # Test short auto-woodcutting session (1 minute for testing)
        print("\n📋 Test: Short auto-woodcutting session (1 minute)")
        print("⚠️ Note: This will run for 1 minute with enhanced features")
        
        # Ask user if they want to run this test
        response = input("Run auto-woodcutting test? (y/n): ").lower().strip()
        if response == 'y':
            success = rs.auto_woodcutting(
                tree_type="tree",
                duration_minutes=1,  # Short test
                inventory_check=True,
                tree_rotation=True
            )
            print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        else:
            print("⏭️ Skipped auto-woodcutting test")
        
        return True
        
    except Exception as e:
        print(f"❌ Auto-woodcutting test failed: {e}")
        return False


def test_object_detection():
    """Test object detection and scanning"""
    print("\n🧪 Testing object detection...")
    print("=" * 50)
    
    try:
        rs = RuneScapeCommands()
        
        # Test object scanning
        print("\n📋 Test: Object scanning")
        detections = rs.scan_objects(save_debug=True)
        print(f"Found {len(detections)} objects")
        
        # Show breakdown by category
        categories = {}
        for detection in detections:
            category = detection['category']
            categories[category] = categories.get(category, 0) + 1
        
        print("Object breakdown:")
        for category, count in categories.items():
            print(f"  {category}: {count} objects")
        
        return True
        
    except Exception as e:
        print(f"❌ Object detection test failed: {e}")
        return False


def demonstrate_chop_tree_scenarios():
    """Demonstrate various chop tree scenarios based on the RuneScape screenshot"""
    print("\n🎮 Demonstrating chop tree scenarios...")
    print("=" * 50)
    
    print("Based on your RuneScape screenshot, here are the scenarios we can handle:")
    print()
    
    scenarios = [
        {
            "name": "Beginner Tree Chopping",
            "description": "Chop regular trees near the starting area",
            "command": "chop tree",
            "features": ["Axe validation", "Multiple attempts", "Human-like timing"]
        },
        {
            "name": "Specific Tree Types", 
            "description": "Target specific tree types (oak, willow, etc.)",
            "command": "chop oak",
            "features": ["Tree type detection", "Fallback options", "Smart retry logic"]
        },
        {
            "name": "Automated Woodcutting",
            "description": "Long-term automated woodcutting with inventory management",
            "command": "auto woodcut 10",
            "features": ["Inventory management", "Tree rotation", "Failure recovery"]
        },
        {
            "name": "Area Scanning",
            "description": "Scan area for available trees and objects",
            "command": "scan objects",
            "features": ["YOLO detection", "Debug visualization", "Object categorization"]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Command: {scenario['command']}")
        print(f"   Features: {', '.join(scenario['features'])}")
        print()


def main():
    """Main test function"""
    print("🌳 RuneScape Enhanced Chop Tree Test Suite")
    print("=" * 60)
    print("This script tests the enhanced chop tree functionality")
    print("Make sure RuneScape is running and visible before starting tests!")
    print()
    
    # Show scenarios first
    demonstrate_chop_tree_scenarios()
    
    # Ask user which tests to run
    print("Available tests:")
    print("1. Basic chop tree functionality")
    print("2. Auto-woodcutting functionality") 
    print("3. Object detection and scanning")
    print("4. Run all tests")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nSelect test to run (1-5): ").strip()
            
            if choice == '1':
                test_basic_chop_tree()
            elif choice == '2':
                test_auto_woodcutting()
            elif choice == '3':
                test_object_detection()
            elif choice == '4':
                print("\n🚀 Running all tests...")
                test_basic_chop_tree()
                test_object_detection()
                test_auto_woodcutting()
                print("\n✅ All tests completed!")
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Test interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
