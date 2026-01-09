"""
Email Service for sending verification emails and OTP codes
"""
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from models.database import execute_query
from email_config import get_email_config

class EmailService:
    def __init__(self):
        # Get email configuration
        config = get_email_config()
        self.smtp_server = config['SMTP_SERVER']
        self.smtp_port = config['SMTP_PORT']
        self.email_address = config['EMAIL_ADDRESS']
        self.email_password = config['EMAIL_PASSWORD']
        self.from_name = config['FROM_NAME']
    
    def generate_otp(self, length=6):
        """Generate a random OTP code"""
        return ''.join(random.choices(string.digits, k=length))
    
    def generate_verification_token(self, length=32):
        """Generate a random verification token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def send_verification_email(self, user_email, user_name, otp_code, verification_token):
        """Send email verification with OTP code"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Verify Your Email Address - E-Commerce Store'
            msg['From'] = f"{self.from_name} <{self.email_address}>"
            msg['To'] = user_email
            
            # Create HTML content
            html_content = self.get_verification_email_template(user_name, otp_code, verification_token)
            
            # Create plain text version
            text_content = f"""
            Hi {user_name},
            
            Welcome to E-Commerce Store!
            
            Please verify your email address by entering this OTP code:
            
            OTP Code: {otp_code}
            
            This code will expire in 15 minutes.
            
            Alternatively, you can click this link to verify:
            http://localhost:5000/auth/verify-email?token={verification_token}
            
            If you didn't create an account, please ignore this email.
            
            Best regards,
            E-Commerce Store Team
            """
            
            # Attach parts
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            return False
    
    def get_verification_email_template(self, user_name, otp_code, verification_token):
        """Get HTML template for verification email"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    font-size: 2rem;
                    font-weight: bold;
                    color: #007bff;
                    margin-bottom: 10px;
                }}
                .otp-code {{
                    background: #007bff;
                    color: white;
                    font-size: 2rem;
                    font-weight: bold;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px;
                    margin: 20px 0;
                    letter-spacing: 3px;
                }}
                .verify-btn {{
                    display: inline-block;
                    background: #28a745;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 0.9rem;
                    color: #666;
                }}
                .warning {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🛒 E-Commerce Store</div>
                    <h1>Verify Your Email Address</h1>
                </div>
                
                <p>Hi <strong>{user_name}</strong>,</p>
                
                <p>Welcome to E-Commerce Store! Please verify your email address to complete your registration.</p>
                
                <div class="otp-code">{otp_code}</div>
                
                <p>Enter this 6-digit code on the verification page, or click the button below:</p>
                
                <div style="text-align: center;">
                    <a href="http://localhost:5000/auth/verify-email?token={verification_token}" class="verify-btn">
                        Verify Email Address
                    </a>
                </div>
                
                <div class="warning">
                    <strong>⏰ Important:</strong> This code will expire in 15 minutes for security reasons.
                </div>
                
                <p>If you didn't create an account with us, please ignore this email.</p>
                
                <div class="footer">
                    <p>Best regards,<br>
                    <strong>E-Commerce Store Team</strong></p>
                    
                    <p><small>This is an automated email. Please do not reply to this message.</small></p>
                </div>
            </div>
        </body>
        </html>
        """
    
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
                return True
            
            return False
            
        except Exception as e:
            print(f"Failed to store verification data: {e}")
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
            
            return {'success': False, 'message': 'Invalid OTP code. Please try again.'}
            
        except Exception as e:
            print(f"Failed to verify OTP: {e}")
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
            print(f"Failed to resend verification email: {e}")
            return {'success': False, 'message': 'Failed to resend email. Please try again.'}

# Create global email service instance
email_service = EmailService()