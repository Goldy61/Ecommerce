#!/usr/bin/env python3
"""
Update database schema for email verification system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import execute_query

def update_database_schema():
    """Add email verification columns to users table"""
    print("🔧 Updating Database Schema for Email Verification")
    print("=" * 60)
    
    try:
        # Add email verification columns to users table
        print("1. Adding email verification columns to users table...")
        
        alter_queries = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN DEFAULT FALSE",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_otp VARCHAR(6)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS otp_expires_at TIMESTAMP NULL",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS otp_attempts INT DEFAULT 0"
        ]
        
        for query in alter_queries:
            try:
                execute_query(query)
                print(f"✅ Executed: {query[:50]}...")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠️  Column already exists: {query[:50]}...")
                else:
                    print(f"❌ Error: {e}")
        
        # Create email verification logs table
        print("\n2. Creating email verification logs table...")
        
        create_logs_table = """
        CREATE TABLE IF NOT EXISTS email_verification_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            email VARCHAR(100) NOT NULL,
            otp_code VARCHAR(6) NOT NULL,
            action ENUM('sent', 'verified', 'expired', 'failed') NOT NULL,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        
        if execute_query(create_logs_table):
            print("✅ Email verification logs table created successfully")
        else:
            print("❌ Failed to create email verification logs table")
        
        # Create indexes
        print("\n3. Creating indexes for better performance...")
        
        index_queries = [
            "CREATE INDEX IF NOT EXISTS idx_users_email_verification ON users(email_verification_token)",
            "CREATE INDEX IF NOT EXISTS idx_users_otp ON users(email_verification_otp)",
            "CREATE INDEX IF NOT EXISTS idx_verification_logs_user ON email_verification_logs(user_id)"
        ]
        
        for query in index_queries:
            try:
                execute_query(query)
                print(f"✅ Created index: {query.split('ON')[1] if 'ON' in query else 'unknown'}")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print(f"⚠️  Index already exists")
                else:
                    print(f"❌ Error creating index: {e}")
        
        # Update existing users to be verified (for backward compatibility)
        print("\n4. Updating existing users to be verified...")
        
        update_existing = "UPDATE users SET is_email_verified = TRUE WHERE created_at < NOW() AND is_email_verified IS NULL"
        
        if execute_query(update_existing):
            print("✅ Existing users marked as verified")
        else:
            print("❌ Failed to update existing users")
        
        # Verify the changes
        print("\n5. Verifying database changes...")
        
        verify_query = "DESCRIBE users"
        result = execute_query(verify_query, fetch=True)
        
        if result:
            verification_columns = ['is_email_verified', 'email_verification_token', 'email_verification_otp', 'otp_expires_at', 'otp_attempts']
            existing_columns = [row['Field'] for row in result]
            
            for col in verification_columns:
                if col in existing_columns:
                    print(f"✅ Column '{col}' exists")
                else:
                    print(f"❌ Column '{col}' missing")
        
        print("\n" + "=" * 60)
        print("🎉 Database Schema Update Complete!")
        print("=" * 60)
        print("Email verification system is now ready to use!")
        print("\nNext steps:")
        print("1. Configure email settings in email_config.py")
        print("2. Test user registration with email verification")
        print("3. Check email verification logs in the database")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Email Verification Database Update Script")
    print("Make sure your database is running and accessible")
    print()
    
    try:
        if update_database_schema():
            print("\n✅ Database update completed successfully!")
        else:
            print("\n❌ Database update failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)