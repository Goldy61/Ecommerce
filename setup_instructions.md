# E-Commerce Website Setup Instructions

## Prerequisites

1. **XAMPP** - Download and install from https://www.apachefriends.org/
2. **Python 3.7+** - Download from https://www.python.org/
3. **Git** (optional) - For version control

## Step-by-Step Setup

### 1. Start XAMPP Services

1. Open XAMPP Control Panel
2. Start **Apache** service
3. Start **MySQL** service
4. Verify both services are running (green status)

### 2. Create Database

1. Open your web browser and go to `http://localhost/phpmyadmin`
2. Click "New" to create a new database
3. Name it `ecommerce_db`
4. Click "Create"

### 3. Import Database Schema

1. In phpMyAdmin, select the `ecommerce_db` database
2. Click on the "Import" tab
3. Choose the file `database/schema.sql` from your project folder
4. Click "Go" to execute the SQL commands
5. Repeat the process with `database/sample_data.sql` to add sample data

### 4. Install Python Dependencies

1. Open Command Prompt or Terminal
2. Navigate to your project folder:
   ```bash
   cd path/to/your/ecommerce-website
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 5. Configure Database Connection

1. Open `config.py`
2. Verify the database settings match your XAMPP MySQL setup:
   - Host: `localhost`
   - User: `root`
   - Password: `` (empty by default)
   - Database: `ecommerce_db`

### 6. Run the Application

1. In your project folder, run:
   ```bash
   python app.py
   ```
2. You should see output like:
   ```
   Starting E-Commerce Application...
   Make sure XAMPP is running with Apache and MySQL services
   Database should be created using the SQL files in database/ folder
   Access the application at: http://localhost:5000
   ```
3. Open your web browser and go to `http://localhost:5000`

## Default Login Credentials

### Admin Login
- URL: `http://localhost:5000/admin/login`
- Username: `admin`
- Password: `admin123` (you'll need to hash this properly)

### Test User Account
You can register a new user account or create one manually in the database.

## Project Structure

```
ecommerce-website/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── database/
│   ├── schema.sql       # Database schema
│   └── sample_data.sql  # Sample test data
├── models/              # Database models
├── routes/              # Flask routes/controllers
├── static/              # CSS, JS, images
└── templates/           # HTML templates
```

## Features Included

### User Features
- User registration and login
- Browse products by category
- Search products
- Add items to shopping cart
- Update cart quantities
- Checkout and place orders
- View order history
- User profile management

### Admin Features
- Admin login
- Dashboard with statistics
- Product management (CRUD)
- Category management
- Order management
- User management

### Technical Features
- MVC architecture
- Session management
- Password hashing
- Input validation
- Responsive design
- AJAX cart functionality
- Error handling

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure XAMPP MySQL is running
   - Check database credentials in `config.py`
   - Verify database `ecommerce_db` exists

2. **Module Not Found Error**
   - Run `pip install -r requirements.txt`
   - Ensure you're in the correct directory

3. **Port Already in Use**
   - Change the port in `app.py`: `app.run(port=5001)`
   - Or stop other applications using port 5000

4. **Images Not Loading**
   - Add actual image files to `static/images/`
   - Or use the placeholder system built into the templates

### Adding Real Product Images

1. Place product images in `static/images/` folder
2. Update the `image_url` field in the products table
3. Use filenames like: `smartphone.jpg`, `laptop.jpg`, etc.

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `config.py`
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Update admin password hash
5. Implement proper input sanitization
6. Add CSRF protection
7. Use a production database (not XAMPP)

## Next Steps

1. Add more products and categories
2. Implement payment gateway integration
3. Add email notifications
4. Implement inventory management
5. Add product reviews and ratings
6. Implement wishlist functionality
7. Add advanced search filters
8. Implement caching for better performance

## Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify all services are running
3. Check the database connection
4. Ensure all dependencies are installed

For development questions, refer to:
- Flask documentation: https://flask.palletsprojects.com/
- MySQL documentation: https://dev.mysql.com/doc/
- Bootstrap documentation: https://getbootstrap.com/docs/