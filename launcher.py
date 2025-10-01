#!/usr/bin/env python3
"""
Cash Up Application Launcher
Choose between web interface, desktop GUI, or command line
"""
import sys
import os
import subprocess
from pathlib import Path

def show_menu():
    print("=" * 50)
    print("    CASH UP APPLICATION LAUNCHER")
    print("=" * 50)
    print()
    print("Choose your preferred interface:")
    print()
    
    # Check what's available
    web_available = True
    desktop_available = True
    
    try:
        import flask
    except ImportError:
        web_available = False
    
    try:
        import tkinter
    except ImportError:
        desktop_available = False
    
    if web_available:
        print("1. Web Interface (Flask)")
        print("   - Modern web-based interface")
        print("   - Accessible from any device on your network")
        print("   - Requires internet browser")
        print()
    else:
        print("1. Web Interface (Flask) - NOT AVAILABLE")
        print("   - Install Flask: pip install flask")
        print()
    
    if desktop_available:
        print("2. Desktop GUI (Tkinter)")
        print("   - Native desktop application")
        print("   - Works offline")
        print("   - Traditional desktop interface")
        print()
    else:
        print("2. Desktop GUI (Tkinter) - NOT AVAILABLE")
        print("   - Install tkinter for your system")
        print()
    
    print("3. Command Line Interface")
    print("   - Original terminal-based interface")
    print("   - Works offline")
    print("   - Fast and lightweight")
    print()
    print("4. Exit")
    print()

def launch_web():
    """Launch the Flask web application"""
    try:
        import flask
    except ImportError:
        print("Flask is not available. Please install it first:")
        print("pip install flask")
        return
    
    print("Starting web interface...")
    print("The application will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    print()
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nWeb server stopped.")
    except Exception as e:
        print(f"Error starting web interface: {e}")

def launch_desktop():
    """Launch the desktop GUI application"""
    try:
        import tkinter
    except ImportError:
        print("Tkinter is not available. Desktop GUI cannot be launched.")
        print("Please install tkinter for your system.")
        return
    
    print("Starting desktop application...")
    try:
        subprocess.run([sys.executable, "desktop_app.py"], check=True)
    except Exception as e:
        print(f"Error starting desktop application: {e}")

def launch_cli():
    """Launch the command line interface"""
    print("Starting command line interface...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except Exception as e:
        print(f"Error starting command line interface: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import flask
    except ImportError:
        missing_deps.append("flask")
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter (desktop GUI will not be available)")
    
    if missing_deps:
        print("Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        if "flask" in missing_deps:
            print("Please install requirements: pip install -r requirements.txt")
            return False
        else:
            print("Web interface will work, but desktop GUI may not be available.")
    
    return True

def main():
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("Error: Please run this script from the cash_up directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            launch_web()
        elif choice == "2":
            launch_desktop()
        elif choice == "3":
            launch_cli()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            input("Press Enter to continue...")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
