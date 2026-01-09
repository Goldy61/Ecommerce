#!/usr/bin/env python3
"""
Create payment tables for Razorpay integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import execute_query

def create_payment_tables():
    """Create payment-related tables step by step"""
    print("🔧 Creating Payment Tables for Razorpay")
    print("=" * 50)
    
    try:
        # 1. Create payments table
        print("1. Creating payments table...")
        
        payments_table = """
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            razorpay_order_id VARCHAR(100) NOT NULL,
            razorpay_payment_id VARCHAR(100),
            razorpay_signature VARCHAR(255),
            amount DECIMAL(10, 2) NOT NULL,
            currency VARCHAR(3) DEFAULT 'INR',
            status ENUM('created', 'pending', 'captured', 'failed', 'refunded', 'cancelled') DEFAULT 'created',
            payment_method VARCHAR(50),
            gateway_response JSON,
            notes JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """
        
        if execute_query(payments_table):
            print("✅ Payments table created successfully")
        else:
            print("❌ Failed to create payments table")
        
        # 2. Create payment_logs table
        print("\n2. Creating payment_logs table...")
        
        payment_logs_table = """
        CREATE TABLE IF NOT EXISTS payment_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            payment_id INT,
            razorpay_payment_id VARCHAR(100),
            event_type VARCHAR(50) NOT NULL,
            event_data JSON,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE
        )
        """
        
        if execute_query(payment_logs_table):
            print("✅ Payment logs table created successfully")
        else:
            print("❌ Failed to create payment logs table")
        
        # 3. Create refunds table
        print("\n3. Creating refunds table...")
        
        refunds_table = """
        CREATE TABLE IF NOT EXISTS refunds (
            id INT AUTO_INCREMENT PRIMARY KEY,
            payment_id INT NOT NULL,
            razorpay_refund_id VARCHAR(100) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            currency VARCHAR(3) DEFAULT 'INR',
            status ENUM('pending', 'processed', 'failed') DEFAULT 'pending',
            reason VARCHAR(255),
            notes JSON,
            gateway_response JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE
        )
        """
        
        if execute_query(refunds_table):
            print("✅ Refunds table created successfully")
        else:
            print("❌ Failed to create refunds table")
        
        # 4. Update orders table
        print("\n4. Updating orders table...")
        
        # Add payment_status column
        add_payment_status = """
        ALTER TABLE orders 
        ADD COLUMN IF NOT EXISTS payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending'
        """
        
        try:
            execute_query(add_payment_status)
            print("✅ Added payment_status column to orders table")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("⚠️  payment_status column already exists")
            else:
                print(f"❌ Failed to add payment_status column: {e}")
        
        # Add razorpay_order_id column
        add_razorpay_order_id = """
        ALTER TABLE orders 
        ADD COLUMN IF NOT EXISTS razorpay_order_id VARCHAR(100)
        """
        
        try:
            execute_query(add_razorpay_order_id)
            print("✅ Added razorpay_order_id column to orders table")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("⚠️  razorpay_order_id column already exists")
            else:
                print(f"❌ Failed to add razorpay_order_id column: {e}")
        
        # 5. Create payment_methods table
        print("\n5. Creating payment_methods table...")
        
        payment_methods_table = """
        CREATE TABLE IF NOT EXISTS payment_methods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            method_name VARCHAR(50) NOT NULL UNIQUE,
            display_name VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            configuration JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        if execute_query(payment_methods_table):
            print("✅ Payment methods table created successfully")
        else:
            print("❌ Failed to create payment methods table")
        
        # 6. Insert default payment methods
        print("\n6. Inserting default payment methods...")
        
        insert_methods = """
        INSERT IGNORE INTO payment_methods (method_name, display_name, is_active) VALUES
        ('razorpay', 'Razorpay (Cards, UPI, Net Banking)', TRUE),
        ('cash_on_delivery', 'Cash on Delivery', TRUE)
        """
        
        if execute_query(insert_methods):
            print("✅ Default payment methods inserted")
        else:
            print("❌ Failed to insert default payment methods")
        
        # 7. Create indexes
        print("\n7. Creating indexes for better performance...")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id)",
            "CREATE INDEX IF NOT EXISTS idx_payments_razorpay_order_id ON payments(razorpay_order_id)",
            "CREATE INDEX IF NOT EXISTS idx_payments_razorpay_payment_id ON payments(razorpay_payment_id)",
            "CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status)",
            "CREATE INDEX IF NOT EXISTS idx_payment_logs_payment_id ON payment_logs(payment_id)",
            "CREATE INDEX IF NOT EXISTS idx_refunds_payment_id ON refunds(payment_id)"
        ]
        
        for index_query in indexes:
            try:
                execute_query(index_query)
                index_name = index_query.split('idx_')[1].split(' ')[0]
                print(f"✅ Created index: idx_{index_name}")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print(f"⚠️  Index already exists")
                else:
                    print(f"❌ Failed to create index: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Payment Tables Creation Complete!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to create payment tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_payment_tables():
    """Verify that all payment tables were created successfully"""
    print("\n🔍 Verifying Payment Tables")
    print("=" * 30)
    
    try:
        tables_to_check = ['payments', 'payment_logs', 'refunds', 'payment_methods']
        
        for table in tables_to_check:
            check_query = f"SHOW TABLES LIKE '{table}'"
            result = execute_query(check_query, fetch=True)
            
            if result:
                print(f"✅ Table '{table}' exists")
                
                # Get table structure
                describe_query = f"DESCRIBE {table}"
                structure = execute_query(describe_query, fetch=True)
                print(f"   - {len(structure)} columns")
            else:
                print(f"❌ Table '{table}' not found")
        
        # Check orders table columns
        print("\n🔍 Checking orders table updates...")
        
        orders_columns_query = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ecommerce_db' 
        AND TABLE_NAME = 'orders' 
        AND COLUMN_NAME IN ('payment_status', 'razorpay_order_id')
        """
        
        orders_columns = execute_query(orders_columns_query, fetch=True)
        
        if orders_columns:
            for column in orders_columns:
                print(f"✅ Orders table has column: {column['COLUMN_NAME']}")
        else:
            print("❌ Orders table missing payment columns")
        
        # Check payment methods data
        print("\n🔍 Checking payment methods...")
        
        methods_query = "SELECT method_name, display_name, is_active FROM payment_methods"
        methods = execute_query(methods_query, fetch=True)
        
        if methods:
            for method in methods:
                status = "Active" if method['is_active'] else "Inactive"
                print(f"✅ Payment method: {method['method_name']} ({status})")
        else:
            print("❌ No payment methods found")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Payment Tables Creation Script")
    print("Make sure your database is running and accessible")
    print()
    
    try:
        if create_payment_tables():
            print("\n✅ Payment tables created successfully!")
            
            if verify_payment_tables():
                print("\n✅ All payment tables verified!")
                print("\nNext steps:")
                print("1. Install Razorpay: pip install razorpay")
                print("2. Update razorpay_config.py with your credentials")
                print("3. Test payment integration")
            else:
                print("\n⚠️  Some verification checks failed")
        else:
            print("\n❌ Failed to create payment tables!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)