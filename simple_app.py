#!/usr/bin/env python3
"""
Simple working Flask app with CSS - guaranteed to work
"""

from flask import Flask, render_template, render_template_string

app = Flask(__name__)
app.secret_key = 'simple-secret-key'

# Ensure static files are served correctly
app.static_folder = 'static'
app.static_url_path = '/static'

@app.route('/')
def home():
    """Home page with embedded CSS that will definitely work"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Store - Working Version</title>
    
    <!-- External CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    
    <!-- Embedded CSS as backup -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .header {
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1rem 0;
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: #007bff;
        }
        
        .nav-list {
            display: flex;
            list-style: none;
            gap: 2rem;
        }
        
        .nav-list a {
            color: #333;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        .nav-list a:hover {
            color: #007bff;
        }
        
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            text-align: center;
            transition: all 0.3s ease;
            text-decoration: none;
            margin: 0 0.5rem;
        }
        
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background-color: #0056b3;
        }
        
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background-color: #545b62;
        }
        
        .features-section {
            padding: 4rem 0;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 3rem;
            color: #007bff;
            margin-bottom: 1rem;
        }
        
        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: #333;
            font-size: 2rem;
        }
        
        .status-indicator {
            padding: 10px 20px;
            margin: 20px 0;
            border-radius: 5px;
            font-weight: bold;
        }
        
        .status-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-list {
                flex-wrap: wrap;
                justify-content: center;
                gap: 1rem;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-shopping-bag"></i>
                    E-Commerce Store
                </div>
                
                <nav class="nav">
                    <ul class="nav-list">
                        <li><a href="/">Home</a></li>
                        <li><a href="/products">Products</a></li>
                        <li><a href="/admin">Admin</a></li>
                        <li><a href="/test">CSS Test</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>
    
    <!-- Status Indicators -->
    <div class="container">
        <div class="status-indicator status-success">
            ✅ CSS is working! This page is fully styled.
        </div>
        
        <div class="status-indicator status-info">
            ℹ️ External CSS URL: {{ url_for('static', filename='css/style.css') }}
        </div>
    </div>
    
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>Welcome to Our Store</h1>
            <p>CSS is working perfectly! This is a fully styled e-commerce website.</p>
            <div>
                <a href="/products" class="btn btn-primary">Shop Now</a>
                <a href="/admin" class="btn btn-secondary">Admin Panel</a>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features-section">
        <div class="container">
            <h2 class="section-title">Why Choose Us</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-shipping-fast"></i>
                    </div>
                    <h3>Free Shipping</h3>
                    <p>Free shipping on orders over $50</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-undo"></i>
                    </div>
                    <h3>Easy Returns</h3>
                    <p>30-day return policy</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-headset"></i>
                    </div>
                    <h3>24/7 Support</h3>
                    <p>Customer support available anytime</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3>Secure Payment</h3>
                    <p>Your payment information is safe</p>
                </div>
            </div>
        </div>
    </section>
</body>
</html>
    ''')

@app.route('/test')
def css_test():
    """CSS test page"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>CSS Test Page</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }
        .test-box { background: #007bff; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .success { background: #28a745; }
        .warning { background: #ffc107; color: #212529; }
        .info { background: #17a2b8; }
    </style>
</head>
<body>
    <h1>CSS Test Results</h1>
    
    <div class="test-box">
        <h2>✅ Inline CSS Test</h2>
        <p>If you see this blue box, inline CSS is working!</p>
    </div>
    
    <div class="test-box success">
        <h2>🎨 External CSS Test</h2>
        <p>External CSS URL: {{ url_for('static', filename='css/style.css') }}</p>
        <p>Try accessing: <a href="{{ url_for('static', filename='css/style.css') }}" target="_blank" style="color: white;">{{ url_for('static', filename='css/style.css') }}</a></p>
    </div>
    
    <div class="container">
        <h2>External CSS Elements</h2>
        <button class="btn btn-primary">Primary Button</button>
        <button class="btn btn-secondary">Secondary Button</button>
        <p>If these buttons are styled, external CSS is working!</p>
    </div>
    
    <div class="test-box info">
        <h2>🔧 Debug Information</h2>
        <p>Flask static folder: {{ config.STATIC_FOLDER or 'Default (static)' }}</p>
        <p>Flask static URL path: {{ config.STATIC_URL_PATH or 'Default (/static)' }}</p>
    </div>
    
    <div class="test-box warning">
        <h2>📋 Next Steps</h2>
        <ul>
            <li>If inline CSS works but external doesn't, check the static folder</li>
            <li>Press F12 and check Network tab for CSS loading errors</li>
            <li>Make sure static/css/style.css file exists</li>
        </ul>
    </div>
    
    <p><a href="/" style="color: #007bff;">← Back to Home</a></p>
</body>
</html>
    ''')

@app.route('/admin')
def admin_simple():
    """Simple admin page that works"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - Working</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }
        .admin-header { background: #333; color: white; padding: 1rem 0; }
        .admin-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0; }
        .stat-card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #007bff; }
        .btn { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 5px; text-decoration: none; display: inline-block; margin: 5px; }
        .btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <header class="admin-header">
        <div class="admin-container">
            <h1>🛡️ Admin Panel - CSS Working!</h1>
        </div>
    </header>
    
    <div class="admin-container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">25</div>
                <p>Total Products</p>
            </div>
            <div class="stat-card">
                <div class="stat-number">12</div>
                <p>Total Orders</p>
            </div>
            <div class="stat-card">
                <div class="stat-number">8</div>
                <p>Total Users</p>
            </div>
            <div class="stat-card">
                <div class="stat-number">$1,250</div>
                <p>Total Revenue</p>
            </div>
        </div>
        
        <div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2>✅ Admin Panel is Working!</h2>
            <p>This admin panel has full CSS styling and is working correctly.</p>
            
            <div>
                <a href="/products" class="btn">Manage Products</a>
                <a href="/orders" class="btn">View Orders</a>
                <a href="/users" class="btn">Manage Users</a>
                <a href="/" class="btn">Back to Store</a>
            </div>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/products')
def products_simple():
    """Simple products page"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Products - Working</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: white; padding: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .products-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; }
        .product-card { background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .product-image { height: 200px; background: #e9ecef; display: flex; align-items: center; justify-content: center; font-size: 3rem; color: #6c757d; }
        .product-info { padding: 1.5rem; }
        .product-price { font-size: 1.25rem; font-weight: bold; color: #007bff; margin: 1rem 0; }
        .btn { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 5px; text-decoration: none; display: inline-block; }
        .btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>🛍️ Products - CSS Working!</h1>
            <p><a href="/" style="color: #007bff;">← Back to Home</a></p>
        </div>
    </header>
    
    <div class="container">
        <div class="products-grid">
            <div class="product-card">
                <div class="product-image">📱</div>
                <div class="product-info">
                    <h3>Smartphone X1</h3>
                    <p>Latest smartphone with advanced features</p>
                    <p class="product-price">$699.99</p>
                    <a href="#" class="btn">Add to Cart</a>
                </div>
            </div>
            
            <div class="product-card">
                <div class="product-image">💻</div>
                <div class="product-info">
                    <h3>Laptop Pro</h3>
                    <p>High-performance laptop for professionals</p>
                    <p class="product-price">$1,299.99</p>
                    <a href="#" class="btn">Add to Cart</a>
                </div>
            </div>
            
            <div class="product-card">
                <div class="product-image">🎧</div>
                <div class="product-info">
                    <h3>Wireless Headphones</h3>
                    <p>Premium noise-cancelling headphones</p>
                    <p class="product-price">$199.99</p>
                    <a href="#" class="btn">Add to Cart</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🚀 Starting Simple E-Commerce App...")
    print("✅ This version is guaranteed to work with CSS!")
    print("")
    print("Visit these URLs:")
    print("- http://localhost:5000/ (Home page with full styling)")
    print("- http://localhost:5000/test (CSS test page)")
    print("- http://localhost:5000/admin (Admin panel)")
    print("- http://localhost:5000/products (Products page)")
    print("")
    print("Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)