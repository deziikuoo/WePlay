#!/usr/bin/env python3
"""
GTA5 VgamePad Setup Script
This script helps set up the vgamepad environment for GTA5 automation.
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_os():
    """Check if operating system is Windows"""
    if platform.system() != "Windows":
        print("❌ This script requires Windows (for ViGEm driver)")
        return False
    print(f"✅ Operating System: {platform.system()} {platform.release()}")
    return True

def install_requirements():
    """Install required Python packages"""
    print("\n📦 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_vgamepad():
    """Check if vgamepad can be imported"""
    print("\n🔍 Checking vgamepad installation...")
    try:
        import vgamepad as vg
        print("✅ VgamePad library imported successfully")
        return True
    except ImportError as e:
        print(f"❌ VgamePad import failed: {e}")
        return False

def test_controller_creation():
    """Test if virtual controller can be created"""
    print("\n🎮 Testing controller creation...")
    try:
        import vgamepad as vg
        gamepad = vg.VX360Gamepad()
        print("✅ Virtual Xbox controller created successfully")
        return True
    except Exception as e:
        print(f"❌ Controller creation failed: {e}")
        print("💡 Make sure ViGEm driver is installed and running")
        return False

def check_vigem_driver():
    """Check if ViGEm driver is installed"""
    print("\n🔍 Checking ViGEm driver...")
    
    # Check if ViGEm driver files exist
    vigem_paths = [
        r"C:\Program Files\ViGEm\ViGEmBus.inf",
        r"C:\Windows\System32\drivers\ViGEmBus.sys",
        r"C:\Windows\System32\ViGEmClient.dll"
    ]
    
    found_files = []
    for path in vigem_paths:
        if os.path.exists(path):
            found_files.append(path)
    
    if found_files:
        print("✅ ViGEm driver files found:")
        for file in found_files:
            print(f"   - {file}")
        return True
    else:
        print("❌ ViGEm driver not found")
        print("💡 Please install ViGEm driver from: https://github.com/ViGEm/ViGEmBus/releases")
        return False

def run_forward_movement_test():
    """Run the forward movement test"""
    print("\n🧪 Running forward movement test...")
    try:
        # Import and test the forward movement script
        sys.path.append(os.path.join(os.path.dirname(__file__), "Player_Basic_Movement"))
        from forward_movement import GTA5ForwardMovement
        
        controller = GTA5ForwardMovement()
        print("✅ Forward movement controller initialized successfully")
        
        # Test basic movement
        print("🎯 Testing basic forward movement...")
        controller.walk_forward(duration=0.5, speed=0.5)
        controller.stop()
        print("✅ Basic movement test completed")
        
        return True
    except Exception as e:
        print(f"❌ Forward movement test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🎮 GTA5 VgamePad Setup Script")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    if not check_os():
        return False
    
    # Check ViGEm driver
    vigem_ok = check_vigem_driver()
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check vgamepad
    if not check_vgamepad():
        return False
    
    # Test controller creation
    if not test_controller_creation():
        if not vigem_ok:
            print("\n💡 ViGEm driver installation required:")
            print("   1. Download from: https://github.com/ViGEm/ViGEmBus/releases")
            print("   2. Install ViGEmBus setup.exe")
            print("   3. Restart your computer")
            print("   4. Run this setup script again")
        return False
    
    # Run forward movement test
    if not run_forward_movement_test():
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("✅ VgamePad is ready for GTA5 automation")
    print("✅ Forward movement script is working")
    print("✅ Virtual Xbox controller is functional")
    print("\n🚀 Next steps:")
    print("   1. Launch GTA5")
    print("   2. Run: python Player_Basic_Movement/forward_movement.py")
    print("   3. Test movement commands in-game")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
