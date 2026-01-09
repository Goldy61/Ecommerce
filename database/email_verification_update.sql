-- Email Verification System Database Updates
-- Add email verification fields to users table

USE ecommerce_db;

-- Add email verification columns to users table
ALTER TABLE users 
ADD COLUMN is_email_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN email_verification_token VARCHAR(255),
ADD COLUMN email_verification_otp VARCHAR(6),
ADD COLUMN otp_expires_at TIMESTAMP NULL,
ADD COLUMN otp_attempts INT DEFAULT 0;

-- Create email verification logs table for tracking
CREATE TABLE email_verification_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    action ENUM('sent', 'verified', 'expired', 'failed') NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create index for better performance
CREATE INDEX idx_users_email_verification ON users(email_verification_token);
CREATE INDEX idx_users_otp ON users(email_verification_otp);
CREATE INDEX idx_verification_logs_user ON email_verification_logs(user_id);

-- Update existing users to be verified (for backward compatibility)
UPDATE users SET is_email_verified = TRUE WHERE created_at < NOW();