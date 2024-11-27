from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = '*********'
app.config['MYSQL_USER'] = '******'
app.config['MYSQL_PASSWORD'] = '*********'
app.config['MYSQL_DB'] = '*************'

mysql = MySQL(app)

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

def categorize_temperature(temperature):
    if temperature <= 34:
        return "hypothermia"
    elif 35 <= temperature <= 38:
        return "normal"
    else:
        return "hyperthermia"

def categorize_age(age):
    if age <= 12:
        return "child"
    elif 13 <= age <= 24:
        return "adolescent"
    else:
        return "adult"

def categorize_weight(weight):
    if weight <= 20:
        return "0 - 20"
    elif 21 <= weight <= 40:
        return "21 - 40"
    elif 41 <= weight <= 100:
        return "41 - 100"
    else:
        return "101 - Above"

def categorize_respiration_rate(respiration_rate):
    if respiration_rate <= 14:
        return "Hypoxy"
    elif 15 <= respiration_rate <= 30:
        return "normal"
    else:
        return "Acidity"

def load_patients():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patients")
    patients_data = cursor.fetchall()
    cursor.close()
    patients = []
    for data in patients_data:
        patients.append(Patient(
            name=data[1], age=data[2], weight=data[3], temperature=data[4], 
            respiration_rate=data[5], service=data[6], hospital=data[7], 
            doctor=data[8], medicine=data[9]
        ))
    return patients

def save_patient(patient):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, weight, temperature, respiration_rate, service, hospital, doctor, medicine) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        patient.name, patient.age, patient.weight, patient.temperature, 
        patient.respiration_rate, patient.service, patient.hospital, 
        patient.doctor, patient.medicine
    ))
    mysql.connection.commit()
    cursor.close()

def suggest_medicine(patients, new_patient):
    temperature_category = categorize_temperature(new_patient.temperature)
    age_category = categorize_age(new_patient.age)
    weight_category = categorize_weight(new_patient.weight)
    respiration_rate_category = categorize_respiration_rate(new_patient.respiration_rate)
    for patient in patients:
        if (categorize_temperature(patient.temperature) == temperature_category and
            categorize_weight(patient.weight) == weight_category and
            categorize_respiration_rate(patient.respiration_rate) == respiration_rate_category and
            categorize_age(patient.age) == age_category):
            if patient.medicine:
                new_patient.medicine = patient.medicine
                return
    new_patient.medicine = request.form.get('medicine')
    save_patient(new_patient)

@app.route('/', methods=['GET', 'POST'])
def get_patient_data():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        temperature = float(request.form['temperature'])
        respiration_rate = int(request.form['respiration_rate'])
        service = request.form['service']
        hospital = request.form['hospital']
        doctor = request.form['doctor']
        medicine = request.form.get('medicine', '')

        new_patient = Patient(name, age, weight, temperature, respiration_rate, service, hospital, doctor, medicine)
        patients = load_patients()
        suggest_medicine(patients, new_patient)
        save_patient(new_patient)
        return redirect(url_for('patient_list'))
    return render_template('patient_form.html')

@app.route('/patients')
def patient_list():
    patients = load_patients()
    return render_template('patient_list.html', patients=patients)

# API Endpoints
@app.route('/api/patients', methods=['POST'])
def api_create_patient():
    data = request.json
    new_patient = Patient(**data)
    save_patient(new_patient)
    return jsonify(new_patient.to_dict()), 201

@app.route('/api/patients', methods=['GET'])
def api_get_patients():
    patients = load_patients()
    return jsonify([patient.to_dict() for patient in patients])

@app.route('/api/patients/<id>', methods=['GET'])
def api_get_patient(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
    data = cursor.fetchone()
    cursor.close()
    if data:
        patient = Patient(
            name=data[1], age=data[2], weight=data[3], temperature=data[4], 
            respiration_rate=data[5], service=data[6], hospital=data[7], 
            doctor=data[8], medicine=data[9]
        )
        return jsonify(patient.to_dict())
    return jsonify({"error": "Patient not found"}), 404

@app.route('/api/patients/<id>', methods=['PUT'])
def api_update_patient(id):
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE patients SET name=%s, age=%s, weight=%s, temperature=%s, 
        respiration_rate=%s, service=%s, hospital=%s, doctor=%s, medicine=%s
        WHERE id=%s
    """, (
        data['name'], data['age'], data['weight'], data['temperature'], 
        data['respiration_rate'], data['service'], data['hospital'], 
        data['doctor'], data['medicine'], id
    ))
    mysql.connection.commit()
    cursor.close()
    return jsonify(data)

@app.route('/api/patients/<id>', methods=['DELETE'])
def api_delete_patient(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM patients WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"message": "Patient deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)

