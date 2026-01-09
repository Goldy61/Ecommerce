"""
Models package for the E-Commerce application
"""

from .database import get_db_connection, close_db_connection
from .user import User
from .product import Product
from .order import Order

__all__ = ['get_db_connection', 'close_db_connection', 'User', 'Product', 'Order']