-- Sample data for E-Commerce Database
USE ecommerce_db;

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Fashion and apparel'),
('Books', 'Books and educational materials'),
('Home & Garden', 'Home improvement and garden supplies'),
('Sports', 'Sports equipment and accessories');

-- Insert sample admin (password: admin123)
-- Note: Run generate_passwords.py to get proper password hashes
INSERT INTO admins (username, email, password_hash, full_name) VALUES
('admin', 'admin@ecommerce.com', 'PLACEHOLDER_HASH', 'System Administrator');

-- Insert sample users (password: user123)  
-- Note: Run generate_passwords.py to get proper password hashes
INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address) VALUES
('john_doe', 'john@example.com', 'PLACEHOLDER_HASH', 'John', 'Doe', '1234567890', '123 Main St, City, State'),
('jane_smith', 'jane@example.com', 'PLACEHOLDER_HASH', 'Jane', 'Smith', '0987654321', '456 Oak Ave, City, State');

-- Insert sample products
INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES
-- Electronics
('Smartphone X1', 'Latest smartphone with advanced features', 699.99, 50, 1, 'smartphone.jpg'),
('Laptop Pro', 'High-performance laptop for professionals', 1299.99, 25, 1, 'laptop.jpg'),
('Wireless Headphones', 'Premium noise-cancelling headphones', 199.99, 100, 1, 'headphones.jpg'),
('Smart Watch', 'Fitness tracking smartwatch', 299.99, 75, 1, 'smartwatch.jpg'),

-- Clothing
('Cotton T-Shirt', 'Comfortable cotton t-shirt', 19.99, 200, 2, 'tshirt.jpg'),
('Denim Jeans', 'Classic blue denim jeans', 49.99, 150, 2, 'jeans.jpg'),
('Running Shoes', 'Lightweight running shoes', 89.99, 80, 2, 'shoes.jpg'),
('Winter Jacket', 'Warm winter jacket', 129.99, 60, 2, 'jacket.jpg'),

-- Books
('Python Programming', 'Learn Python programming from scratch', 39.99, 100, 3, 'python_book.jpg'),
('Web Development Guide', 'Complete guide to web development', 45.99, 75, 3, 'web_book.jpg'),
('Data Science Handbook', 'Comprehensive data science reference', 59.99, 50, 3, 'data_book.jpg'),

-- Home & Garden
('Coffee Maker', 'Automatic coffee brewing machine', 79.99, 40, 4, 'coffee_maker.jpg'),
('Garden Tools Set', 'Complete set of gardening tools', 34.99, 30, 4, 'garden_tools.jpg'),
('LED Desk Lamp', 'Adjustable LED desk lamp', 24.99, 90, 4, 'desk_lamp.jpg'),

-- Sports
('Yoga Mat', 'Non-slip exercise yoga mat', 29.99, 120, 5, 'yoga_mat.jpg'),
('Basketball', 'Official size basketball', 24.99, 60, 5, 'basketball.jpg'),
('Dumbbells Set', '20lb adjustable dumbbells', 89.99, 35, 5, 'dumbbells.jpg');

-- Note: In a real application, password hashes would be generated using proper hashing
-- Run generate_passwords.py to create proper password hashes, then update the records above
-- Example commands after running generate_passwords.py:
-- UPDATE admins SET password_hash = 'generated_hash_here' WHERE username = 'admin';
-- UPDATE users SET password_hash = 'generated_hash_here' WHERE username IN ('john_doe', 'jane_smith');