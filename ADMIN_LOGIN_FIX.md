# 🔧 Admin Login Fix Guide

## 🐛 Problem
You can't login to the admin panel because the password hashes in the database are placeholders (`PLACEHOLDER_HASH`) instead of actual password hashes.

## 🎯 Quick Solution

### **Method 1: Run the Fix Script (Recommended)**
1. **Run the fix script:**
   ```bash
   python fix_admin_login.py
   ```

2. **Login to admin panel:**
   - URL: `http://localhost:5000/admin/login`
   - Username: `admin`
   - Password: `admin123`

### **Method 2: Manual Database Update**
1. **Generate password hashes:**
   ```bash
   python generate_passwords.py
   ```

2. **Copy the SQL commands from the output and run them in phpMyAdmin or MySQL:**
   ```sql
   UPDATE admins SET password_hash = 'generated_hash_here' WHERE username = 'admin';
   UPDATE users SET password_hash = 'generated_hash_here' WHERE username = 'john_doe';
   UPDATE users SET password_hash = 'generated_hash_here' WHERE username = 'jane_smith';
   ```

### **Method 3: Direct SQL Commands**
If you want to set custom passwords, run these SQL commands in phpMyAdmin:

```sql
-- Set admin password to 'admin123'
UPDATE admins SET password_hash = 'pbkdf2:sha256:600000$...' WHERE username = 'admin';

-- Or create a new admin if none exists
INSERT INTO admins (username, email, password_hash, full_name) 
VALUES ('admin', 'admin@ecommerce.com', 'pbkdf2:sha256:600000$...', 'System Administrator');
```

## 🔍 Troubleshooting

### **Issue 1: "Admin table doesn't exist"**
**Solution:** Run the database schema first:
```bash
mysql -u root -p ecommerce_db < database/schema.sql
mysql -u root -p ecommerce_db < database/sample_data.sql
```

### **Issue 2: "Database connection failed"**
**Solution:** Make sure XAMPP is running:
1. Start XAMPP Control Panel
2. Start Apache and MySQL services
3. Verify database exists in phpMyAdmin

### **Issue 3: "Invalid admin credentials"**
**Solution:** Check if admin exists and password is correct:
```sql
SELECT username, full_name FROM admins WHERE username = 'admin';
```

### **Issue 4: "Admin access required"**
**Solution:** Make sure you're accessing the correct URL:
- ❌ Wrong: `http://localhost:5000/login`
- ✅ Correct: `http://localhost:5000/admin/login`

## 📊 Default Credentials

After running the fix, you can use these credentials:

### **Admin Login:**
- **URL:** `http://localhost:5000/admin/login`
- **Username:** `admin`
- **Password:** `admin123`

### **Regular User Login:**
- **URL:** `http://localhost:5000/login`
- **Username:** `john_doe` or `jane_smith`
- **Password:** `user123`

## 🔧 How the Fix Works

### **The Problem:**
The sample data file contains placeholder password hashes:
```sql
INSERT INTO admins (username, email, password_hash, full_name) VALUES
('admin', 'admin@ecommerce.com', 'PLACEHOLDER_HASH', 'System Administrator');
```

### **The Solution:**
The fix script generates proper password hashes using Werkzeug's security functions:
```python
from werkzeug.security import generate_password_hash
admin_hash = generate_password_hash("admin123")
```

### **Database Update:**
The script then updates the database with the real password hash:
```sql
UPDATE admins SET password_hash = 'pbkdf2:sha256:600000$...' WHERE username = 'admin';
```

## 🎯 Verification Steps

1. **Check if admin exists:**
   ```sql
   SELECT * FROM admins WHERE username = 'admin';
   ```

2. **Test login process:**
   - Go to `http://localhost:5000/admin/login`
   - Enter username: `admin`
   - Enter password: `admin123`
   - Should redirect to admin dashboard

3. **Verify admin session:**
   - After login, check if you can access admin pages
   - Try visiting `http://localhost:5000/admin/dashboard`

## 🚀 Admin Panel Features

Once logged in, you'll have access to:

- **📊 Dashboard** - Statistics and overview
- **📦 Products** - Manage products, add/edit/delete
- **📋 Orders** - View and manage customer orders
- **👥 Users** - Manage user accounts
- **🏷️ Categories** - Manage product categories

## 🔐 Security Notes

### **Change Default Passwords:**
For production use, change the default passwords:
1. Login to admin panel
2. Go to admin settings (if available)
3. Or manually update the database:
   ```sql
   UPDATE admins SET password_hash = 'new_hash_here' WHERE username = 'admin';
   ```

### **Create Additional Admins:**
```sql
INSERT INTO admins (username, email, password_hash, full_name) 
VALUES ('your_username', 'your_email@example.com', 'your_password_hash', 'Your Full Name');
```

## 📁 Files Involved

- **`routes/auth.py`** - Contains admin login logic
- **`templates/admin/login.html`** - Admin login page
- **`database/schema.sql`** - Creates admins table
- **`database/sample_data.sql`** - Contains placeholder admin data
- **`generate_passwords.py`** - Generates password hashes
- **`fix_admin_login.py`** - Automated fix script

## ✅ Success Criteria

After applying the fix:
- ✅ Admin login page loads at `/admin/login`
- ✅ Can login with username `admin` and password `admin123`
- ✅ Redirects to admin dashboard after successful login
- ✅ Can access all admin panel features
- ✅ Admin session persists across page refreshes

The admin login should now work perfectly! 🎉