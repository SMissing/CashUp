#!/usr/bin/env python3
"""
Setup script for Cash Up Application
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["Reports", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Directory created: {directory}")

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError:
        print("✗ Flask import failed")
        return False
    
    try:
        import tkinter
        print("✓ Tkinter imported successfully")
    except ImportError:
        print("✗ Tkinter import failed (desktop GUI may not work)")
    
    try:
        from cash_up_core import CashUpCalculator
        print("✓ Core modules imported successfully")
    except ImportError as e:
        print(f"✗ Core module import failed: {e}")
        return False
    
    return True

def main():
    print("=" * 50)
    print("    CASH UP APPLICATION SETUP")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed. Please install dependencies manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Test imports
    if not test_imports():
        print("Setup completed with warnings. Some features may not work.")
    else:
        print("✓ Setup completed successfully!")
    
    print()
    print("You can now run the application with:")
    print("  python launcher.py")
    print()
    print("Or run individual interfaces:")
    print("  python app.py          # Web interface")
    print("  python desktop_app.py  # Desktop GUI")
    print("  python main.py         # Command line")

if __name__ == "__main__":
    main()
