# E-Commerce Website

A complete e-commerce solution built with Flask, MySQL, and vanilla JavaScript.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Server**: XAMPP (Apache + MySQL)

## Project Structure
```
ecommerce-website/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── database/
│   ├── schema.sql       # Database schema
│   └── sample_data.sql  # Sample test data
├── models/
│   ├── __init__.py
│   ├── user.py         # User model
│   ├── product.py      # Product model
│   └── order.py        # Order model
├── routes/
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── products.py     # Product routes
│   ├── cart.py         # Cart routes
│   └── admin.py        # Admin routes
├── static/
│   ├── css/
│   │   ├── style.css   # Main stylesheet
│   │   └── admin.css   # Admin panel styles
│   ├── js/
│   │   ├── main.js     # Main JavaScript
│   │   ├── cart.js     # Cart functionality
│   │   └── admin.js    # Admin panel JS
│   └── images/         # Product images
└── templates/
    ├── base.html       # Base template
    ├── index.html      # Home page
    ├── products.html   # Product listing
    ├── product_detail.html
    ├── cart.html       # Shopping cart
    ├── checkout.html   # Checkout page
    ├── login.html      # User login
    ├── register.html   # User registration
    └── admin/
        ├── dashboard.html
        ├── products.html
        └── orders.html
```

## Setup Instructions
1. Install XAMPP and start Apache + MySQL
2. Create database using provided SQL files
3. Install Python dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`
5. Access at http://localhost:5000

## Features
- User authentication and registration
- Product catalog with categories
- Shopping cart functionality
- Order management
- Admin panel for product/order management
- Responsive design