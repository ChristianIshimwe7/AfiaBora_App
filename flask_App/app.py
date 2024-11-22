# app.py

from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['medical_db']
collection = db['patients']

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
    patients_data = collection.find()
    return [Patient(**data) for data in patients_data]

def save_patient(patient):
    collection.insert_one(patient.to_dict())

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
            print(f"Patient {new_patient.name} matches with previous patient {patient.name}.")
            if patient.medicine:
                print(f"Suggested medicine: {patient.medicine}")
                new_patient.medicine = patient.medicine
                return
    new_patient.medicine = input("No matching records found. Enter medicine suggestion for the new patient: ")
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
        new_patient = Patient(name, age, weight, temperature, respiration_rate, service, hospital, doctor)
        patients = load_patients()
        suggest_medicine(patients, new_patient)
        save_patient(new_patient)
        return redirect(url_for('patient_list'))
    return render_template('patient_form.html')

@app.route('/patients')
def patient_list():
    patients = load_patients()
    return render_template('patient_list.html', patients=patients)

if __name__ == "__main__":
    app.run(debug=True)
