#!/usr/bin/env python3
"""
Test the registration and email verification flow
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from models.database import execute_query
from utils.mock_email_service import mock_email_service

def test_registration_flow():
    """Test the complete registration and email verification flow"""
    print("🧪 Testing Registration and Email Verification Flow")
    print("=" * 60)
    
    try:
        # Test 1: Create a test user
        print("1. Testing user creation...")
        
        test_username = "testuser123"
        test_email = "test@example.com"
        test_password = "password123"
        
        # Check if user already exists and delete if needed
        existing_user = User.get_by_username(test_username)
        if existing_user:
            delete_query = "DELETE FROM users WHERE username = %s"
            execute_query(delete_query, (test_username,))
            print(f"✅ Deleted existing test user: {test_username}")
        
        # Create new user
        user = User.create_user(
            username=test_username,
            email=test_email,
            password=test_password,
            first_name="Test",
            last_name="User"
        )
        
        if user:
            print(f"✅ User created successfully: {user.username} (ID: {user.id})")
        else:
            print("❌ Failed to create user")
            return False
        
        # Test 2: Generate and send verification email
        print("\n2. Testing email verification process...")
        
        otp_code = mock_email_service.generate_otp()
        verification_token = mock_email_service.generate_verification_token()
        
        print(f"✅ Generated OTP: {otp_code}")
        print(f"✅ Generated Token: {verification_token[:10]}...")
        
        # Send verification email
        email_sent = mock_email_service.send_verification_email(
            test_email, "Test", otp_code, verification_token
        )
        
        if email_sent:
            print("✅ Verification email sent successfully")
        else:
            print("❌ Failed to send verification email")
            return False
        
        # Store verification data
        data_stored = mock_email_service.store_verification_data(
            user.id, test_email, otp_code, verification_token
        )
        
        if data_stored:
            print("✅ Verification data stored successfully")
        else:
            print("❌ Failed to store verification data")
            return False
        
        # Test 3: Verify OTP
        print("\n3. Testing OTP verification...")
        
        # Test with correct OTP
        result = mock_email_service.verify_otp(user.id, otp_code)
        
        if result['success']:
            print(f"✅ OTP verification successful: {result['message']}")
        else:
            print(f"❌ OTP verification failed: {result['message']}")
            return False
        
        # Test 4: Check user verification status
        print("\n4. Checking user verification status...")
        
        is_verified = User.is_email_verified(user.id)
        
        if is_verified:
            print("✅ User email is now verified")
        else:
            print("❌ User email is still not verified")
            return False
        
        # Test 5: Test login with verified user
        print("\n5. Testing login with verified user...")
        
        login_result = User.verify_password(test_username, test_password)
        
        if isinstance(login_result, User):
            print(f"✅ Login successful for verified user: {login_result.username}")
        else:
            print(f"❌ Login failed: {login_result}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! Email verification system is working correctly.")
        print("=" * 60)
        
        # Cleanup
        print("\n6. Cleaning up test data...")
        delete_query = "DELETE FROM users WHERE username = %s"
        if execute_query(delete_query, (test_username,)):
            print("✅ Test user deleted successfully")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_unverified_login():
    """Test login attempt with unverified user"""
    print("\n🧪 Testing Unverified User Login")
    print("=" * 40)
    
    try:
        # Create unverified user
        test_username = "unverified_user"
        test_email = "unverified@example.com"
        test_password = "password123"
        
        # Delete if exists
        existing_user = User.get_by_username(test_username)
        if existing_user:
            delete_query = "DELETE FROM users WHERE username = %s"
            execute_query(delete_query, (test_username,))
        
        # Create user
        user = User.create_user(
            username=test_username,
            email=test_email,
            password=test_password,
            first_name="Unverified",
            last_name="User"
        )
        
        if not user:
            print("❌ Failed to create unverified user")
            return False
        
        print(f"✅ Created unverified user: {user.username}")
        
        # Try to login (should fail)
        login_result = User.verify_password(test_username, test_password)
        
        if isinstance(login_result, dict) and login_result.get('error') == 'email_not_verified':
            print("✅ Login correctly blocked for unverified user")
            print(f"   User ID for verification: {login_result['user_id']}")
        else:
            print("❌ Login should have been blocked for unverified user")
            return False
        
        # Cleanup
        delete_query = "DELETE FROM users WHERE username = %s"
        execute_query(delete_query, (test_username,))
        print("✅ Unverified test user deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Unverified login test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Email Verification System - Complete Flow Test")
    print("Make sure your database is running and accessible")
    print()
    
    try:
        # Test complete flow
        if test_registration_flow():
            print("\n✅ Registration flow test: PASSED")
        else:
            print("\n❌ Registration flow test: FAILED")
            sys.exit(1)
        
        # Test unverified login
        if test_unverified_login():
            print("✅ Unverified login test: PASSED")
        else:
            print("❌ Unverified login test: FAILED")
            sys.exit(1)
        
        print("\n🎉 ALL TESTS PASSED!")
        print("The email verification system is working correctly!")
        
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)