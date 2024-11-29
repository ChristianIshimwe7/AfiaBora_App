from flask import Blueprint, request, render_template, redirect, url_for, session
from bson import ObjectId # to use MongoDB ObjectId for unique ticket IDs
from flask import current_app

# Create a Blueprint for appointments
appointments_bp = Blueprint('appointments', __name__)

# Route to create a new appointment
@appointments_bp.route('/new', methods=['GET', 'POST'])
def create_appointment():
    from app import db
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        service = request.form['service']

        # Validate inputs
        if not (patient_name and doctor_name and appointment_date and appointment_time):
            return "All fields are required!", 400

        # Save the appointment
        collection_appointments = db['appointments']
        appointment = {
            "patient_name": patient_name,
            "doctor_name": doctor_name,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "service": service
        }
        result = collection_appointments.insert_one(appointment)
        ticket_id = str(result.inserted_id)

        return redirect(url_for('appointments.ticket', ticket_id=ticket_id))


@appointments_bp.route('/ticket/<ticket_id>')
def ticket(ticket_id):
    db = current_app.config['db']
    # Fetch the appointment using the ticket ID
    collection_appointments = db['appointments']
    appointment = collection_appointments.find_one({"_id": ObjectId(ticket_id)})
    if not appointment:
        return "Ticket not found", 404
    
    return render_template('appointment_ticket.html', appointment=appointment, ticket_id=ticket_id)

@appointments_bp.route('/appointments_list')
def appointments_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if not authenticated
    
    # Replace with your database collection for appointments
    appointments_collection = appointments_bp.config['db']['appointments']
    
    # Query to fetch appointments for the logged-in user
    user_id = session.get('user_id')
    appointments = list(appointments_collection.find({"user_id": user_id}))
    
    return render_template('appointments_list.html', appointments=appointments)
