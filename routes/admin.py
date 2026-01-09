"""
Admin routes for managing products, orders, and users
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.product import Product
from models.order import Order
from models.user import User
from models.database import execute_query
from routes.auth import admin_required
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
# @admin_required  # Temporarily disabled for testing
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics
    stats = {}
    
    # Total products
    products = Product.get_all_products()
    stats['total_products'] = len(products)
    
    # Total orders
    orders = Order.get_all_orders()
    stats['total_orders'] = len(orders)
    
    # Total users
    user_query = "SELECT COUNT(*) as count FROM users"
    user_result = execute_query(user_query, fetch=True)
    stats['total_users'] = user_result[0]['count'] if user_result else 0
    
    # Total revenue
    revenue_query = "SELECT SUM(total_amount) as revenue FROM orders WHERE status != 'cancelled'"
    revenue_result = execute_query(revenue_query, fetch=True)
    stats['total_revenue'] = float(revenue_result[0]['revenue']) if revenue_result and revenue_result[0]['revenue'] else 0
    
    # Recent orders
    recent_orders = Order.get_all_orders(limit=5)
    
    # Low stock products
    low_stock_query = "SELECT * FROM products WHERE stock_quantity < 10 AND is_active = TRUE ORDER BY stock_quantity ASC LIMIT 5"
    low_stock_products = execute_query(low_stock_query, fetch=True) or []
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products)

@admin_bp.route('/products')
@admin_required
def products():
    """Admin products management"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    
    # Get all products (including inactive ones for admin)
    query = """
    SELECT p.*, c.name as category_name 
    FROM products p 
    LEFT JOIN categories c ON p.category_id = c.id
    """
    params = []
    
    if search:
        query += " WHERE (p.name LIKE %s OR p.description LIKE %s)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
    
    query += " ORDER BY p.created_at DESC"
    
    products_list = execute_query(query, params, fetch=True) or []
    
    # Get categories for dropdown
    categories = Product.get_categories()
    
    return render_template('admin/products.html',
                         products=products_list,
                         categories=categories,
                         search_query=search)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price', type=float)
        stock_quantity = request.form.get('stock_quantity', type=int)
        category_id = request.form.get('category_id', type=int)
        image_url = request.form.get('image_url')
        
        # Validation
        if not all([name, description, price, stock_quantity, category_id]):
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('admin.add_product'))
        
        if price <= 0:
            flash('Price must be greater than 0', 'error')
            return redirect(url_for('admin.add_product'))
        
        if stock_quantity < 0:
            flash('Stock quantity cannot be negative', 'error')
            return redirect(url_for('admin.add_product'))
        
        # Create product
        if Product.create_product(name, description, price, stock_quantity, category_id, image_url):
            flash('Product added successfully', 'success')
            return redirect(url_for('admin.products'))
        else:
            flash('Failed to add product', 'error')
    
    categories = Product.get_categories()
    return render_template('admin/add_product.html', categories=categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    """Edit existing product"""
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin.products'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = request.form.get('price', type=float)
        product.stock_quantity = request.form.get('stock_quantity', type=int)
        product.category_id = request.form.get('category_id', type=int)
        product.image_url = request.form.get('image_url')
        product.is_active = request.form.get('is_active') == 'on'
        
        # Validation
        if not all([product.name, product.description, product.price, product.stock_quantity, product.category_id]):
            flash('Please fill in all required fields', 'error')
            return render_template('admin/edit_product.html', product=product, categories=Product.get_categories())
        
        if product.price <= 0:
            flash('Price must be greater than 0', 'error')
            return render_template('admin/edit_product.html', product=product, categories=Product.get_categories())
        
        if product.stock_quantity < 0:
            flash('Stock quantity cannot be negative', 'error')
            return render_template('admin/edit_product.html', product=product, categories=Product.get_categories())
        
        # Update product
        if product.update():
            flash('Product updated successfully', 'success')
            return redirect(url_for('admin.products'))
        else:
            flash('Failed to update product', 'error')
    
    categories = Product.get_categories()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Delete (deactivate) product"""
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'})
    
    if product.delete():
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete product'})

@admin_bp.route('/orders')
@admin_required
def orders():
    """Admin orders management"""
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    
    orders_list = Order.get_all_orders(status=status_filter)
    
    # Get order status counts for filter tabs
    status_counts = {}
    all_orders = Order.get_all_orders()
    status_counts['all'] = len(all_orders)
    
    for status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        status_orders = [o for o in all_orders if o.status == status]
        status_counts[status] = len(status_orders)
    
    return render_template('admin/orders.html',
                         orders=orders_list,
                         status_filter=status_filter,
                         status_counts=status_counts)

@admin_bp.route('/orders/<int:order_id>')
@admin_required
def order_detail(order_id):
    """Admin order detail view"""
    order = Order.get_by_id(order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('admin.orders'))
    
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/update-status', methods=['POST'])
@admin_required
def update_order_status():
    """Update order status"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        if not order_id or not new_status:
            return jsonify({'success': False, 'message': 'Missing required fields'})
        
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'})
        
        if order.update_status(new_status):
            return jsonify({'success': True, 'message': 'Order status updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update order status'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'})

@admin_bp.route('/users')
@admin_required
def users():
    """Admin users management"""
    search = request.args.get('search', '').strip()
    
    query = "SELECT * FROM users"
    params = []
    
    if search:
        query += " WHERE (username LIKE %s OR email LIKE %s OR first_name LIKE %s OR last_name LIKE %s)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term, search_term])
    
    query += " ORDER BY created_at DESC"
    
    users_list = execute_query(query, params, fetch=True) or []
    
    return render_template('admin/users.html',
                         users=users_list,
                         search_query=search)

@admin_bp.route('/categories')
@admin_required
def categories():
    """Admin categories management"""
    categories_list = Product.get_categories()
    
    # Get product count for each category
    for category in categories_list:
        count_query = "SELECT COUNT(*) as count FROM products WHERE category_id = %s AND is_active = TRUE"
        count_result = execute_query(count_query, (category['id'],), fetch=True)
        category['product_count'] = count_result[0]['count'] if count_result else 0
    
    return render_template('admin/categories.html', categories=categories_list)

@admin_bp.route('/categories/add', methods=['POST'])
@admin_required
def add_category():
    """Add new category"""
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('Category name is required', 'error')
        return redirect(url_for('admin.categories'))
    
    query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
    if execute_query(query, (name, description)):
        flash('Category added successfully', 'success')
    else:
        flash('Failed to add category', 'error')
    
    return redirect(url_for('admin.categories'))

@admin_bp.route('/categories/edit/<int:category_id>', methods=['POST'])
@admin_required
def edit_category(category_id):
    """Edit category"""
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('Category name is required', 'error')
        return redirect(url_for('admin.categories'))
    
    query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
    if execute_query(query, (name, description, category_id)):
        flash('Category updated successfully', 'success')
    else:
        flash('Failed to update category', 'error')
    
    return redirect(url_for('admin.categories'))

@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    """Delete category"""
    # Check if category has products
    check_query = "SELECT COUNT(*) as count FROM products WHERE category_id = %s"
    result = execute_query(check_query, (category_id,), fetch=True)
    
    if result and result[0]['count'] > 0:
        return jsonify({'success': False, 'message': 'Cannot delete category with existing products'})
    
    delete_query = "DELETE FROM categories WHERE id = %s"
    if execute_query(delete_query, (category_id,)):
        return jsonify({'success': True, 'message': 'Category deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to delete category'})