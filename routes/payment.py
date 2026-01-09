"""
Payment routes for Razorpay integration
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.order import Order
from models.user import User
from models.database import execute_query
from routes.auth import login_required
from utils.razorpay_service import razorpay_service
import json

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/initiate', methods=['POST'])
@login_required
def initiate_payment():
    """Initiate Razorpay payment for an order"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({'success': False, 'message': 'Order ID required'})
        
        # Get order details
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        # Verify order belongs to current user
        if order.user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Unauthorized access'})
        
        # Check if payment already exists for this order
        existing_payment = razorpay_service.get_payment_record(order_id=order_id)
        if existing_payment and existing_payment['status'] in ['captured', 'paid']:
            return jsonify({'success': False, 'message': 'Order already paid'})
        
        # Get user information
        user = User.get_by_id(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Prepare user info for checkout
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone
        }
        
        # Get checkout data from Razorpay service
        checkout_data = razorpay_service.get_checkout_data(
            order_amount=float(order.total_amount),
            order_id=order_id,
            user_info=user_info
        )
        
        if not checkout_data:
            return jsonify({'success': False, 'message': 'Failed to create payment order'})
        
        # Store payment record in database
        payment_stored = razorpay_service.store_payment_record(
            order_id=order_id,
            razorpay_order_id=checkout_data['order_id'],
            razorpay_payment_id=None,  # Will be updated after payment
            amount=float(order.total_amount),
            status='created',
            payment_method='razorpay',
            notes={'initiated_by': user.username}
        )
        
        if not payment_stored:
            return jsonify({'success': False, 'message': 'Failed to store payment record'})
        
        # Update order with Razorpay order ID
        update_order_query = """
        UPDATE orders 
        SET razorpay_order_id = %s, payment_status = 'pending'
        WHERE id = %s
        """
        execute_query(update_order_query, (checkout_data['order_id'], order_id))
        
        return jsonify({
            'success': True,
            'checkout_data': checkout_data,
            'message': 'Payment initiated successfully'
        })
        
    except Exception as e:
        print(f"❌ Payment initiation failed: {e}")
        return jsonify({'success': False, 'message': 'Payment initiation failed'})

@payment_bp.route('/verify', methods=['POST'])
@login_required
def verify_payment():
    """Verify Razorpay payment after successful payment"""
    try:
        data = request.get_json()
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return jsonify({'success': False, 'message': 'Missing payment verification data'})
        
        # Verify payment signature
        is_valid = razorpay_service.verify_payment_signature(
            razorpay_order_id, razorpay_payment_id, razorpay_signature
        )
        
        if not is_valid:
            return jsonify({'success': False, 'message': 'Invalid payment signature'})
        
        # Get payment details from Razorpay
        payment_details = razorpay_service.get_payment_details(razorpay_payment_id)
        
        if not payment_details:
            return jsonify({'success': False, 'message': 'Failed to get payment details'})
        
        # Update payment record in database
        update_payment_query = """
        UPDATE payments 
        SET razorpay_payment_id = %s, 
            razorpay_signature = %s,
            status = %s,
            payment_method = %s,
            gateway_response = %s,
            updated_at = NOW()
        WHERE razorpay_order_id = %s
        """
        
        payment_status = 'captured' if payment_details['status'] == 'captured' else payment_details['status']
        
        execute_query(update_payment_query, (
            razorpay_payment_id,
            razorpay_signature,
            payment_status,
            payment_details.get('method', 'unknown'),
            json.dumps(payment_details),
            razorpay_order_id
        ))
        
        # Update order status
        update_order_query = """
        UPDATE orders 
        SET payment_status = 'paid', 
            payment_method = %s,
            payment_method_details = %s
        WHERE razorpay_order_id = %s
        """
        
        payment_method_details = {
            'method': payment_details.get('method'),
            'bank': payment_details.get('bank'),
            'wallet': payment_details.get('wallet'),
            'vpa': payment_details.get('vpa'),
            'card_id': payment_details.get('card_id')
        }
        
        execute_query(update_order_query, (
            payment_details.get('method', 'razorpay'),
            json.dumps(payment_method_details),
            razorpay_order_id
        ))
        
        # Get order ID for redirect
        order_query = "SELECT id FROM orders WHERE razorpay_order_id = %s"
        order_result = execute_query(order_query, (razorpay_order_id,), fetch=True)
        
        if order_result:
            order_id = order_result[0]['id']
            
            # Log payment success
            log_payment_event(razorpay_payment_id, 'payment_success', {
                'order_id': order_id,
                'amount': payment_details.get('amount', 0) / 100,  # Convert paise to rupees
                'method': payment_details.get('method')
            })
            
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully',
                'redirect_url': url_for('cart.order_confirmation', order_id=order_id)
            })
        else:
            return jsonify({'success': False, 'message': 'Order not found'})
        
    except Exception as e:
        print(f"❌ Payment verification failed: {e}")
        return jsonify({'success': False, 'message': 'Payment verification failed'})

@payment_bp.route('/failed', methods=['POST'])
@login_required
def payment_failed():
    """Handle failed payment"""
    try:
        data = request.get_json()
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        error_description = data.get('error_description', 'Payment failed')
        
        if razorpay_order_id:
            # Update payment record
            update_payment_query = """
            UPDATE payments 
            SET status = 'failed',
                notes = %s,
                updated_at = NOW()
            WHERE razorpay_order_id = %s
            """
            
            execute_query(update_payment_query, (
                json.dumps({'error': error_description}),
                razorpay_order_id
            ))
            
            # Update order status
            update_order_query = """
            UPDATE orders 
            SET payment_status = 'failed'
            WHERE razorpay_order_id = %s
            """
            
            execute_query(update_order_query, (razorpay_order_id,))
            
            # Log payment failure
            if razorpay_payment_id:
                log_payment_event(razorpay_payment_id, 'payment_failed', {
                    'error': error_description,
                    'razorpay_order_id': razorpay_order_id
                })
        
        return jsonify({
            'success': True,
            'message': 'Payment failure recorded',
            'redirect_url': url_for('cart.checkout')
        })
        
    except Exception as e:
        print(f"❌ Failed to handle payment failure: {e}")
        return jsonify({'success': False, 'message': 'Failed to process payment failure'})

@payment_bp.route('/status/<int:order_id>')
@login_required
def payment_status(order_id):
    """Get payment status for an order"""
    try:
        # Verify order belongs to current user
        order = Order.get_by_id(order_id)
        if not order or order.user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        # Get payment record
        payment_record = razorpay_service.get_payment_record(order_id=order_id)
        
        if payment_record:
            return jsonify({
                'success': True,
                'payment_status': payment_record['status'],
                'payment_method': payment_record['payment_method'],
                'amount': float(payment_record['amount']),
                'created_at': payment_record['created_at'].isoformat() if payment_record['created_at'] else None
            })
        else:
            return jsonify({
                'success': True,
                'payment_status': 'not_initiated',
                'message': 'No payment record found'
            })
        
    except Exception as e:
        print(f"❌ Failed to get payment status: {e}")
        return jsonify({'success': False, 'message': 'Failed to get payment status'})

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Razorpay webhooks"""
    try:
        # Get webhook data
        webhook_data = request.get_json()
        
        if not webhook_data:
            return jsonify({'status': 'error', 'message': 'No data received'}), 400
        
        # Verify webhook signature (optional but recommended)
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        
        # Log webhook event
        event_type = webhook_data.get('event')
        entity = webhook_data.get('payload', {}).get('payment', {}).get('entity', {})
        
        print(f"📧 Webhook received: {event_type}")
        
        # Store webhook event
        store_webhook_query = """
        INSERT INTO webhook_events (event_id, event_type, entity_type, entity_id, payload)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        execute_query(store_webhook_query, (
            webhook_data.get('event_id', ''),
            event_type,
            entity.get('entity', ''),
            entity.get('id', ''),
            json.dumps(webhook_data)
        ))
        
        # Process specific webhook events
        if event_type == 'payment.captured':
            handle_payment_captured_webhook(entity)
        elif event_type == 'payment.failed':
            handle_payment_failed_webhook(entity)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"❌ Webhook processing failed: {e}")
        return jsonify({'status': 'error', 'message': 'Webhook processing failed'}), 500

def handle_payment_captured_webhook(payment_entity):
    """Handle payment.captured webhook"""
    try:
        payment_id = payment_entity.get('id')
        order_id = payment_entity.get('order_id')
        
        if payment_id and order_id:
            # Update payment status
            razorpay_service.update_payment_status(payment_id, 'captured', {
                'webhook_processed': True,
                'captured_at': payment_entity.get('captured_at')
            })
            
            print(f"✅ Webhook: Payment captured - {payment_id}")
        
    except Exception as e:
        print(f"❌ Failed to handle payment captured webhook: {e}")

def handle_payment_failed_webhook(payment_entity):
    """Handle payment.failed webhook"""
    try:
        payment_id = payment_entity.get('id')
        error_description = payment_entity.get('error_description', 'Payment failed')
        
        if payment_id:
            # Update payment status
            razorpay_service.update_payment_status(payment_id, 'failed', {
                'webhook_processed': True,
                'error_description': error_description
            })
            
            print(f"❌ Webhook: Payment failed - {payment_id}")
        
    except Exception as e:
        print(f"❌ Failed to handle payment failed webhook: {e}")

def log_payment_event(payment_id, event_type, event_data):
    """Log payment event to payment_logs table"""
    try:
        # Get payment record ID
        payment_record = razorpay_service.get_payment_record(razorpay_payment_id=payment_id)
        
        if payment_record:
            log_query = """
            INSERT INTO payment_logs (payment_id, razorpay_payment_id, event_type, event_data, ip_address)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            execute_query(log_query, (
                payment_record['id'],
                payment_id,
                event_type,
                json.dumps(event_data),
                request.remote_addr
            ))
            
            print(f"📝 Payment event logged: {event_type}")
        
    except Exception as e:
        print(f"❌ Failed to log payment event: {e}")