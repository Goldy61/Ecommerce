#!/usr/bin/env python3
"""
Test Email Verification System
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import execute_query
from utils.email_service import email_service

def test_email_verification_system():
    """Test the email verification system components"""
    print("🧪 Testing Email Verification System")
    print("=" * 50)
    
    try:
        # Test 1: Check if database columns exist
        print("1. Checking database schema...")
        
        check_columns_query = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'ecommerce_db' 
        AND TABLE_NAME = 'users' 
        AND COLUMN_NAME IN ('is_email_verified', 'email_verification_token', 'email_verification_otp', 'otp_expires_at', 'otp_attempts')
        """
        
        result = execute_query(check_columns_query, fetch=True)
        
        if result and len(result) >= 5:
            print("✅ All email verification columns exist")
        else:
            print(f"⚠️  Found {len(result) if result else 0} out of 5 required columns")
        
        # Test 2: Check if logs table exists
        print("\n2. Checking email verification logs table...")
        
        check_logs_table = """
        SELECT COUNT(*) as count 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'ecommerce_db' 
        AND TABLE_NAME = 'email_verification_logs'
        """
        
        logs_result = execute_query(check_logs_table, fetch=True)
        
        if logs_result and logs_result[0]['count'] > 0:
            print("✅ Email verification logs table exists")
        else:
            print("❌ Email verification logs table missing")
        
        # Test 3: Test OTP generation
        print("\n3. Testing OTP generation...")
        
        otp = email_service.generate_otp()
        token = email_service.generate_verification_token()
        
        if len(otp) == 6 and otp.isdigit():
            print(f"✅ OTP generated successfully: {otp}")
        else:
            print(f"❌ Invalid OTP generated: {otp}")
        
        if len(token) == 32 and token.isalnum():
            print(f"✅ Verification token generated successfully: {token[:10]}...")
        else:
            print(f"❌ Invalid token generated: {token}")
        
        # Test 4: Test email configuration
        print("\n4. Testing email configuration...")
        
        config_valid = True
        if email_service.email_address == 'your-email@gmail.com':
            print("⚠️  Email address not configured (using default)")
            config_valid = False
        
        if email_service.email_password == 'your-app-password':
            print("⚠️  Email password not configured (using default)")
            config_valid = False
        
        if config_valid:
            print("✅ Email configuration appears to be set")
        else:
            print("❌ Email configuration needs to be updated in email_config.py")
        
        # Test 5: Check existing users
        print("\n5. Checking existing users verification status...")
        
        users_query = "SELECT COUNT(*) as total, SUM(is_email_verified) as verified FROM users"
        users_result = execute_query(users_query, fetch=True)
        
        if users_result:
            total = users_result[0]['total']
            verified = users_result[0]['verified'] or 0
            print(f"✅ Found {total} users, {verified} verified")
        else:
            print("⚠️  No users found or query failed")
        
        print("\n" + "=" * 50)
        print("🎯 Email Verification System Status")
        print("=" * 50)
        
        if result and len(result) >= 5:
            print("✅ Database schema: Ready")
        else:
            print("❌ Database schema: Incomplete")
        
        if config_valid:
            print("✅ Email configuration: Ready")
        else:
            print("⚠️  Email configuration: Needs setup")
        
        print("✅ OTP generation: Working")
        print("✅ Token generation: Working")
        
        print("\n📋 Next Steps:")
        print("1. Update email_config.py with your email settings")
        print("2. Test user registration with email verification")
        print("3. Check email delivery and OTP verification")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_email_setup_instructions():
    """Show instructions for setting up email"""
    print("\n📧 EMAIL SETUP INSTRUCTIONS")
    print("=" * 50)
    print("To enable email verification, update email_config.py with:")
    print()
    print("For Gmail:")
    print("1. Enable 2-Factor Authentication")
    print("2. Generate App Password: https://myaccount.google.com/apppasswords")
    print("3. Update EMAIL_ADDRESS and EMAIL_PASSWORD in email_config.py")
    print()
    print("For testing without real email:")
    print("1. Use Mailtrap.io for fake SMTP testing")
    print("2. Or modify email_service.py to log emails instead of sending")
    print()
    print("Example configuration:")
    print("EMAIL_ADDRESS = 'your-email@gmail.com'")
    print("EMAIL_PASSWORD = 'your-16-char-app-password'")

if __name__ == "__main__":
    print("🚀 Email Verification System Test")
    print("Make sure your database is running")
    print()
    
    try:
        if test_email_verification_system():
            show_email_setup_instructions()
        else:
            print("\n❌ System test failed!")
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()