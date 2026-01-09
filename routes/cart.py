"""
Shopping cart routes for cart management, checkout, and order processing
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.order import Cart, Order
from models.product import Product
from models.user import User
from routes.auth import login_required

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart():
    """Display shopping cart"""
    try:
        user_id = session['user_id']
        cart_items = Cart.get_cart_items(user_id)
        
        # Calculate totals (convert Decimal to float for calculations)
        subtotal = sum(float(item['subtotal']) for item in cart_items)
        tax = subtotal * 0.08  # 8% tax
        shipping = 10.00 if subtotal > 0 else 0  # $10 shipping, free if empty cart
        total = subtotal + tax + shipping
        
        return render_template('cart.html',
                             cart_items=cart_items,
                             subtotal=subtotal,
                             tax=tax,
                             shipping=shipping,
                             total=total)
    except Exception as e:
        print(f"Database error in cart route: {e}")
        # If database fails, show empty cart
        return render_template('cart.html',
                             cart_items=[],
                             subtotal=0,
                             tax=0,
                             shipping=0,
                             total=0)

@cart_bp.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """Add product to cart (AJAX)"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({'success': False, 'message': 'Product ID required'})
        
        # Validate product exists and is available
        product = Product.get_by_id(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'})
        
        if product.stock_quantity < quantity:
            return jsonify({'success': False, 'message': 'Insufficient stock'})
        
        # Add to cart
        user_id = session['user_id']
        if Cart.add_to_cart(user_id, product_id, quantity):
            # Get updated cart count
            cart_count = Cart.get_cart_count(user_id)
            return jsonify({
                'success': True, 
                'message': f'{product.name} added to cart',
                'cart_count': cart_count
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to add to cart'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'})

@cart_bp.route('/api/cart/update', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantity (AJAX)"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 0)
        
        if not product_id:
            return jsonify({'success': False, 'message': 'Product ID required'})
        
        user_id = session['user_id']
        
        if quantity <= 0:
            # Remove item from cart
            if Cart.remove_from_cart(user_id, product_id):
                cart_count = Cart.get_cart_count(user_id)
                return jsonify({
                    'success': True, 
                    'message': 'Item removed from cart',
                    'cart_count': cart_count
                })
        else:
            # Validate stock
            product = Product.get_by_id(product_id)
            if product and product.stock_quantity >= quantity:
                if Cart.update_cart_item(user_id, product_id, quantity):
                    cart_count = Cart.get_cart_count(user_id)
                    return jsonify({
                        'success': True, 
                        'message': 'Cart updated',
                        'cart_count': cart_count
                    })
            else:
                return jsonify({'success': False, 'message': 'Insufficient stock'})
        
        return jsonify({'success': False, 'message': 'Failed to update cart'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'})

@cart_bp.route('/api/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    """Remove item from cart (AJAX)"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'success': False, 'message': 'Product ID required'})
        
        user_id = session['user_id']
        
        if Cart.remove_from_cart(user_id, product_id):
            cart_count = Cart.get_cart_count(user_id)
            return jsonify({
                'success': True, 
                'message': 'Item removed from cart',
                'cart_count': cart_count
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to remove item'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'})

@cart_bp.route('/api/cart/count')
@login_required
def get_cart_count():
    """Get cart item count (AJAX)"""
    user_id = session['user_id']
    count = Cart.get_cart_count(user_id)
    return jsonify({'cart_count': count})

@cart_bp.route('/checkout')
@login_required
def checkout():
    """Checkout page"""
    user_id = session['user_id']
    cart_items = Cart.get_cart_items(user_id)
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart.view_cart'))
    
    # Get user info for pre-filling form
    user = User.get_by_id(user_id)
    
    # Calculate totals (convert Decimal to float for calculations)
    subtotal = sum(float(item['subtotal']) for item in cart_items)
    tax = subtotal * 0.08
    shipping = 10.00
    total = subtotal + tax + shipping
    
    return render_template('checkout.html',
                         cart_items=cart_items,
                         user=user,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)

@cart_bp.route('/place-order', methods=['POST'])
@login_required
def place_order():
    """Process order placement"""
    user_id = session['user_id']
    cart_items = Cart.get_cart_items(user_id)
    
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart.view_cart'))
    
    # Get form data
    shipping_address = request.form.get('shipping_address')
    payment_method = request.form.get('payment_method', 'cash_on_delivery')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    if not shipping_address:
        flash('Shipping address is required', 'error')
        return redirect(url_for('cart.checkout'))
    
    # Validate stock availability
    for item in cart_items:
        product = Product.get_by_id(item['product_id'])
        if not product or product.stock_quantity < item['quantity']:
            flash(f'Insufficient stock for {item["name"]}', 'error')
            return redirect(url_for('cart.checkout'))
    
    # Prepare cart items for order creation
    order_items = []
    for item in cart_items:
        order_items.append({
            'product_id': item['product_id'],
            'quantity': item['quantity'],
            'price': item['price']
        })
    
    # Create order with payment method
    order_id = Order.create_order(user_id, order_items, shipping_address, payment_method)
    
    if order_id:
        # Update customer information in order
        update_customer_info_query = """
        UPDATE orders 
        SET first_name = %s, last_name = %s, email = %s, phone = %s
        WHERE id = %s
        """
        execute_query(update_customer_info_query, (first_name, last_name, email, phone, order_id))
        
        # For Cash on Delivery, complete the order immediately
        if payment_method == 'cash_on_delivery':
            # Update product stock
            for item in cart_items:
                product = Product.get_by_id(item['product_id'])
                if product:
                    product.update_stock(-item['quantity'])
            
            # Clear cart
            Cart.clear_cart(user_id)
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('cart.order_confirmation', order_id=order_id))
        
        # For Razorpay, redirect to order confirmation (payment will be handled by JavaScript)
        elif payment_method == 'razorpay':
            return redirect(url_for('cart.order_confirmation', order_id=order_id))
    
    flash('Failed to place order. Please try again.', 'error')
    return redirect(url_for('cart.checkout'))

@cart_bp.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    """Order confirmation page"""
    user_id = session['user_id']
    order = Order.get_by_id(order_id)
    
    # Verify order belongs to current user
    if not order or order.user_id != user_id:
        flash('Order not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('order_confirmation.html', order=order)

@cart_bp.route('/orders')
@login_required
def order_history():
    """User order history"""
    user_id = session['user_id']
    orders = Order.get_user_orders(user_id)
    
    return render_template('order_history.html', orders=orders)

@cart_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """Order detail page"""
    user_id = session['user_id']
    order = Order.get_by_id(order_id)
    
    # Verify order belongs to current user
    if not order or order.user_id != user_id:
        flash('Order not found', 'error')
        return redirect(url_for('cart.order_history'))
    
    return render_template('order_detail.html', order=order)