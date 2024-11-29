from flask import Flask, request, render_template, redirect, url_for, Blueprint, jsonify, session
from pymongo import MongoClient
from routes.appointments import appointments_bp
from routes.symptom_checker import symptom_checker_bp
from routes.auth import auth_bp
from routes.health_records import health_records_bp
from routes.reports import reports_bp
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')

app.register_blueprint(appointments_bp, url_prefix='/appointments')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(health_records_bp, url_prefix='/records')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'jpg', 'jpeg', 'png', 'txt', 'docx'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

client = MongoClient('localhost', 27017)
db = client['medical_db']
collection = db['patients']
users_collection = db['users']

app.config['db'] = db

class Patient:
    def __init__(self, name, age, weight, temperature, respiration_rate, service, hospital, doctor, medicine=None):
        self.name = name
        self.age = age
        self.weight = weight
        self.temperature = temperature
        self.respiration_rate = respiration_rate
        self.service = service
        self.hospital = hospital
        self.doctor = doctor
        self.medicine = medicine

    def __repr__(self):
        return f"Name: {self.name}, Age: {self.age}, Weight: {self.weight}, Temperature: {self.temperature}, Respiration Rate: {self.respiration_rate}, Service: {self.service}, Hospital: {self.hospital}, Doctor: {self.doctor}, Medicine: {self.medicine}"

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "temperature": self.temperature,
            "respiration_rate": self.respiration_rate,
            "service": self.service,
            "hospital": self.hospital,
            "doctor": self.doctor,
            "medicine": self.medicine
        }

app.register_blueprint(symptom_checker_bp)
app.register_blueprint(reports_bp, url_prefix='/reports')

# Define a helper function to check if the user is logged in
def check_login():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in

@app.route('/home')
def dashboard():
    if check_login():
        return check_login()
    user_name = session.get('user_name', 'Guest')
    return render_template('dashboard.html', user_name=user_name)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/appointments')
def appointments():
    if check_login():
        return check_login()
    return render_template('appointment_form.html')

@app.route('/appointment_list')
def appointment_list():
    if check_login():
        return check_login()
    # Render the appointment form or appointment list page
    return render_template('appointment_list.html')

@app.route('/symptom_checker')
def symptom_checker():
    if check_login():
        return check_login()
    # Render the symptom checker form page
    return render_template('symptom_checker.html')

# Login Page
@app.route('/login')
def login():
    return render_template('login.html')

# Signup Page
@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/reports')
def reports():
    if check_login():
        return check_login()
    return render_template('reports.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/profile')
def profile():
    if check_login():
        return check_login()
    user_id = session['user_id']
    user = users_collection.find_one({"_id": user_id})
    return render_template('profile.html', user=user)

@app.route('/activity')
def activity():
    if check_login():
        return check_login()
    user_id = session['user_id']
    user = users_collection.find_one({"_id": user_id})
    return render_template('activity.html', user=user)

@app.route('/settings')
def settings():
    if check_login():
        return check_login()
    user_id = session['user_id']
    user = users_collection.find_one({"_id": user_id})
    return render_template('settings.html', user=user)

@app.route('/edit_profile')
def edit_profile():
    if check_login():
        return check_login()
    user_id = session['user_id']
    user = users_collection.find_one({"_id": user_id})
    return render_template('edit_profile.html', user=user)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect('/login')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/footer')
def footer():
    return render_template('footer.html')


if __name__ == "__main__":
    app.run(debug=True)
