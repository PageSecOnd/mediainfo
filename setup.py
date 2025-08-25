#!/usr/bin/env python3
"""
Setup script for MediaInfo Viewer
"""

import os
import sys
import subprocess
import platform

def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_context_menu():
    """Setup context menu integration based on platform"""
    system = platform.system().lower()
    
    if system == "windows":
        print("\n📋 To add context menu integration on Windows:")
        print("1. Run 'install_context_menu_windows.bat' as Administrator")
        print("2. Or manually run the batch file from an elevated command prompt")
        
    elif system == "linux":
        print("\n📋 Setting up context menu integration on Linux...")
        try:
            subprocess.check_call(["bash", "install_context_menu_linux.sh"])
            print("✅ Context menu integration setup completed!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup context menu: {e}")
            print("You can manually run: bash install_context_menu_linux.sh")
            
    elif system == "darwin":  # macOS
        print("\n📋 For macOS context menu integration:")
        print("1. You can create an Automator service")
        print("2. Or use the application directly from Finder")
        
    else:
        print(f"\n⚠️  Platform '{system}' not specifically supported for context menu integration")

def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    try:
        import customtkinter
        import pymediainfo
        from PIL import Image
        print("✅ All required modules can be imported!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🎬 MediaInfo Viewer Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation!")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n❌ Setup failed during testing!")
        sys.exit(1)
    
    # Setup context menu
    setup_context_menu()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Usage:")
    print("1. Run: python mediainfo_viewer.py")
    print("2. Or double-click on mediainfo_viewer.py")
    print("3. Or right-click on media files (if context menu is installed)")
    
    # Ask if user wants to launch the application
    try:
        launch = input("\n🚀 Would you like to launch the application now? (y/n): ").lower().strip()
        if launch in ['y', 'yes']:
            print("Launching MediaInfo Viewer...")
            subprocess.Popen([sys.executable, "mediainfo_viewer.py"])
    except KeyboardInterrupt:
        print("\nSetup completed.")

if __name__ == "__main__":
    main()