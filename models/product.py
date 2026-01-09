"""
Product model for handling product-related database operations
"""
from .database import execute_query

class Product:
    """Product model class"""
    
    def __init__(self, id=None, name=None, description=None, price=None, 
                 stock_quantity=None, category_id=None, image_url=None, 
                 is_active=True, category_name=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category_id = category_id
        self.image_url = image_url
        self.is_active = is_active
        self.category_name = category_name
    
    @staticmethod
    def get_all_products(limit=None, offset=None, category_id=None, search=None):
        """
        Get all active products with optional filtering and pagination
        """
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.is_active = TRUE
        """
        params = []
        
        # Add category filter
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
        
        # Add search filter
        if search:
            query += " AND (p.name LIKE %s OR p.description LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        query += " ORDER BY p.created_at DESC"
        
        # Add pagination
        if limit:
            query += " LIMIT %s"
            params.append(limit)
            if offset:
                query += " OFFSET %s"
                params.append(offset)
        
        results = execute_query(query, params, fetch=True)
        
        if results:
            products = []
            for row in results:
                product = Product(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    price=float(row['price']),
                    stock_quantity=row['stock_quantity'],
                    category_id=row['category_id'],
                    image_url=row['image_url'],
                    is_active=row['is_active'],
                    category_name=row['category_name']
                )
                products.append(product)
            return products
        return []
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.id = %s AND p.is_active = TRUE
        """
        result = execute_query(query, (product_id,), fetch=True)
        
        if result:
            row = result[0] if isinstance(result, list) else result
            return Product(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                price=float(row['price']),
                stock_quantity=row['stock_quantity'],
                category_id=row['category_id'],
                image_url=row['image_url'],
                is_active=row['is_active'],
                category_name=row['category_name']
            )
        return None
    
    @staticmethod
    def get_categories():
        """Get all product categories"""
        query = "SELECT * FROM categories ORDER BY name"
        results = execute_query(query, fetch=True)
        return results or []
    
    @staticmethod
    def create_product(name, description, price, stock_quantity, category_id, image_url=None):
        """Create a new product"""
        query = """
        INSERT INTO products (name, description, price, stock_quantity, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (name, description, price, stock_quantity, category_id, image_url)
        return execute_query(query, params)
    
    def update(self):
        """Update product information"""
        query = """
        UPDATE products 
        SET name = %s, description = %s, price = %s, stock_quantity = %s, 
            category_id = %s, image_url = %s, is_active = %s
        WHERE id = %s
        """
        params = (self.name, self.description, self.price, self.stock_quantity,
                 self.category_id, self.image_url, self.is_active, self.id)
        return execute_query(query, params)
    
    def delete(self):
        """Soft delete product (set is_active to False)"""
        query = "UPDATE products SET is_active = FALSE WHERE id = %s"
        return execute_query(query, (self.id,))
    
    def update_stock(self, quantity_change):
        """
        Update product stock quantity
        Args: quantity_change - positive to add stock, negative to reduce
        """
        new_quantity = self.stock_quantity + quantity_change
        if new_quantity < 0:
            return False  # Cannot have negative stock
        
        query = "UPDATE products SET stock_quantity = %s WHERE id = %s"
        result = execute_query(query, (new_quantity, self.id))
        
        if result:
            self.stock_quantity = new_quantity
            return True
        return False
    
    @staticmethod
    def get_featured_products(limit=8):
        """Get featured products for home page"""
        query = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.is_active = TRUE AND p.stock_quantity > 0
        ORDER BY p.created_at DESC 
        LIMIT %s
        """
        results = execute_query(query, (limit,), fetch=True)
        
        if results:
            products = []
            for row in results:
                product = Product(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    price=float(row['price']),
                    stock_quantity=row['stock_quantity'],
                    category_id=row['category_id'],
                    image_url=row['image_url'],
                    is_active=row['is_active'],
                    category_name=row['category_name']
                )
                products.append(product)
            return products
        return []
    
    def to_dict(self):
        """Convert product object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0,
            'stock_quantity': self.stock_quantity,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'category_name': self.category_name
        }