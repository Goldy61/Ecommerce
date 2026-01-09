#!/usr/bin/env python3
"""
Fix admin login by updating password hashes in the database
This script will create proper password hashes and update the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from models.database import execute_query

def fix_admin_passwords():
    """Fix admin and user password hashes in the database"""
    print("🔧 Fixing Admin Login Issue")
    print("=" * 50)
    
    # Generate password hashes
    admin_password = "admin123"
    user_password = "user123"
    
    admin_hash = generate_password_hash(admin_password)
    user_hash = generate_password_hash(user_password)
    
    print(f"Generated admin hash: {admin_hash[:50]}...")
    print(f"Generated user hash: {user_hash[:50]}...")
    
    try:
        # Update admin password
        print("\n1. Updating admin password...")
        admin_query = "UPDATE admins SET password_hash = %s WHERE username = 'admin'"
        admin_result = execute_query(admin_query, (admin_hash,))
        
        if admin_result:
            print("✅ Admin password updated successfully")
        else:
            print("❌ Failed to update admin password")
            
        # Update sample user passwords
        print("\n2. Updating sample user passwords...")
        user_query = "UPDATE users SET password_hash = %s WHERE username IN ('john_doe', 'jane_smith')"
        user_result = execute_query(user_query, (user_hash,))
        
        if user_result:
            print("✅ Sample user passwords updated successfully")
        else:
            print("❌ Failed to update user passwords")
            
        # Verify admin exists
        print("\n3. Verifying admin account...")
        check_query = "SELECT username, full_name FROM admins WHERE username = 'admin'"
        check_result = execute_query(check_query, fetch=True)
        
        if check_result:
            admin_data = check_result[0] if isinstance(check_result, list) else check_result
            print(f"✅ Admin account found: {admin_data['username']} ({admin_data['full_name']})")
        else:
            print("❌ Admin account not found! Creating new admin...")
            create_admin()
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Admin Login Fix Complete!")
    print("=" * 50)
    print("You can now login to admin panel with:")
    print("  URL: http://localhost:5000/admin/login")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 50)
    
    return True

def create_admin():
    """Create a new admin account if it doesn't exist"""
    admin_password = "admin123"
    admin_hash = generate_password_hash(admin_password)
    
    create_query = """
    INSERT INTO admins (username, email, password_hash, full_name) 
    VALUES ('admin', 'admin@ecommerce.com', %s, 'System Administrator')
    """
    
    result = execute_query(create_query, (admin_hash,))
    
    if result:
        print("✅ New admin account created successfully")
    else:
        print("❌ Failed to create admin account")

def check_admin_table():
    """Check if admin table exists and has data"""
    print("🔍 Checking admin table...")
    
    try:
        # Check if table exists
        table_query = "SHOW TABLES LIKE 'admins'"
        table_result = execute_query(table_query, fetch=True)
        
        if not table_result:
            print("❌ Admins table does not exist!")
            print("Please run the database schema first:")
            print("  mysql -u root -p ecommerce_db < database/schema.sql")
            return False
        
        # Check admin data
        admin_query = "SELECT * FROM admins"
        admin_result = execute_query(admin_query, fetch=True)
        
        if admin_result:
            print(f"✅ Found {len(admin_result)} admin(s) in database")
            for admin in admin_result:
                print(f"  - {admin['username']} ({admin['full_name']})")
        else:
            print("⚠️ No admin accounts found in database")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking admin table: {e}")
        return False

def test_admin_login():
    """Test admin login functionality"""
    print("\n🧪 Testing admin login...")
    
    try:
        from werkzeug.security import check_password_hash
        
        # Get admin from database
        query = "SELECT * FROM admins WHERE username = 'admin'"
        result = execute_query(query, fetch=True)
        
        if result:
            admin_data = result[0] if isinstance(result, list) else result
            
            # Test password
            if check_password_hash(admin_data['password_hash'], 'admin123'):
                print("✅ Admin login test successful!")
                return True
            else:
                print("❌ Admin password verification failed!")
                return False
        else:
            print("❌ Admin account not found!")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Admin Login Fix Script")
    print("Make sure your database is running and the schema is loaded")
    print()
    
    try:
        # Step 1: Check admin table
        if not check_admin_table():
            print("\n💡 Please ensure:")
            print("1. MySQL/XAMPP is running")
            print("2. Database 'ecommerce_db' exists")
            print("3. Schema has been loaded: mysql -u root -p ecommerce_db < database/schema.sql")
            print("4. Sample data has been loaded: mysql -u root -p ecommerce_db < database/sample_data.sql")
            sys.exit(1)
        
        # Step 2: Fix passwords
        if fix_admin_passwords():
            # Step 3: Test login
            if test_admin_login():
                print("\n🎉 Everything is working! You can now login to admin panel.")
            else:
                print("\n❌ Login test failed. Please check the database manually.")
        else:
            print("\n❌ Failed to fix passwords. Please check database connection.")
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()