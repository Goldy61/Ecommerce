#!/usr/bin/env python3
"""
Minimal test Flask app to debug CSS and template issues
"""

from flask import Flask, render_template_string, render_template

app = Flask(__name__)
app.secret_key = 'test-secret-key'

@app.route('/')
def test_home():
    """Test home page with inline template"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        <style>
            .test-box {
                background: #007bff;
                color: white;
                padding: 20px;
                margin: 20px;
                border-radius: 10px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="test-box">
            <h1>Flask CSS Test</h1>
            <p>If you see blue background, inline CSS works!</p>
            <p>CSS URL: {{ url_for('static', filename='css/style.css') }}</p>
        </div>
        
        <div class="container">
            <h2>External CSS Test</h2>
            <button class="btn btn-primary">This should be styled if external CSS loads</button>
        </div>
        
        <div style="margin: 20px; padding: 20px; background: #f8f9fa; border: 1px solid #dee2e6;">
            <h3>Debug Info</h3>
            <p>Template rendering: {{ 'Working!' }}</p>
            <p>Static folder: {{ config.get('STATIC_FOLDER', 'Not set') }}</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

@app.route('/template-test')
def template_test():
    """Test using actual template file"""
    try:
        return render_template('debug.html')
    except Exception as e:
        return f"Template error: {str(e)}"

@app.route('/admin-test')
def admin_test():
    """Test admin template with mock data"""
    mock_stats = {
        'total_products': 10,
        'total_orders': 5,
        'total_users': 3,
        'total_revenue': 150.00
    }
    
    mock_user_info = {
        'admin_username': 'test_admin'
    }
    
    try:
        return render_template('admin/dashboard.html', 
                             stats=mock_stats, 
                             user_info=mock_user_info,
                             recent_orders=[],
                             low_stock_products=[])
    except Exception as e:
        return f"Admin template error: {str(e)}"

if __name__ == '__main__':
    print("🧪 Starting Test Flask App...")
    print("Visit these URLs:")
    print("- http://localhost:5001/ (inline template test)")
    print("- http://localhost:5001/template-test (template file test)")
    print("- http://localhost:5001/admin-test (admin template test)")
    print("\nPress Ctrl+C to stop")
    
    app.run(debug=True, port=5001)