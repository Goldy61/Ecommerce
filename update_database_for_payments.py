#!/usr/bin/env python3
"""
Update database schema for Razorpay payment system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import execute_query

def update_database_for_payments():
    """Add payment-related tables and columns to database"""
    print("🔧 Updating Database Schema for Razorpay Payments")
    print("=" * 60)
    
    try:
        # Read and execute the payment schema SQL
        print("1. Reading payment schema SQL file...")
        
        with open('database/razorpay_payment_schema.sql', 'r') as file:
            sql_content = file.read()
        
        # Split SQL commands (simple approach)
        sql_commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        print(f"✅ Found {len(sql_commands)} SQL commands to execute")
        
        # Execute each SQL command
        print("\n2. Executing SQL commands...")
        
        success_count = 0
        for i, command in enumerate(sql_commands, 1):
            try:
                if command.upper().startswith(('CREATE', 'ALTER', 'INSERT', 'UPDATE')):
                    execute_query(command)
                    print(f"✅ Command {i}: {command[:50]}...")
                    success_count += 1
                else:
                    print(f"⚠️  Skipped {i}: {command[:50]}...")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                    print(f"⚠️  Command {i}: Already exists - {command[:50]}...")
                    success_count += 1
                else:
                    print(f"❌ Command {i} failed: {e}")
        
        print(f"\n✅ Successfully executed {success_count}/{len(sql_commands)} commands")
        
        # Verify the changes
        print("\n3. Verifying database changes...")
        
        # Check if payments table exists
        check_payments = "SHOW TABLES LIKE 'payments'"
        payments_result = execute_query(check_payments, fetch=True)
        
        if payments_result:
            print("✅ Payments table created successfully")
            
            # Check payments table structure
            describe_payments = "DESCRIBE payments"
            payments_structure = execute_query(describe_payments, fetch=True)
            print(f"   - Payments table has {len(payments_structure)} columns")
        else:
            print("❌ Payments table not found")
        
        # Check if payment_logs table exists
        check_logs = "SHOW TABLES LIKE 'payment_logs'"
        logs_result = execute_query(check_logs, fetch=True)
        
        if logs_result:
            print("✅ Payment logs table created successfully")
        else:
            print("❌ Payment logs table not found")
        
        # Check if orders table was updated
        check_orders_columns = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ecommerce_db' 
        AND TABLE_NAME = 'orders' 
        AND COLUMN_NAME IN ('payment_status', 'razorpay_order_id')
        """
        
        orders_columns = execute_query(check_orders_columns, fetch=True)
        
        if orders_columns and len(orders_columns) >= 2:
            print("✅ Orders table updated with payment columns")
        else:
            print(f"⚠️  Orders table partially updated ({len(orders_columns) if orders_columns else 0}/2 columns)")
        
        # Check payment methods
        check_payment_methods = "SELECT COUNT(*) as count FROM payment_methods"
        methods_result = execute_query(check_payment_methods, fetch=True)
        
        if methods_result:
            count = methods_result[0]['count']
            print(f"✅ Payment methods table has {count} entries")
        else:
            print("❌ Payment methods table not accessible")
        
        print("\n" + "=" * 60)
        print("🎉 Database Update Complete!")
        print("=" * 60)
        print("Payment system database schema is now ready!")
        print("\nNext steps:")
        print("1. Install Razorpay package: pip install razorpay")
        print("2. Update razorpay_config.py with your credentials")
        print("3. Test payment integration")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_payment_tables():
    """Test the payment tables functionality"""
    print("\n🧪 Testing Payment Tables")
    print("=" * 40)
    
    try:
        # Test inserting a sample payment record
        test_payment_query = """
        INSERT INTO payments (
            order_id, razorpay_order_id, amount, status, payment_method
        ) VALUES (1, 'test_order_123', 100.00, 'created', 'test')
        """
        
        if execute_query(test_payment_query):
            print("✅ Sample payment record inserted")
            
            # Retrieve the record
            get_payment_query = "SELECT * FROM payments WHERE razorpay_order_id = 'test_order_123'"
            payment_record = execute_query(get_payment_query, fetch=True)
            
            if payment_record:
                print("✅ Sample payment record retrieved")
                
                # Clean up test data
                cleanup_query = "DELETE FROM payments WHERE razorpay_order_id = 'test_order_123'"
                execute_query(cleanup_query)
                print("✅ Test data cleaned up")
            else:
                print("❌ Failed to retrieve payment record")
        else:
            print("❌ Failed to insert sample payment record")
        
        return True
        
    except Exception as e:
        print(f"❌ Payment tables test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Razorpay Payment Database Update Script")
    print("Make sure your database is running and accessible")
    print()
    
    try:
        if update_database_for_payments():
            print("\n✅ Database update completed successfully!")
            
            # Test the tables
            if test_payment_tables():
                print("✅ Payment tables test passed!")
            else:
                print("⚠️  Payment tables test had issues")
        else:
            print("\n❌ Database update failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)