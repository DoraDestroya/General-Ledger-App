import os
import subprocess
import sys

def build_windows_exe():
    print("Building Windows executable...")
    
    # Ensure we're using Python 3
    if sys.version_info[0] < 3:
        print("Error: Python 3 is required")
        sys.exit(1)
    
    # Install required packages
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "pillow"])
    
    # Create the icon
    subprocess.run([sys.executable, "app_icon.py"])
    
    # Build the executable
    subprocess.run([sys.executable, "-m", "PyInstaller", "general_ledger.spec"])
    
    print("\nBuild completed!")
    print("The Windows executable can be found in the 'dist' directory.")

if __name__ == "__main__":
    build_windows_exe() 