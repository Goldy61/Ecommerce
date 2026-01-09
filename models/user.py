"""
User model for handling user-related database operations
"""
from werkzeug.security import generate_password_hash, check_password_hash
from .database import execute_query

class User:
    """User model class"""
    
    def __init__(self, id=None, username=None, email=None, first_name=None, 
                 last_name=None, phone=None, address=None):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.address = address
    
    @staticmethod
    def create_user(username, email, password, first_name, last_name, phone=None, address=None):
        """
        Create a new user account (unverified)
        Returns: User ID if successful, None if failed
        """
        password_hash = generate_password_hash(password)
        
        query = """
        INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address, is_email_verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE)
        """
        params = (username, email, password_hash, first_name, last_name, phone, address)
        
        result = execute_query(query, params)
        if result:
            # Get the created user
            return User.get_by_username(username)
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = execute_query(query, (user_id,), fetch=True)
        
        if result:
            user_data = result[0] if isinstance(result, list) else result
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address']
            )
        return None
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        
        if result:
            user_data = result[0] if isinstance(result, list) else result
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,), fetch=True)
        
        if result:
            user_data = result[0] if isinstance(result, list) else result
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address']
            )
        return None
    
    @staticmethod
    def verify_password(username, password):
        """
        Verify user password and check email verification
        Returns: User object if valid and verified, None if invalid or unverified
        """
        query = "SELECT * FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        
        if result:
            user_data = result[0] if isinstance(result, list) else result
            if check_password_hash(user_data['password_hash'], password):
                # Check if email is verified
                if not user_data.get('is_email_verified', False):
                    return {'error': 'email_not_verified', 'user_id': user_data['id']}
                
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    phone=user_data['phone'],
                    address=user_data['address']
                )
        return None
    
    @staticmethod
    def is_email_verified(user_id):
        """Check if user's email is verified"""
        query = "SELECT is_email_verified FROM users WHERE id = %s"
        result = execute_query(query, (user_id,), fetch=True)
        
        if result:
            user_data = result[0] if isinstance(result, list) else result
            return user_data.get('is_email_verified', False)
        return False
    
    @staticmethod
    def get_by_verification_token(token):
        """Get user by email verification token"""
        query = "SELECT * FROM users WHERE email_verification_token = %s"
        result = execute_query(query, (token,), fetch=True)
        
        if result:
            user_data = result[0] if isinstance(result, list) else result
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address']
            )
        return None
    
    def update_profile(self, first_name=None, last_name=None, phone=None, address=None):
        """Update user profile information"""
        updates = []
        params = []
        
        if first_name:
            updates.append("first_name = %s")
            params.append(first_name)
            self.first_name = first_name
            
        if last_name:
            updates.append("last_name = %s")
            params.append(last_name)
            self.last_name = last_name
            
        if phone:
            updates.append("phone = %s")
            params.append(phone)
            self.phone = phone
            
        if address:
            updates.append("address = %s")
            params.append(address)
            self.address = address
        
        if updates:
            params.append(self.id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            return execute_query(query, params)
        
        return True
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'address': self.address
        }