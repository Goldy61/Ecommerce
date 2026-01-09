#!/usr/bin/env python3
"""
Quick fix for admin login - generates and displays the exact SQL commands needed
"""

from werkzeug.security import generate_password_hash

def generate_admin_fix():
    """Generate the exact SQL commands to fix admin login"""
    print("🔧 Quick Admin Login Fix")
    print("=" * 50)
    
    # Generate password hash for admin123
    admin_password = "admin123"
    admin_hash = generate_password_hash(admin_password)
    
    print(f"Generated password hash for 'admin123':")
    print(f"{admin_hash}")
    print()
    
    print("📋 COPY AND RUN THESE SQL COMMANDS IN PHPMYADMIN:")
    print("=" * 50)
    print()
    
    # SQL commands to fix the issue
    print("-- Step 1: Update admin password")
    print(f"UPDATE admins SET password_hash = '{admin_hash}' WHERE username = 'admin';")
    print()
    
    print("-- Step 2: Verify admin exists")
    print("SELECT username, full_name FROM admins WHERE username = 'admin';")
    print()
    
    print("-- Step 3: If no admin found, create one")
    print(f"INSERT INTO admins (username, email, password_hash, full_name) VALUES")
    print(f"('admin', 'admin@ecommerce.com', '{admin_hash}', 'System Administrator');")
    print()
    
    print("=" * 50)
    print("📝 INSTRUCTIONS:")
    print("=" * 50)
    print("1. Open phpMyAdmin: http://localhost/phpmyadmin")
    print("2. Select database: ecommerce_db")
    print("3. Go to SQL tab")
    print("4. Copy and paste the UPDATE command above")
    print("5. Click 'Go' to execute")
    print("6. Try admin login again with:")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 50)

if __name__ == "__main__":
    generate_admin_fix()