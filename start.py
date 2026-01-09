#!/usr/bin/env python3
"""
Quick start script for E-Commerce application
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 E-Commerce Quick Start")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ app.py not found!")
        print("Make sure you're in the project directory.")
        return
    
    print("Choose which version to run:")
    print("1. Simple App (guaranteed to work with CSS)")
    print("2. Full App (with database features)")
    print("3. Test App (for debugging)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        print("\n🎯 Starting Simple App...")
        print("This version has embedded CSS and will definitely work!")
        os.system('python simple_app.py')
    elif choice == '2':
        print("\n🎯 Starting Full App...")
        print("Make sure XAMPP is running and database is set up!")
        os.system('python app.py')
    elif choice == '3':
        print("\n🎯 Starting Test App...")
        print("This is for debugging CSS and template issues.")
        os.system('python test_app.py')
    else:
        print("❌ Invalid choice!")
        return

if __name__ == '__main__':
    main()