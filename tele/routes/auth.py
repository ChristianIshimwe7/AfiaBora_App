from flask import Blueprint, request, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from datetime import datetime


auth_bp = Blueprint('auth', __name__)
client = MongoClient('localhost', 27017)
db = client['medical_db']
users_collection = db['users']
logging.basicConfig(level=logging.ERROR)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # Handle POST request
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Check if all fields are filled
    if not (username and email and password and confirm_password):
        return render_template('error.html', error_message="All fields are required")

    # Ensure passwords match
    if password != confirm_password:
        return render_template('error.html', error_message="Passwords do not match")

    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return render_template('error.html', error_message="Username already exists")

    # Hash the password and store the user in the database
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return redirect(url_for('auth.login'))

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Show login form if it's a GET request

    # Handle POST request for login
    username = request.form.get('username')
    password = request.form.get('password')

    # Find the user by username in the database
    user = users_collection.find_one({"username": username})
    
    # If the user doesn't exist or the password is incorrect, return an error message
    if not user or not check_password_hash(user['password'], password):
        return render_template('error.html', error_message="Invalid username or password")
    
    # If login is successful, store user information in the session
    session['user_id'] = str(user['_id'])  # Store the user's ID (make sure it's stored as a string)
    session['username'] = user['username']  # Optionally store the username (for user-friendly display)

    # Redirect to the profile page after successful login
    return redirect(url_for('auth.profile'))

# Profile route
@auth_bp.route('/profile')
def profile():
    from app import users_collection
    # Get user_id from session
    user_id = session.get('user_id')

    # Check if user_id exists in session
    if not user_id:
        return redirect(url_for('auth.login'))

    try:
        # Convert the string user_id from session to ObjectId for querying MongoDB
        user_id = ObjectId(user_id)
        
        # Fetch the user from the database
        user = users_collection.find_one({"_id": user_id})

        # Debugging: print user object to verify if it's retrieved correctly
        print(f"Fetched user: {user}")

        if user:
            # If join_date is a datetime object, format it to string
            if isinstance(user.get('join_date'), datetime):
                user['join_date'] = user['join_date'].strftime('%B %d, %Y')

            # Render profile template with the user's data
            return render_template('profile.html', user=user)
        else:
            return "User not found", 404

    except Exception as e:
        print(f"Error fetching user: {e}")
        return "Error fetching user", 500

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Properly remove user_id and username from the session
    session.pop('user_id', None)
    session.pop('username', None)
    
    return redirect(url_for('login'))
