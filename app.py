"""
Main Flask application for E-Commerce website
"""
from flask import Flask, render_template, session
from config import config
from routes import register_blueprints
from models.product import Product
from models.order import Cart
import os

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Explicitly set static folder and URL path
    app.static_folder = 'static'
    app.static_url_path = '/static'
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    register_blueprints(app)
    
    # Main routes
    @app.route('/')
    def index():
        """Home page"""
        try:
            # Get featured products
            featured_products = Product.get_featured_products(limit=8)
            
            # Get categories
            categories = Product.get_categories()
            
            return render_template('index.html', 
                                 featured_products=featured_products,
                                 categories=categories)
        except Exception as e:
            print(f"Database error in index route: {e}")
            # If database fails, show a working page anyway
            return render_template('index.html', 
                                 featured_products=[],
                                 categories=[])
    
    @app.route('/test')
    def test():
        """Test page to check if CSS is loading"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>CSS Test</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <style>
                .test-box {
                    background-color: red;
                    color: white;
                    padding: 20px;
                    margin: 20px;
                    border-radius: 10px;
                }
            </style>
        </head>
        <body>
            <div class="test-box">
                <h1>CSS Test Page</h1>
                <p>If you see this box with red background, inline CSS is working.</p>
                <p>Check browser developer tools (F12) to see if style.css is loading.</p>
            </div>
            <div class="container">
                <h2>This should be styled by style.css if it's loading</h2>
                <button class="btn btn-primary">Test Button</button>
            </div>
        </body>
        </html>
        '''
    
    @app.route('/test-cart')
    def test_cart():
        """Test cart page without authentication"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shopping Cart Test - E-Commerce Store</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <style>
                body { font-family: Arial, sans-serif; background: #f8f9fa; }
                .container { max-width: 1200px; margin: 2rem auto; padding: 0 20px; }
                .cart-container { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; }
                .cart-items { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .cart-item { display: flex; align-items: center; gap: 1rem; padding: 1.5rem 0; border-bottom: 1px solid #eee; }
                .item-image { width: 100px; height: 100px; background: #e9ecef; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 2rem; color: #6c757d; }
                .item-details { flex: 1; }
                .item-details h3 { margin-bottom: 0.5rem; color: #333; }
                .item-price { font-weight: bold; color: #007bff; margin-bottom: 0.5rem; }
                .quantity-controls { display: flex; align-items: center; gap: 0.5rem; }
                .quantity-btn { width: 30px; height: 30px; border: 1px solid #ddd; background: #f8f9fa; cursor: pointer; border-radius: 3px; }
                .quantity-input { width: 60px; text-align: center; padding: 5px; border: 1px solid #ddd; border-radius: 3px; }
                .cart-summary { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); height: fit-content; }
                .summary-row { display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid #eee; }
                .total-row { font-size: 1.2rem; font-weight: bold; border-top: 2px solid #007bff; margin-top: 1rem; padding-top: 1rem; }
                .btn { padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; }
                .btn-primary { background: #007bff; color: white; }
                .btn-outline { background: transparent; color: #007bff; border: 2px solid #007bff; }
                .btn:hover { opacity: 0.9; }
                .checkout-btn { width: 100%; margin-bottom: 1rem; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style="text-align: center; margin-bottom: 2rem; color: #333;">Shopping Cart (Test)</h1>
                
                <div class="cart-container">
                    <div class="cart-items">
                        <h2 style="margin-bottom: 1.5rem; color: #333;">Items in Your Cart</h2>
                        
                        <!-- Sample Cart Item 1 -->
                        <div class="cart-item">
                            <div class="item-image">📱</div>
                            <div class="item-details">
                                <h3>Smartphone X1</h3>
                                <p class="item-price">$699.99</p>
                                <p style="color: #28a745; font-size: 0.9rem;">In Stock</p>
                            </div>
                            <div class="item-quantity">
                                <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Quantity:</label>
                                <div class="quantity-controls">
                                    <button class="quantity-btn">-</button>
                                    <input type="number" class="quantity-input" value="1" min="1">
                                    <button class="quantity-btn">+</button>
                                </div>
                            </div>
                            <div class="item-subtotal">
                                <span style="display: block; font-size: 0.9rem; color: #666; margin-bottom: 0.25rem;">Subtotal:</span>
                                <span style="font-size: 1.1rem; font-weight: bold; color: #333;">$699.99</span>
                            </div>
                            <div class="item-actions">
                                <button style="background: none; border: none; color: #dc3545; font-size: 1.2rem; cursor: pointer; padding: 8px;" title="Remove from cart">🗑️</button>
                            </div>
                        </div>
                        
                        <!-- Sample Cart Item 2 -->
                        <div class="cart-item">
                            <div class="item-image">💻</div>
                            <div class="item-details">
                                <h3>Laptop Pro</h3>
                                <p class="item-price">$1,299.99</p>
                                <p style="color: #28a745; font-size: 0.9rem;">In Stock</p>
                            </div>
                            <div class="item-quantity">
                                <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Quantity:</label>
                                <div class="quantity-controls">
                                    <button class="quantity-btn">-</button>
                                    <input type="number" class="quantity-input" value="1" min="1">
                                    <button class="quantity-btn">+</button>
                                </div>
                            </div>
                            <div class="item-subtotal">
                                <span style="display: block; font-size: 0.9rem; color: #666; margin-bottom: 0.25rem;">Subtotal:</span>
                                <span style="font-size: 1.1rem; font-weight: bold; color: #333;">$1,299.99</span>
                            </div>
                            <div class="item-actions">
                                <button style="background: none; border: none; color: #dc3545; font-size: 1.2rem; cursor: pointer; padding: 8px;" title="Remove from cart">🗑️</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="cart-summary">
                        <h3 style="margin-bottom: 1.5rem; text-align: center; color: #333;">Order Summary</h3>
                        
                        <div class="summary-row">
                            <span>Subtotal:</span>
                            <span>$1,999.98</span>
                        </div>
                        
                        <div class="summary-row">
                            <span>Tax (8%):</span>
                            <span>$160.00</span>
                        </div>
                        
                        <div class="summary-row">
                            <span>Shipping:</span>
                            <span>$10.00</span>
                        </div>
                        
                        <div class="summary-row total-row">
                            <span>Total:</span>
                            <span>$2,169.98</span>
                        </div>
                        
                        <div style="margin-top: 2rem;">
                            <button class="btn btn-primary checkout-btn" onclick="alert('Checkout requires user login and database setup!')">
                                Proceed to Checkout
                            </button>
                            <a href="/" class="btn btn-outline" style="width: 100%;">Continue Shopping</a>
                        </div>
                    </div>
                </div>
                
                <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-top: 2rem;">
                    <h3>✅ Shopping Cart Features Working:</h3>
                    <ul style="line-height: 2;">
                        <li>✅ Beautiful cart layout and styling</li>
                        <li>✅ Responsive grid design</li>
                        <li>✅ Product display with images</li>
                        <li>✅ Quantity controls styling</li>
                        <li>✅ Order summary calculations</li>
                        <li>✅ Action buttons and interactions</li>
                    </ul>
                    
                    <p><strong>Note:</strong> This is a test version with sample data. The real cart will work once you log in and the database is set up.</p>
                </div>
            </div>
            
            <script>
                // Add some interactivity to quantity buttons
                document.querySelectorAll('.quantity-btn').forEach(btn => {
                    btn.addEventListener('click', function() {
                        const input = this.parentNode.querySelector('.quantity-input');
                        const isIncrease = this.textContent === '+';
                        let value = parseInt(input.value);
                        
                        if (isIncrease) {
                            input.value = value + 1;
                        } else if (value > 1) {
                            input.value = value - 1;
                        }
                    });
                });
            </script>
        </body>
        </html>
        '''
    
    @app.route('/test-profile')
    def test_profile():
        """Test profile page without database"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Profile Test - E-Commerce Store</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <style>
                body { font-family: Arial, sans-serif; background: #f8f9fa; }
                .container { max-width: 800px; margin: 2rem auto; }
                .profile-card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 2rem; }
                .profile-header { text-align: center; margin-bottom: 2rem; }
                .profile-avatar { font-size: 5rem; color: #007bff; margin-bottom: 1rem; }
                .form-group { margin-bottom: 1.5rem; }
                .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
                .form-group input, .form-group textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }
                .btn { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; margin-right: 1rem; }
                .btn:hover { background: #0056b3; }
                .btn-secondary { background: #6c757d; }
                .btn-secondary:hover { background: #545b62; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="profile-card">
                    <div class="profile-header">
                        <div class="profile-avatar">
                            <i class="fas fa-user-circle"></i>
                        </div>
                        <h1>User Profile (Test)</h1>
                        <p>This is a test profile page. CSS is working perfectly!</p>
                    </div>
                    
                    <form>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div class="form-group">
                                <label for="first_name">First Name</label>
                                <input type="text" id="first_name" value="John" readonly>
                            </div>
                            
                            <div class="form-group">
                                <label for="last_name">Last Name</label>
                                <input type="text" id="last_name" value="Doe" readonly>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" value="john@example.com" readonly>
                        </div>
                        
                        <div class="form-group">
                            <label for="phone">Phone Number</label>
                            <input type="tel" id="phone" value="+1 (555) 123-4567" readonly>
                        </div>
                        
                        <div class="form-group">
                            <label for="address">Address</label>
                            <textarea id="address" rows="3" readonly>123 Main Street
City, State 12345</textarea>
                        </div>
                        
                        <div style="margin-top: 2rem;">
                            <button type="button" class="btn" onclick="alert('Profile update requires database setup!')">Update Profile</button>
                            <button type="button" class="btn btn-secondary" onclick="window.location.href='/'">Back to Home</button>
                        </div>
                    </form>
                </div>
                
                <div class="profile-card">
                    <h3>✅ Profile Page Features Working:</h3>
                    <ul style="line-height: 2;">
                        <li>✅ CSS styling is perfect</li>
                        <li>✅ Responsive design</li>
                        <li>✅ Form layout and styling</li>
                        <li>✅ Icons and typography</li>
                        <li>✅ Button interactions</li>
                    </ul>
                    
                    <p><strong>Note:</strong> This is a test version. The real profile page will work once the database is set up.</p>
                </div>
            </div>
            
            <!-- Font Awesome for icons -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </body>
        </html>
        '''
    
    @app.route('/simple-test')
    def simple_test():
        """Simple test without database"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Test</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .test { background: #007bff; color: white; padding: 20px; border-radius: 10px; }
            </style>
        </head>
        <body>
            <div class="test">
                <h1>Simple CSS Test</h1>
                <p>If you see this blue box, inline CSS works!</p>
            </div>
            <div class="container">
                <h2>External CSS Test</h2>
                <button class="btn btn-primary">Test Button</button>
            </div>
        </body>
        </html>
        '''
    
    @app.route('/simple-login')
    def simple_login():
        """Simple login page for testing"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login - E-Commerce Store</title>
            <link rel="stylesheet" href="/static/css/style.css">
            <style>
                body { font-family: Arial, sans-serif; background: #f8f9fa; }
                .container { max-width: 500px; margin: 2rem auto; }
                .form-container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 1.5rem; }
                .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
                .form-group input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; }
                .btn { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
                .btn:hover { background: #0056b3; }
                .text-center { text-align: center; }
                .mt-3 { margin-top: 1rem; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="form-container">
                    <h2 class="text-center mb-4">Login to Your Account</h2>
                    <p class="text-center">This is a test login page. CSS is working!</p>
                    
                    <form>
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" placeholder="Enter your username">
                        </div>
                        
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" placeholder="Enter your password">
                        </div>
                        
                        <div class="form-group">
                            <button type="button" class="btn" onclick="alert('Login functionality requires database setup!')">
                                Login (Test)
                            </button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <p><a href="/">← Back to Home</a></p>
                        <p><a href="/register">Don't have an account? Register here</a></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
    
    @app.route('/debug')
    def debug():
        """Debug page"""
        return render_template('debug.html')
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html')
    
    @app.route('/contact')
    def contact():
        """Contact page"""
        return render_template('contact.html')
    
    # Context processor to make cart count available in all templates
    @app.context_processor
    def inject_cart_count():
        """Inject cart count into all templates"""
        cart_count = 0
        try:
            if 'user_id' in session:
                cart_count = Cart.get_cart_count(session['user_id'])
                # Ensure cart_count is always an integer, never None
                cart_count = int(cart_count) if cart_count is not None else 0
        except Exception as e:
            print(f"Error getting cart count: {e}")
            cart_count = 0
        return {'cart_count': cart_count}
    
    # Context processor to make user info available in all templates
    @app.context_processor
    def inject_user_info():
        """Inject user info into all templates"""
        user_info = {
            'is_logged_in': 'user_id' in session,
            'is_admin': session.get('user_type') == 'admin',
            'username': session.get('username'),
            'admin_username': session.get('admin_username')
        }
        return {'user_info': user_info}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return render_template('500.html'), 500
    
    return app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Run the application
    print("Starting E-Commerce Application...")
    print("Make sure XAMPP is running with Apache and MySQL services")
    print("Database should be created using the SQL files in database/ folder")
    print("Access the application at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)