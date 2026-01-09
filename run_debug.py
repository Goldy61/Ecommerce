#!/usr/bin/env python3
"""
Debug script to help troubleshoot the E-Commerce application
"""

import os
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files exist"""
    print("🔍 Checking file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'static/css/style.css',
        'static/js/main.js',
        'templates/base.html',
        'templates/index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found!")
    return True

def check_static_folder():
    """Check static folder structure"""
    print("\n🔍 Checking static folder...")
    
    static_path = Path('static')
    if not static_path.exists():
        print("❌ static/ folder not found!")
        return False
    
    css_path = static_path / 'css' / 'style.css'
    js_path = static_path / 'js' / 'main.js'
    
    if css_path.exists():
        size = css_path.stat().st_size
        print(f"✅ style.css found ({size} bytes)")
    else:
        print("❌ style.css not found!")
        return False
    
    if js_path.exists():
        size = js_path.stat().st_size
        print(f"✅ main.js found ({size} bytes)")
    else:
        print("❌ main.js not found!")
        return False
    
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = [
        'flask',
        'mysql-connector-python',
        'werkzeug'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_flask_import():
    """Test if Flask app can be imported"""
    print("\n🔍 Testing Flask app import...")
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test if static folder is configured
        print(f"✅ Static folder: {app.static_folder}")
        print(f"✅ Static URL path: {app.static_url_path}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to import Flask app: {e}")
        return False

def main():
    """Main debug function"""
    print("🚀 E-Commerce Debug Tool")
    print("=" * 50)
    
    # Check current directory
    print(f"📁 Current directory: {os.getcwd()}")
    
    # Run all checks
    checks = [
        check_file_structure(),
        check_static_folder(),
        check_dependencies(),
        test_flask_import()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 All checks passed!")
        print("\n📋 Next steps:")
        print("1. Make sure XAMPP is running (Apache + MySQL)")
        print("2. Create database using: database/schema.sql")
        print("3. Run: python app.py")
        print("4. Visit: http://localhost:5000/test")
        print("5. Visit: http://localhost:5000/debug")
        print("6. Check browser developer tools (F12) for CSS errors")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    
    print("\n🔧 Troubleshooting tips:")
    print("- If CSS doesn't load, check browser developer tools (F12)")
    print("- Look for 404 errors in the Network tab")
    print("- Make sure Flask is running in debug mode")
    print("- Try clearing browser cache (Ctrl+F5)")

if __name__ == "__main__":
    main()