from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from bson.objectid import ObjectId

health_records_bp = Blueprint('health_records', __name__)

@health_records_bp.route('/records/<patient_id>', methods=['GET'])
def get_health_records(patient_id):
    """Retrieve all health records for a specific patient."""
    records = list(request.app.config['db']['health_records'].find({"patient_id": ObjectId(patient_id)}))
    return render_template('health_records.html', records=records, patient_id=patient_id)

@health_records_bp.route('/records/<patient_id>/add', methods=['GET', 'POST'])
def add_health_record(patient_id):
    """Add a new health record."""
    if request.method == 'GET':
        return render_template('add_health_record.html', patient_id=patient_id)
    
    # Handle POST request
    data = request.form
    new_record = {
        "patient_id": ObjectId(patient_id),
        "visit_date": data.get('visit_date'),
        "symptoms": data.getlist('symptoms'),
        "test_results": [],
        "diagnosis": data.get('diagnosis'),
        "treatment": data.get('treatment'),
        "notes": data.get('notes')
    }
    request.app.config['db']['health_records'].insert_one(new_record)
    return redirect(url_for('health_records.get_health_records', patient_id=patient_id))

@health_records_bp.route('/records/<record_id>/add-test', methods=['POST'])
def add_test_result(record_id):
    """Add a test result to an existing health record."""
    data = request.form
    test_result = {
        "test_name": data.get('test_name'),
        "result": data.get('result'),
        "date": data.get('date')
    }
    request.app.config['db']['health_records'].update_one(
        {"_id": ObjectId(record_id)},
        {"$push": {"test_results": test_result}}
    )
    return redirect(url_for('health_records.get_health_records', patient_id=data.get('patient_id')))
