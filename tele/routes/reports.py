from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from bson import ObjectId
import os

# Create a blueprint for reports
reports_bp = Blueprint('reports_bp', __name__)

# Route to view reports for the logged-in patient
@reports_bp.route('/reports')
def view_reports():
    from app import db
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))  # Redirect if not logged in

    user_id = session['user_id']
    
    # Fetch reports related to the logged-in patient from MongoDB
    patient_reports = db.reports.find({"patient_id": ObjectId(user_id)})
    
    # Convert MongoDB cursor to list
    reports_list = list(patient_reports)

    # Render the template with the patient's reports
    return render_template('reports.html', reports=reports_list)

# Route for submitting reports (could be for an admin interface)
@reports_bp.route('/submit_report', methods=['POST'])
def submit_report():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))  # Ensure user is logged in

    # Get the form data (this could come from a form or API request)
    patient_id = request.form.get('patient_id')  # Patient ID
    report_type = request.form.get('report_type')
    doctor = request.form.get('doctor')
    test_result = request.form.get('test_result')

    # Optional: if file upload (e.g., PDF report)
    file = request.files.get('file')
    file_path = None
    if file:
        # Save the file somewhere and get its path
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

    # Read data from a file ('data_file.txt') and process it
    try:
        with open('data_file.txt', 'r', encoding='utf-8', errors='ignore') as data_file:
            data = data_file.read()  # Read all content from the file

            # Process data (this is an example of processing)
            # You can tailor this logic to your specific needs
            processed_data = data.splitlines()  # Example: Split into lines if it's text data

            # Insert each line from the file into the database or use it as needed
            for line in processed_data:
                # Assuming each line contains report-related data, you might process it as needed
                report = {
                    "patient_id": ObjectId(patient_id),
                    "report_type": report_type,
                    "date": "2024-12-01",  # You can generate dynamic dates
                    "doctor": doctor,
                    "test_result": test_result,
                    "file_path": file_path,
                    "line_data": line  # Store the data from the file
                }
                # Insert into the 'reports' collection
                db.reports.insert_one(report)

        return jsonify({"message": "Report submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500