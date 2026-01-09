#!/usr/bin/env python3
"""
Debug registration process to see what's happening
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from models.database import execute_query
from utils.mock_email_service import mock_email_service

def debug_recent_registrations():
    """Check recent registrations and their verification status"""
    print("🔍 Debugging Recent Registrations")
    print("=" * 50)
    
    try:
        # Get recent users
        query = """
        SELECT id, username, email, first_name, is_email_verified, 
               email_verification_otp, otp_expires_at, created_at
        FROM users 
        ORDER BY created_at DESC 
        LIMIT 10
        """
        
        result = execute_query(query, fetch=True)
        
        if result:
            print(f"Found {len(result)} recent users:")
            print()
            
            for user in result:
                print(f"👤 User ID: {user['id']}")
                print(f"   Username: {user['username']}")
                print(f"   Email: {user['email']}")
                print(f"   Name: {user['first_name']}")
                print(f"   Verified: {'✅ Yes' if user['is_email_verified'] else '❌ No'}")
                print(f"   OTP: {user['email_verification_otp'] or 'None'}")
                print(f"   OTP Expires: {user['otp_expires_at'] or 'None'}")
                print(f"   Created: {user['created_at']}")
                print("-" * 40)
        else:
            print("No users found in database")
        
        # Check verification logs
        print("\n📋 Recent Verification Logs:")
        
        logs_query = """
        SELECT vl.*, u.username 
        FROM email_verification_logs vl
        JOIN users u ON vl.user_id = u.id
        ORDER BY vl.created_at DESC 
        LIMIT 10
        """
        
        logs_result = execute_query(logs_query, fetch=True)
        
        if logs_result:
            for log in logs_result:
                print(f"📧 {log['action'].upper()}: {log['username']} ({log['email']})")
                print(f"   OTP: {log['otp_code']}")
                print(f"   Time: {log['created_at']}")
                print("-" * 30)
        else:
            print("No verification logs found")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_email_send():
    """Manually test email sending for a user"""
    print("\n🧪 Manual Email Send Test")
    print("=" * 30)
    
    try:
        # Get the most recent unverified user
        query = """
        SELECT id, username, email, first_name 
        FROM users 
        WHERE is_email_verified = FALSE 
        ORDER BY created_at DESC 
        LIMIT 1
        """
        
        result = execute_query(query, fetch=True)
        
        if result:
            user = result[0]
            print(f"Testing email send for: {user['username']} ({user['email']})")
            
            # Generate new OTP and send email
            otp_code = mock_email_service.generate_otp()
            verification_token = mock_email_service.generate_verification_token()
            
            print(f"Generated OTP: {otp_code}")
            
            # Send email
            email_sent = mock_email_service.send_verification_email(
                user['email'], user['first_name'], otp_code, verification_token
            )
            
            if email_sent:
                print("✅ Email sent successfully")
                
                # Store verification data
                if mock_email_service.store_verification_data(
                    user['id'], user['email'], otp_code, verification_token
                ):
                    print("✅ Verification data stored")
                    print(f"\n🔢 Use this OTP to verify: {otp_code}")
                    return user['id'], otp_code
                else:
                    print("❌ Failed to store verification data")
            else:
                print("❌ Failed to send email")
        else:
            print("No unverified users found")
        
        return None, None
        
    except Exception as e:
        print(f"❌ Manual email test failed: {e}")
        return None, None

def verify_user_with_otp(user_id, otp_code):
    """Verify a user with OTP"""
    print(f"\n✅ Verifying user {user_id} with OTP {otp_code}")
    
    result = mock_email_service.verify_otp(user_id, otp_code)
    
    if result['success']:
        print(f"✅ Verification successful: {result['message']}")
        return True
    else:
        print(f"❌ Verification failed: {result['message']}")
        return False

if __name__ == "__main__":
    print("🚀 Registration Debug Tool")
    print("This will help debug the email verification process")
    print()
    
    try:
        # Debug recent registrations
        debug_recent_registrations()
        
        # Test manual email send
        user_id, otp_code = test_manual_email_send()
        
        if user_id and otp_code:
            print(f"\n💡 To verify this user manually:")
            print(f"   1. Go to: http://localhost:5000/auth/verify-email?user_id={user_id}")
            print(f"   2. Enter OTP: {otp_code}")
            print(f"   3. Or run: python -c \"from debug_registration import verify_user_with_otp; verify_user_with_otp({user_id}, '{otp_code}')\"")
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()