-- Razorpay Payment System Database Schema
-- Add payment-related tables to support Razorpay integration

USE ecommerce_db;

-- Payments table to store payment transactions
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    razorpay_order_id VARCHAR(100) NOT NULL,
    razorpay_payment_id VARCHAR(100),
    razorpay_signature VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    status ENUM('created', 'pending', 'captured', 'failed', 'refunded', 'cancelled') DEFAULT 'created',
    payment_method VARCHAR(50),
    gateway_response JSON,
    notes JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_razorpay_order_id (razorpay_order_id),
    INDEX idx_razorpay_payment_id (razorpay_payment_id),
    INDEX idx_payment_status (status),
    INDEX idx_payment_created (created_at)
);

-- Payment logs table for tracking payment events
CREATE TABLE IF NOT EXISTS payment_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_id INT,
    razorpay_payment_id VARCHAR(100),
    event_type VARCHAR(50) NOT NULL,
    event_data JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE,
    INDEX idx_payment_logs_payment (payment_id),
    INDEX idx_payment_logs_event (event_type),
    INDEX idx_payment_logs_created (created_at)
);

-- Refunds table to track refund transactions
CREATE TABLE IF NOT EXISTS refunds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_id INT NOT NULL,
    razorpay_refund_id VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'INR',
    status ENUM('pending', 'processed', 'failed') DEFAULT 'pending',
    reason VARCHAR(255),
    notes JSON,
    gateway_response JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE,
    INDEX idx_refund_razorpay_id (razorpay_refund_id),
    INDEX idx_refund_status (status),
    INDEX idx_refund_created (created_at)
);

-- Update orders table to include payment status
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS razorpay_order_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS payment_method_details JSON;

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_razorpay_id ON orders(razorpay_order_id);

-- Payment methods configuration table (optional)
CREATE TABLE IF NOT EXISTS payment_methods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(50) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    configuration JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default payment methods
INSERT IGNORE INTO payment_methods (method_name, display_name, is_active) VALUES
('razorpay', 'Razorpay (Cards, UPI, Net Banking)', TRUE),
('cash_on_delivery', 'Cash on Delivery', TRUE);

-- Webhook events table to track Razorpay webhooks
CREATE TABLE IF NOT EXISTS webhook_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(100) NOT NULL UNIQUE,
    event_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50),
    entity_id VARCHAR(100),
    payload JSON NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    processed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_webhook_event_id (event_id),
    INDEX idx_webhook_event_type (event_type),
    INDEX idx_webhook_processed (processed),
    INDEX idx_webhook_created (created_at)
);

-- Payment analytics view (optional)
CREATE OR REPLACE VIEW payment_analytics AS
SELECT 
    DATE(p.created_at) as payment_date,
    p.status,
    p.payment_method,
    COUNT(*) as transaction_count,
    SUM(p.amount) as total_amount,
    AVG(p.amount) as average_amount
FROM payments p
GROUP BY DATE(p.created_at), p.status, p.payment_method
ORDER BY payment_date DESC;

-- Add some sample data for testing (optional)
-- This will be useful for testing the payment system
INSERT IGNORE INTO payment_methods (method_name, display_name, is_active, configuration) VALUES
('test_card', 'Test Credit Card', FALSE, '{"test_mode": true, "card_number": "4111111111111111"}'),
('test_upi', 'Test UPI', FALSE, '{"test_mode": true, "upi_id": "test@paytm"}');

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_payments_order_status ON payments(order_id, status);
CREATE INDEX IF NOT EXISTS idx_payments_created_status ON payments(created_at, status);
CREATE INDEX IF NOT EXISTS idx_orders_payment_created ON orders(payment_status, created_at);