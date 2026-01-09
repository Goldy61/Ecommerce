#!/usr/bin/env python3
"""
Test database connection
"""

from models.database import get_db_connection, execute_query

def test_database():
    print("🔍 Testing Database Connection...")
    
    # Test basic connection
    try:
        connection = get_db_connection()
        if connection:
            print("✅ Database connection successful!")
            connection.close()
        else:
            print("❌ Database connection failed!")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False
    
    # Test query execution
    try:
        result = execute_query("SELECT 1 as test", fetch=True)
        if result:
            print("✅ Database query execution successful!")
        else:
            print("❌ Database query execution failed!")
            return False
    except Exception as e:
        print(f"❌ Database query error: {e}")
        return False
    
    # Test if tables exist
    try:
        tables = ['users', 'products', 'categories', 'orders', 'cart', 'admins', 'order_items']
        for table in tables:
            result = execute_query(f"SHOW TABLES LIKE '{table}'", fetch=True)
            if result:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
    except Exception as e:
        print(f"❌ Table check error: {e}")
        return False
    
    print("\n🎉 Database test completed!")
    return True

if __name__ == "__main__":
    test_database()