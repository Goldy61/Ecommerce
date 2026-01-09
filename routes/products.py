"""
Product routes for displaying products, categories, and search functionality
"""
from flask import Blueprint, render_template, request, jsonify
from models.product import Product
from config import Config

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def products():
    """Product listing page with filtering and pagination"""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '').strip()
    
    # Calculate pagination
    per_page = Config.PRODUCTS_PER_PAGE
    offset = (page - 1) * per_page
    
    # Get products with filters
    products_list = Product.get_all_products(
        limit=per_page + 1,  # Get one extra to check if there are more pages
        offset=offset,
        category_id=category_id,
        search=search if search else None
    )
    
    # Check if there are more pages
    has_next = len(products_list) > per_page
    if has_next:
        products_list = products_list[:-1]  # Remove the extra product
    
    has_prev = page > 1
    
    # Get categories for filter dropdown
    categories = Product.get_categories()
    
    # Get selected category name
    selected_category = None
    if category_id:
        for cat in categories:
            if cat['id'] == category_id:
                selected_category = cat['name']
                break
    
    return render_template('products.html', 
                         products=products_list,
                         categories=categories,
                         selected_category_id=category_id,
                         selected_category=selected_category,
                         search_query=search,
                         page=page,
                         has_prev=has_prev,
                         has_next=has_next,
                         prev_page=page-1 if has_prev else None,
                         next_page=page+1 if has_next else None)

@products_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return render_template('404.html'), 404
    
    # Get related products from the same category
    related_products = []
    if product.category_id:
        all_related = Product.get_all_products(category_id=product.category_id, limit=8)
        # Filter out the current product
        related_products = [p for p in all_related if p.id != product.id][:4]
    
    return render_template('product_detail.html', 
                         product=product,
                         related_products=related_products)

@products_bp.route('/api/products/autocomplete')
def api_autocomplete():
    """API endpoint for search autocomplete suggestions"""
    search_term = request.args.get('q', '').strip()
    limit = request.args.get('limit', 8, type=int)
    
    if not search_term or len(search_term) < 1:
        return jsonify({'suggestions': []})
    
    # Limit results for autocomplete
    limit = min(limit, 10)
    
    products_list = Product.get_all_products(
        limit=limit,
        search=search_term
    )
    
    # Get categories for mapping
    categories = Product.get_categories()
    category_map = {cat['id']: cat['name'] for cat in categories}
    
    # Return minimal data for autocomplete
    suggestions = []
    for product in products_list:
        suggestions.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image_url': product.image_url,
            'category_name': category_map.get(product.category_id, 'Uncategorized'),
            'stock_quantity': product.stock_quantity
        })
    
    return jsonify({'suggestions': suggestions})

@products_bp.route('/api/products/search')
def api_search_products():
    """API endpoint for product search with autocomplete support (AJAX)"""
    search_term = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if not search_term and not category_id:
        return jsonify({'products': []})
    
    # Limit the number of results for autocomplete
    limit = min(limit, 20)  # Maximum 20 results
    
    products_list = Product.get_all_products(
        limit=limit,
        category_id=category_id,
        search=search_term if search_term else None
    )
    
    # Convert products to dictionaries with additional info
    products_data = []
    categories = Product.get_categories()
    category_map = {cat['id']: cat['name'] for cat in categories}
    
    for product in products_list:
        product_dict = product.to_dict()
        # Add category name
        product_dict['category_name'] = category_map.get(product.category_id, 'Uncategorized')
        products_data.append(product_dict)
    
    return jsonify({'products': products_data})

@products_bp.route('/api/product/<int:product_id>')
def api_get_product(product_id):
    """API endpoint to get product details (AJAX)"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({'product': product.to_dict()})

@products_bp.route('/categories')
def categories():
    """Categories listing page"""
    categories_list = Product.get_categories()
    
    # Get product count for each category
    for category in categories_list:
        products_in_category = Product.get_all_products(category_id=category['id'])
        category['product_count'] = len(products_in_category)
    
    return render_template('categories.html', categories=categories_list)

@products_bp.route('/category/<int:category_id>')
def category_products(category_id):
    """Products in a specific category"""
    # Get category info
    categories = Product.get_categories()
    category = None
    for cat in categories:
        if cat['id'] == category_id:
            category = cat
            break
    
    if not category:
        return render_template('404.html'), 404
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = Config.PRODUCTS_PER_PAGE
    offset = (page - 1) * per_page
    
    # Get products in this category
    products_list = Product.get_all_products(
        limit=per_page + 1,
        offset=offset,
        category_id=category_id
    )
    
    # Check pagination
    has_next = len(products_list) > per_page
    if has_next:
        products_list = products_list[:-1]
    
    has_prev = page > 1
    
    return render_template('category_products.html',
                         category=category,
                         products=products_list,
                         page=page,
                         has_prev=has_prev,
                         has_next=has_next,
                         prev_page=page-1 if has_prev else None,
                         next_page=page+1 if has_next else None)

@products_bp.route('/api/categories')
def api_get_categories():
    """API endpoint to get all categories"""
    categories_list = Product.get_categories()
    return jsonify({'categories': categories_list})