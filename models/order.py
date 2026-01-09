"""
Order model for handling order-related database operations
"""
from .database import execute_query
from datetime import datetime

class Order:
    """Order model class"""
    
    def __init__(self, id=None, user_id=None, total_amount=None, status='pending',
                 shipping_address=None, payment_method='cash_on_delivery', 
                 created_at=None, items=None):
        self.id = id
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.shipping_address = shipping_address
        self.payment_method = payment_method
        self.created_at = created_at
        self.items = items or []
    
    @staticmethod
    def create_order(user_id, cart_items, shipping_address, payment_method='cash_on_delivery'):
        """
        Create a new order from cart items
        Args:
            user_id: ID of the user placing the order
            cart_items: List of cart items with product details
            shipping_address: Delivery address
            payment_method: Payment method (default: cash_on_delivery)
        Returns: Order ID if successful, None if failed
        """
        # Calculate total amount (convert Decimal to float for calculations)
        total_amount = sum(float(item['price']) * item['quantity'] for item in cart_items)
        
        # Create order
        order_query = """
        INSERT INTO orders (user_id, total_amount, status, shipping_address, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """
        order_params = (user_id, total_amount, 'pending', shipping_address, payment_method)
        
        if execute_query(order_query, order_params):
            # Get the created order ID
            order_id_query = "SELECT LAST_INSERT_ID() as order_id"
            result = execute_query(order_id_query, fetch=True)
            
            if result:
                order_id = result[0]['order_id'] if isinstance(result, list) else result['order_id']
                
                # Insert order items
                for item in cart_items:
                    item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                    """
                    item_params = (order_id, item['product_id'], item['quantity'], item['price'])
                    execute_query(item_query, item_params)
                
                # Clear user's cart
                Cart.clear_cart(user_id)
                
                return order_id
        return None
    
    @staticmethod
    def get_by_id(order_id):
        """Get order by ID with items"""
        order_query = """
        SELECT o.*, u.username, u.first_name, u.last_name 
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = %s
        """
        order_result = execute_query(order_query, (order_id,), fetch=True)
        
        if order_result:
            order_data = order_result[0] if isinstance(order_result, list) else order_result
            
            # Get order items
            items_query = """
            SELECT oi.*, p.name as product_name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
            """
            items_result = execute_query(items_query, (order_id,), fetch=True)
            
            order = Order(
                id=order_data['id'],
                user_id=order_data['user_id'],
                total_amount=float(order_data['total_amount']),
                status=order_data['status'],
                shipping_address=order_data['shipping_address'],
                payment_method=order_data['payment_method'],
                created_at=order_data['created_at'],
                items=items_result or []
            )
            
            # Add user info
            order.username = order_data['username']
            order.customer_name = f"{order_data['first_name']} {order_data['last_name']}"
            
            return order
        return None
    
    @staticmethod
    def get_user_orders(user_id, limit=None):
        """Get all orders for a specific user"""
        query = """
        SELECT o.*, COUNT(oi.id) as item_count
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.user_id = %s
        GROUP BY o.id
        ORDER BY o.created_at DESC
        """
        params = [user_id]
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        results = execute_query(query, params, fetch=True)
        
        if results:
            orders = []
            for row in results:
                order = Order(
                    id=row['id'],
                    user_id=row['user_id'],
                    total_amount=float(row['total_amount']),
                    status=row['status'],
                    shipping_address=row['shipping_address'],
                    payment_method=row['payment_method'],
                    created_at=row['created_at']
                )
                order.item_count = row['item_count']
                orders.append(order)
            return orders
        return []
    
    @staticmethod
    def get_all_orders(limit=None, status=None):
        """Get all orders for admin panel"""
        query = """
        SELECT o.*, u.username, u.first_name, u.last_name, COUNT(oi.id) as item_count
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        """
        params = []
        
        if status:
            query += " WHERE o.status = %s"
            params.append(status)
        
        query += " GROUP BY o.id ORDER BY o.created_at DESC"
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        results = execute_query(query, params, fetch=True)
        
        if results:
            orders = []
            for row in results:
                order = Order(
                    id=row['id'],
                    user_id=row['user_id'],
                    total_amount=float(row['total_amount']),
                    status=row['status'],
                    shipping_address=row['shipping_address'],
                    payment_method=row['payment_method'],
                    created_at=row['created_at']
                )
                order.username = row['username']
                order.customer_name = f"{row['first_name']} {row['last_name']}"
                order.item_count = row['item_count']
                orders.append(order)
            return orders
        return []
    
    def update_status(self, new_status):
        """Update order status"""
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return False
        
        query = "UPDATE orders SET status = %s WHERE id = %s"
        result = execute_query(query, (new_status, self.id))
        
        if result:
            self.status = new_status
            return True
        return False
    
    def to_dict(self):
        """Convert order object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'shipping_address': self.shipping_address,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': self.items
        }

class Cart:
    """Cart model for shopping cart operations"""
    
    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        """Add product to cart or update quantity if already exists"""
        # Check if item already in cart
        check_query = "SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s"
        existing = execute_query(check_query, (user_id, product_id), fetch=True)
        
        if existing:
            # Update quantity
            current_qty = existing[0]['quantity'] if isinstance(existing, list) else existing['quantity']
            new_quantity = current_qty + quantity
            update_query = "UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s"
            return execute_query(update_query, (new_quantity, user_id, product_id))
        else:
            # Add new item
            insert_query = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
            return execute_query(insert_query, (user_id, product_id, quantity))
    
    @staticmethod
    def get_cart_items(user_id):
        """Get all items in user's cart"""
        query = """
        SELECT c.*, p.name, p.price, p.image_url, p.stock_quantity,
               (c.quantity * p.price) as subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s AND p.is_active = TRUE
        ORDER BY c.created_at DESC
        """
        return execute_query(query, (user_id,), fetch=True) or []
    
    @staticmethod
    def update_cart_item(user_id, product_id, quantity):
        """Update cart item quantity"""
        if quantity <= 0:
            return Cart.remove_from_cart(user_id, product_id)
        
        query = "UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s"
        return execute_query(query, (quantity, user_id, product_id))
    
    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove item from cart"""
        query = "DELETE FROM cart WHERE user_id = %s AND product_id = %s"
        return execute_query(query, (user_id, product_id))
    
    @staticmethod
    def clear_cart(user_id):
        """Clear all items from user's cart"""
        query = "DELETE FROM cart WHERE user_id = %s"
        return execute_query(query, (user_id,))
    
    @staticmethod
    def get_cart_count(user_id):
        """Get total number of items in cart"""
        query = "SELECT SUM(quantity) as total FROM cart WHERE user_id = %s"
        result = execute_query(query, (user_id,), fetch=True)
        
        if result:
            total = result[0]['total'] if isinstance(result, list) else result['total']
            return total or 0
        return 0