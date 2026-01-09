"""
Mock Email Service for testing email verification without real email
This service logs emails to console instead of sending them
"""
import random
import string
from datetime import datetime, timedelta
from models.database import execute_query

class MockEmailService:
    def __init__(self):
        self.from_name = 'E-Commerce Store (Test Mode)'
        print("📧 Mock Email Service initialized - emails will be logged to console")
    
    def generate_otp(self, length=6):
        """Generate a random OTP code"""
        return ''.join(random.choices(string.digits, k=length))
    
    def generate_verification_token(self, length=32):
        """Generate a random verification token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def send_verification_email(self, user_email, user_name, otp_code, verification_token):
        """Mock send email verification with OTP code (logs to console)"""
        print("\n" + "="*60)
        print("📧 EMAIL VERIFICATION (TEST MODE)")
        print("="*60)
        print(f"To: {user_email}")
        print(f"Subject: Verify Your Email Address - E-Commerce Store")
        print()
        print(f"Hi {user_name},")
        print()
        print("Welcome to E-Commerce Store!")
        print()
        print("Please verify your email address by entering this OTP code:")
        print()
        print(f"🔢 OTP CODE: {otp_code}")
        print()
        print("This code will expire in 15 minutes.")
        print()
        print("Alternatively, you can use this verification link:")
        print(f"http://localhost:5000/auth/verify-email?token={verification_token}")
        print()
        print("If you didn't create an account, please ignore this email.")
        print()
        print("Best regards,")
        print("E-Commerce Store Team")
        print("="*60)
        print("✅ Email logged successfully (would be sent in production)")
        print("="*60)
        
        # Always return True for mock service
        return True
    
    def store_verification_data(self, user_id, email, otp_code, verification_token):
        """Store OTP and verification token in database"""
        try:
            # Set expiration time (15 minutes from now)
            expires_at = datetime.now() + timedelta(minutes=15)
            
            # Update user with verification data
            query = """
            UPDATE users 
            SET email_verification_otp = %s, 
                email_verification_token = %s, 
                otp_expires_at = %s,
                otp_attempts = 0
            WHERE id = %s
            """
            
            result = execute_query(query, (otp_code, verification_token, expires_at, user_id))
            
            if result:
                # Log the email sending
                log_query = """
                INSERT INTO email_verification_logs (user_id, email, otp_code, action)
                VALUES (%s, %s, %s, 'sent')
                """
                execute_query(log_query, (user_id, email, otp_code))
                print(f"✅ Verification data stored for user {user_id}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Failed to store verification data: {e}")
            return False
    
    def verify_otp(self, user_id, otp_code):
        """Verify OTP code for user"""
        try:
            # Get user verification data
            query = """
            SELECT email_verification_otp, otp_expires_at, otp_attempts, email
            FROM users 
            WHERE id = %s
            """
            
            result = execute_query(query, (user_id,), fetch=True)
            
            if not result:
                return {'success': False, 'message': 'User not found'}
            
            user_data = result[0] if isinstance(result, list) else result
            
            # Check if OTP has expired
            if user_data['otp_expires_at'] and datetime.now() > user_data['otp_expires_at']:
                return {'success': False, 'message': 'OTP has expired. Please request a new one.'}
            
            # Check attempt limit
            if user_data['otp_attempts'] >= 5:
                return {'success': False, 'message': 'Too many failed attempts. Please request a new OTP.'}
            
            # Verify OTP
            if user_data['email_verification_otp'] == otp_code:
                # Mark email as verified
                update_query = """
                UPDATE users 
                SET is_email_verified = TRUE,
                    email_verification_otp = NULL,
                    email_verification_token = NULL,
                    otp_expires_at = NULL,
                    otp_attempts = 0
                WHERE id = %s
                """
                
                if execute_query(update_query, (user_id,)):
                    # Log successful verification
                    log_query = """
                    INSERT INTO email_verification_logs (user_id, email, otp_code, action)
                    VALUES (%s, %s, %s, 'verified')
                    """
                    execute_query(log_query, (user_id, user_data['email'], otp_code))
                    
                    print(f"✅ Email verified successfully for user {user_id}")
                    return {'success': True, 'message': 'Email verified successfully!'}
            
            # Increment failed attempts
            attempt_query = "UPDATE users SET otp_attempts = otp_attempts + 1 WHERE id = %s"
            execute_query(attempt_query, (user_id,))
            
            # Log failed attempt
            log_query = """
            INSERT INTO email_verification_logs (user_id, email, otp_code, action)
            VALUES (%s, %s, %s, 'failed')
            """
            execute_query(log_query, (user_id, user_data['email'], otp_code))
            
            print(f"❌ Invalid OTP attempt for user {user_id}")
            return {'success': False, 'message': 'Invalid OTP code. Please try again.'}
            
        except Exception as e:
            print(f"❌ Failed to verify OTP: {e}")
            return {'success': False, 'message': 'Verification failed. Please try again.'}
    
    def resend_verification_email(self, user_id):
        """Resend verification email with new OTP"""
        try:
            # Get user data
            query = "SELECT username, email, first_name FROM users WHERE id = %s"
            result = execute_query(query, (user_id,), fetch=True)
            
            if not result:
                return {'success': False, 'message': 'User not found'}
            
            user_data = result[0] if isinstance(result, list) else result
            
            # Generate new OTP and token
            otp_code = self.generate_otp()
            verification_token = self.generate_verification_token()
            
            # Send email
            if self.send_verification_email(
                user_data['email'], 
                user_data['first_name'], 
                otp_code, 
                verification_token
            ):
                # Store new verification data
                if self.store_verification_data(user_id, user_data['email'], otp_code, verification_token):
                    return {'success': True, 'message': 'Verification email sent successfully!'}
            
            return {'success': False, 'message': 'Failed to send verification email'}
            
        except Exception as e:
            print(f"❌ Failed to resend verification email: {e}")
            return {'success': False, 'message': 'Failed to resend email. Please try again.'}

# Create global mock email service instance
mock_email_service = MockEmailService()