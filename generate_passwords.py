"""
Script to generate password hashes for the E-Commerce application
Run this script to generate proper password hashes for admin and test users
"""

from werkzeug.security import generate_password_hash

def generate_admin_hash():
    """Generate password hash for admin user"""
    password = "admin123"
    hash_value = generate_password_hash(password)
    print(f"Admin password hash for 'admin123': {hash_value}")
    return hash_value

def generate_user_hash():
    """Generate password hash for test user"""
    password = "user123"
    hash_value = generate_password_hash(password)
    print(f"User password hash for 'user123': {hash_value}")
    return hash_value

def generate_custom_hash(password):
    """Generate password hash for custom password"""
    hash_value = generate_password_hash(password)
    print(f"Password hash for '{password}': {hash_value}")
    return hash_value

if __name__ == "__main__":
    print("E-Commerce Password Hash Generator")
    print("=" * 40)
    
    # Generate default hashes
    admin_hash = generate_admin_hash()
    user_hash = generate_user_hash()
    
    print("\n" + "=" * 40)
    print("SQL UPDATE COMMANDS:")
    print("=" * 40)
    
    print(f"\n-- Update admin password")
    print(f"UPDATE admins SET password_hash = '{admin_hash}' WHERE username = 'admin';")
    
    print(f"\n-- Update sample user passwords")
    print(f"UPDATE users SET password_hash = '{user_hash}' WHERE username = 'john_doe';")
    print(f"UPDATE users SET password_hash = '{user_hash}' WHERE username = 'jane_smith';")
    
    print("\n" + "=" * 40)
    print("INSTRUCTIONS:")
    print("=" * 40)
    print("1. Copy the UPDATE commands above")
    print("2. Run them in phpMyAdmin or MySQL command line")
    print("3. Use these credentials to login:")
    print("   - Admin: username='admin', password='admin123'")
    print("   - Users: username='john_doe' or 'jane_smith', password='user123'")
    
    # Interactive mode
    print("\n" + "=" * 40)
    print("CUSTOM PASSWORD GENERATOR:")
    print("=" * 40)
    
    while True:
        custom_password = input("\nEnter a custom password (or 'quit' to exit): ").strip()
        if custom_password.lower() == 'quit':
            break
        if custom_password:
            generate_custom_hash(custom_password)
        else:
            print("Please enter a valid password.")
    
    print("\nThank you for using the password generator!")