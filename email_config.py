"""
Email Configuration for E-Commerce Application
Update these settings with your email provider details
"""
import os

# Email Configuration
EMAIL_CONFIG = {
    # Gmail Configuration (recommended)
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'EMAIL_ADDRESS': 'apurvapatel2852@gmail.com',  # Your Gmail address
    'EMAIL_PASSWORD': 'njwjpiuaaziqenox',    # Gmail App Password (not regular password)
    'FROM_NAME': 'E-Commerce Store',
    
    # Alternative: Outlook/Hotmail
    # 'SMTP_SERVER': 'smtp-mail.outlook.com',
    # 'SMTP_PORT': 587,
    # 'EMAIL_ADDRESS': 'your-email@outlook.com',
    # 'EMAIL_PASSWORD': 'your-password',
    
    # Alternative: Yahoo Mail
    # 'SMTP_SERVER': 'smtp.mail.yahoo.com',
    # 'SMTP_PORT': 587,
    # 'EMAIL_ADDRESS': 'your-email@yahoo.com',
    # 'EMAIL_PASSWORD': 'your-app-password',
}

# Environment Variables (Recommended for production)
def get_email_config():
    """Get email configuration from environment variables or defaults"""
    return {
        'SMTP_SERVER': os.getenv('SMTP_SERVER', EMAIL_CONFIG['SMTP_SERVER']),
        'SMTP_PORT': int(os.getenv('SMTP_PORT', EMAIL_CONFIG['SMTP_PORT'])),
        'EMAIL_ADDRESS': os.getenv('EMAIL_ADDRESS', EMAIL_CONFIG['EMAIL_ADDRESS']),
        'EMAIL_PASSWORD': os.getenv('EMAIL_PASSWORD', EMAIL_CONFIG['EMAIL_PASSWORD']),
        'FROM_NAME': os.getenv('FROM_NAME', EMAIL_CONFIG['FROM_NAME']),
    }

# Instructions for setting up Gmail App Password:
"""
GMAIL SETUP INSTRUCTIONS:

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings: https://myaccount.google.com/
3. Navigate to Security > 2-Step Verification > App passwords
4. Generate an app password for "Mail"
5. Use this app password (not your regular Gmail password) in EMAIL_PASSWORD

ENVIRONMENT VARIABLES SETUP:

For production, set these environment variables:
- SMTP_SERVER=smtp.gmail.com
- SMTP_PORT=587
- EMAIL_ADDRESS=your-email@gmail.com
- EMAIL_PASSWORD=your-app-password
- FROM_NAME=E-Commerce Store

TESTING SETUP:

For testing without real email, you can use:
- Mailtrap.io (fake SMTP for testing)
- MailHog (local email testing)
- Or simply disable email sending in development
"""