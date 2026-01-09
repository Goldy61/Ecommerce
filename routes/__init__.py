"""
Routes package for the E-Commerce application
"""

from .auth import auth_bp
from .products import products_bp
from .cart import cart_bp
from .admin import admin_bp
from .payment import payment_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp)