"""
Authentication routes for user login, registration, and session management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models.database import execute_query

# Use mock email service for testing (change to email_service for production)
from utils.mock_email_service import mock_email_service as email_service
# from utils.email_service import email_service  # Uncomment for production

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        # Verify user credentials
        user_result = User.verify_password(username, password)
        
        if isinstance(user_result, dict) and user_result.get('error') == 'email_not_verified':
            # User exists but email not verified
            flash('Please verify your email address before logging in.', 'warning')
            return redirect(url_for('auth.verify_email_page', user_id=user_result['user_id']))
        elif user_result:
            # User verified and valid
            session['user_id'] = user_result.id
            session['username'] = user_result.username
            session['user_type'] = 'user'
            session.permanent = True
            
            flash(f'Welcome back, {user_result.first_name}!', 'success')
            
            # Redirect to intended page or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page and handler"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        # Validation
        if not all([username, email, password, confirm_password, first_name, last_name]):
            flash('Please fill in all required fields', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        # Check if username or email already exists
        if User.get_by_username(username):
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.get_by_email(email):
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user (unverified)
        user = User.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address
        )
        
        if user:
            # Generate OTP and verification token
            otp_code = email_service.generate_otp()
            verification_token = email_service.generate_verification_token()
            
            # Send verification email
            if email_service.send_verification_email(email, first_name, otp_code, verification_token):
                # Store verification data
                if email_service.store_verification_data(user.id, email, otp_code, verification_token):
                    flash('Registration successful! Please check your email for verification code.', 'success')
                    return redirect(url_for('auth.verify_email_page', user_id=user.id))
                else:
                    flash('Registration successful but failed to send verification email. Please contact support.', 'warning')
            else:
                flash('Registration successful but failed to send verification email. Please contact support.', 'warning')
            
            return redirect(url_for('auth.verify_email_page', user_id=user.id))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """User logout handler"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        flash('Please log in to view your profile', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        user = User.get_by_id(session['user_id'])
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('auth.login'))
        
        return render_template('profile.html', user=user)
    except Exception as e:
        print(f"Database error in profile route: {e}")
        # If database fails, show profile page with session data
        mock_user = {
            'username': session.get('username', 'user'),
            'first_name': 'User',
            'last_name': '',
            'email': 'user@example.com',
            'phone': '',
            'address': ''
        }
        return render_template('profile.html', user=mock_user)

@auth_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """Update user profile"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    try:
        user = User.get_by_id(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})
        
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        # Update profile
        if user.update_profile(first_name, last_name, phone, address):
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update profile'})
    except Exception as e:
        print(f"Database error in update_profile: {e}")
        return jsonify({'success': False, 'message': 'Database error. Please try again later.'})

# Admin authentication routes
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('admin/login.html')
        
        # Verify admin credentials
        query = "SELECT * FROM admins WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        
        if result:
            admin_data = result[0] if isinstance(result, list) else result
            if check_password_hash(admin_data['password_hash'], password):
                # Create admin session
                session['admin_id'] = admin_data['id']
                session['admin_username'] = admin_data['username']
                session['user_type'] = 'admin'
                session.permanent = True
                
                flash(f'Welcome, {admin_data["full_name"]}!', 'success')
                return redirect(url_for('admin.dashboard'))
        
        flash('Invalid admin credentials', 'error')
    
    return render_template('admin/login.html')

@auth_bp.route('/admin/logout')
def admin_logout():
    """Admin logout handler"""
    session.clear()
    flash('Admin logged out successfully', 'info')
    return redirect(url_for('index'))

# Helper function to check if user is logged in
def login_required(f):
    """Decorator to require user login"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to check if admin is logged in
def admin_required(f):
    """Decorator to require admin login"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session or session.get('user_type') != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Email Verification Routes
@auth_bp.route('/verify-email')
def verify_email_page():
    """Email verification page"""
    user_id = request.args.get('user_id')
    token = request.args.get('token')
    
    if not user_id and not token:
        flash('Invalid verification link', 'error')
        return redirect(url_for('auth.login'))
    
    # If token provided, verify automatically
    if token:
        user = User.get_by_verification_token(token)
        if user:
            # Mark as verified
            query = """
            UPDATE users 
            SET is_email_verified = TRUE,
                email_verification_otp = NULL,
                email_verification_token = NULL,
                otp_expires_at = NULL
            WHERE id = %s
            """
            if execute_query(query, (user.id,)):
                flash('Email verified successfully! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
        
        flash('Invalid or expired verification link', 'error')
        return redirect(url_for('auth.login'))
    
    # Show OTP verification page
    return render_template('verify_email.html', user_id=user_id)

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP code"""
    user_id = request.form.get('user_id')
    otp_code = request.form.get('otp_code')
    
    if not user_id or not otp_code:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Verify OTP
    result = email_service.verify_otp(user_id, otp_code)
    
    if result['success']:
        return jsonify({'success': True, 'message': result['message'], 'redirect': url_for('auth.login')})
    else:
        return jsonify({'success': False, 'message': result['message']})

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    user_id = request.form.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'message': 'User ID required'})
    
    # Resend verification email
    result = email_service.resend_verification_email(user_id)
    
    return jsonify(result)