"""
Razorpay Payment Service for handling payment operations
"""
import razorpay
import hmac
import hashlib
import json
from decimal import Decimal
from razorpay_config import get_razorpay_config
from models.database import execute_query

class RazorpayService:
    def __init__(self):
        """Initialize Razorpay client with configuration"""
        self.config = get_razorpay_config()
        self.client = razorpay.Client(auth=(self.config['KEY_ID'], self.config['KEY_SECRET']))
        print(f"🔧 Razorpay Service initialized with Key ID: {self.config['KEY_ID'][:10]}...")
    
    def create_order(self, amount, currency='INR', receipt=None, notes=None):
        """
        Create a Razorpay order
        
        Args:
            amount (float): Amount in rupees (will be converted to paise)
            currency (str): Currency code (default: INR)
            receipt (str): Receipt ID for reference
            notes (dict): Additional notes/metadata
        
        Returns:
            dict: Razorpay order response or None if failed
        """
        try:
            # Convert amount to paise (Razorpay uses smallest currency unit)
            amount_in_paise = int(float(amount) * 100)
            
            order_data = {
                'amount': amount_in_paise,
                'currency': currency or self.config['CURRENCY'],
                'receipt': receipt or f'order_{hash(str(amount_in_paise))}',
                'payment_capture': 1  # Auto capture payment
            }
            
            if notes:
                order_data['notes'] = notes
            
            # Create order with Razorpay
            razorpay_order = self.client.order.create(order_data)
            
            print(f"✅ Razorpay order created: {razorpay_order['id']}")
            return razorpay_order
            
        except Exception as e:
            print(f"❌ Failed to create Razorpay order: {e}")
            return None
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verify payment signature for security
        
        Args:
            razorpay_order_id (str): Razorpay order ID
            razorpay_payment_id (str): Razorpay payment ID
            razorpay_signature (str): Razorpay signature
        
        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            # Create signature string
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            # Generate expected signature
            expected_signature = hmac.new(
                self.config['KEY_SECRET'].encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            is_valid = hmac.compare_digest(expected_signature, razorpay_signature)
            
            if is_valid:
                print(f"✅ Payment signature verified for payment: {razorpay_payment_id}")
            else:
                print(f"❌ Invalid payment signature for payment: {razorpay_payment_id}")
            
            return is_valid
            
        except Exception as e:
            print(f"❌ Failed to verify payment signature: {e}")
            return False
    
    def get_payment_details(self, payment_id):
        """
        Get payment details from Razorpay
        
        Args:
            payment_id (str): Razorpay payment ID
        
        Returns:
            dict: Payment details or None if failed
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            print(f"✅ Retrieved payment details for: {payment_id}")
            return payment
            
        except Exception as e:
            print(f"❌ Failed to get payment details: {e}")
            return None
    
    def capture_payment(self, payment_id, amount):
        """
        Manually capture payment (if auto-capture is disabled)
        
        Args:
            payment_id (str): Razorpay payment ID
            amount (float): Amount to capture in rupees
        
        Returns:
            dict: Capture response or None if failed
        """
        try:
            amount_in_paise = int(float(amount) * 100)
            
            capture_response = self.client.payment.capture(payment_id, amount_in_paise)
            print(f"✅ Payment captured: {payment_id}")
            return capture_response
            
        except Exception as e:
            print(f"❌ Failed to capture payment: {e}")
            return None
    
    def refund_payment(self, payment_id, amount=None, notes=None):
        """
        Refund a payment
        
        Args:
            payment_id (str): Razorpay payment ID
            amount (float): Amount to refund in rupees (None for full refund)
            notes (dict): Refund notes
        
        Returns:
            dict: Refund response or None if failed
        """
        try:
            refund_data = {}
            
            if amount:
                refund_data['amount'] = int(float(amount) * 100)
            
            if notes:
                refund_data['notes'] = notes
            
            refund_response = self.client.payment.refund(payment_id, refund_data)
            print(f"✅ Payment refunded: {payment_id}")
            return refund_response
            
        except Exception as e:
            print(f"❌ Failed to refund payment: {e}")
            return None
    
    def store_payment_record(self, order_id, razorpay_order_id, razorpay_payment_id, 
                           amount, status, payment_method=None, notes=None):
        """
        Store payment record in database
        
        Args:
            order_id (int): Internal order ID
            razorpay_order_id (str): Razorpay order ID
            razorpay_payment_id (str): Razorpay payment ID
            amount (float): Payment amount
            status (str): Payment status
            payment_method (str): Payment method used
            notes (dict): Additional notes
        
        Returns:
            bool: True if stored successfully, False otherwise
        """
        try:
            query = """
            INSERT INTO payments (
                order_id, razorpay_order_id, razorpay_payment_id, 
                amount, status, payment_method, notes, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """
            
            params = (
                order_id,
                razorpay_order_id,
                razorpay_payment_id,
                amount,
                status,
                payment_method,
                json.dumps(notes) if notes else None
            )
            
            result = execute_query(query, params)
            
            if result:
                print(f"✅ Payment record stored for order: {order_id}")
                return True
            else:
                print(f"❌ Failed to store payment record for order: {order_id}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to store payment record: {e}")
            return False
    
    def get_payment_record(self, order_id=None, razorpay_payment_id=None):
        """
        Get payment record from database
        
        Args:
            order_id (int): Internal order ID
            razorpay_payment_id (str): Razorpay payment ID
        
        Returns:
            dict: Payment record or None if not found
        """
        try:
            if order_id:
                query = "SELECT * FROM payments WHERE order_id = %s ORDER BY created_at DESC LIMIT 1"
                params = (order_id,)
            elif razorpay_payment_id:
                query = "SELECT * FROM payments WHERE razorpay_payment_id = %s"
                params = (razorpay_payment_id,)
            else:
                return None
            
            result = execute_query(query, params, fetch=True)
            
            if result:
                payment_record = result[0] if isinstance(result, list) else result
                print(f"✅ Retrieved payment record")
                return payment_record
            else:
                print(f"❌ Payment record not found")
                return None
                
        except Exception as e:
            print(f"❌ Failed to get payment record: {e}")
            return None
    
    def update_payment_status(self, razorpay_payment_id, status, notes=None):
        """
        Update payment status in database
        
        Args:
            razorpay_payment_id (str): Razorpay payment ID
            status (str): New payment status
            notes (dict): Additional notes
        
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            query = """
            UPDATE payments 
            SET status = %s, notes = %s, updated_at = NOW()
            WHERE razorpay_payment_id = %s
            """
            
            params = (
                status,
                json.dumps(notes) if notes else None,
                razorpay_payment_id
            )
            
            result = execute_query(query, params)
            
            if result:
                print(f"✅ Payment status updated: {razorpay_payment_id} -> {status}")
                return True
            else:
                print(f"❌ Failed to update payment status: {razorpay_payment_id}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to update payment status: {e}")
            return False
    
    def get_checkout_data(self, order_amount, order_id, user_info):
        """
        Get data required for Razorpay checkout
        
        Args:
            order_amount (float): Order amount in rupees
            order_id (int): Internal order ID
            user_info (dict): User information
        
        Returns:
            dict: Checkout data for frontend
        """
        try:
            # Create Razorpay order
            razorpay_order = self.create_order(
                amount=order_amount,
                receipt=f'order_{order_id}',
                notes={
                    'order_id': str(order_id),
                    'user_id': str(user_info.get('id', '')),
                    'user_email': user_info.get('email', '')
                }
            )
            
            if not razorpay_order:
                return None
            
            # Prepare checkout data
            checkout_data = {
                'key': self.config['KEY_ID'],
                'amount': razorpay_order['amount'],  # Amount in paise
                'currency': razorpay_order['currency'],
                'order_id': razorpay_order['id'],
                'name': self.config['COMPANY_NAME'],
                'description': f'Order #{order_id}',
                'prefill': {
                    'name': f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}".strip(),
                    'email': user_info.get('email', ''),
                    'contact': user_info.get('phone', '')
                },
                'theme': {
                    'color': '#007bff'
                },
                'method': self.config['PAYMENT_METHODS']
            }
            
            # Add company logo if available
            if self.config.get('COMPANY_LOGO'):
                checkout_data['image'] = self.config['COMPANY_LOGO']
            
            return checkout_data
            
        except Exception as e:
            print(f"❌ Failed to get checkout data: {e}")
            return None

# Create global Razorpay service instance
try:
    razorpay_service = RazorpayService()
except Exception as e:
    print(f"❌ Failed to initialize Razorpay service: {e}")
    print("💡 Please install razorpay package: pip install razorpay")
    print("💡 And update razorpay_config.py with your credentials")
    razorpay_service = None