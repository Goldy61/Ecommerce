"""
Razorpay Payment Gateway Configuration
Update these settings with your Razorpay credentials
"""
import os

# Razorpay Configuration
RAZORPAY_CONFIG = {
    # Test Mode Credentials (for development)
    'KEY_ID': 'rzp_test_your_key_id',  # Your Razorpay Test Key ID
    'KEY_SECRET': 'your_test_key_secret',  # Your Razorpay Test Key Secret
    
    # Production Credentials (for live environment)
    # 'KEY_ID': 'rzp_live_your_key_id',
    # 'KEY_SECRET': 'your_live_key_secret',
    
    # Currency
    'CURRENCY': 'INR',  # Indian Rupees
    
    # Company Details
    'COMPANY_NAME': 'E-Commerce Store',
    'COMPANY_LOGO': 'https://your-domain.com/logo.png',  # Optional
    
    # Webhook Secret (for payment verification)
    'WEBHOOK_SECRET': 'your_webhook_secret',
    
    # Payment Options
    'PAYMENT_METHODS': {
        'card': True,
        'netbanking': True,
        'wallet': True,
        'upi': True,
        'emi': True
    }
}

# Environment Variables (Recommended for production)
def get_razorpay_config():
    """Get Razorpay configuration from environment variables or defaults"""
    return {
        'KEY_ID': os.getenv('RAZORPAY_KEY_ID', RAZORPAY_CONFIG['KEY_ID']),
        'KEY_SECRET': os.getenv('RAZORPAY_KEY_SECRET', RAZORPAY_CONFIG['KEY_SECRET']),
        'CURRENCY': os.getenv('RAZORPAY_CURRENCY', RAZORPAY_CONFIG['CURRENCY']),
        'COMPANY_NAME': os.getenv('COMPANY_NAME', RAZORPAY_CONFIG['COMPANY_NAME']),
        'COMPANY_LOGO': os.getenv('COMPANY_LOGO', RAZORPAY_CONFIG.get('COMPANY_LOGO')),
        'WEBHOOK_SECRET': os.getenv('RAZORPAY_WEBHOOK_SECRET', RAZORPAY_CONFIG['WEBHOOK_SECRET']),
        'PAYMENT_METHODS': RAZORPAY_CONFIG['PAYMENT_METHODS']
    }

# Instructions for setting up Razorpay:
"""
RAZORPAY SETUP INSTRUCTIONS:

1. Create Razorpay Account:
   - Go to https://razorpay.com/
   - Sign up for a new account
   - Complete KYC verification

2. Get API Keys:
   - Login to Razorpay Dashboard
   - Go to Settings > API Keys
   - Generate Test Keys for development
   - Generate Live Keys for production

3. Update Configuration:
   - Replace 'rzp_test_your_key_id' with your actual Test Key ID
   - Replace 'your_test_key_secret' with your actual Test Key Secret
   - For production, use Live Keys

4. Test Mode vs Live Mode:
   - Test Mode: Use test keys, no real money transactions
   - Live Mode: Use live keys, real money transactions
   - Always test thoroughly before going live

5. Environment Variables (Production):
   - RAZORPAY_KEY_ID=your_actual_key_id
   - RAZORPAY_KEY_SECRET=your_actual_key_secret
   - RAZORPAY_CURRENCY=INR
   - COMPANY_NAME=Your Company Name
   - RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

6. Webhook Setup (Optional but recommended):
   - Go to Settings > Webhooks in Razorpay Dashboard
   - Add webhook URL: https://yourdomain.com/payment/webhook
   - Select events: payment.captured, payment.failed
   - Set webhook secret for security

7. Test Cards (for testing):
   - Success: 4111 1111 1111 1111
   - Failure: 4000 0000 0000 0002
   - CVV: Any 3 digits
   - Expiry: Any future date

CURRENCY SUPPORT:
- INR (Indian Rupees) - Primary
- USD, EUR, GBP - International (requires activation)

PAYMENT METHODS:
- Credit/Debit Cards (Visa, MasterCard, RuPay, Amex)
- Net Banking (All major banks)
- UPI (Google Pay, PhonePe, Paytm, etc.)
- Wallets (Paytm, Mobikwik, Freecharge, etc.)
- EMI (No Cost EMI, Regular EMI)
"""