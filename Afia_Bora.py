import json

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

def print_intro():
    print("**WELCOME TO THE DOCTOR'S MEDICAL PRESCRIPTION SUGGESTION SYSTEM!**")
    print("Rules and Guidelines:")
    print("- Patients falling within certain age ranges will be considered as the same case for medicine suggestion.")
    print("- Otherwise, you will be prompted to enter a new medicine for the new case.")

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

def get_patient_data():
    name = input("Enter patient's name (or 'B' to go back): ")
    if name.upper() == 'B':
        return None
    age = int(input("Enter patient's age (or 'B' to go back): "))
    if str(age).upper() == 'B':
        return None
    weight = float(input("Enter patient's weight (in kg) (or 'B' to go back): "))
    if str(weight).upper() == 'B':
        return None
    temperature = float(input("Enter patient's temperature (in Celsius) (or 'B' to go back): "))
    if str(temperature).upper() == 'B':
        return None
    respiration_rate = int(input("Enter patient's respiration rate (breaths per minute) (or 'B' to go back): "))
    if str(respiration_rate).upper() == 'B':
        return None
    service = input("Enter patient's service (or 'B' to go back): ")
    if service.upper() == 'B':
        return None
    hospital = input("Enter patient's hospital (or 'B' to go back): ")
    if hospital.upper() == 'B':
        return None
    doctor = input("Enter doctor's name for approval (or 'B' to go back): ")
    if doctor.upper() == 'B':
        return None
    return name, age, weight, temperature, respiration_rate, service, hospital, doctor

def load_patients(filename):
    try:
        with open(filename, 'r') as f:
            patients_data = json.load(f)
            return [Patient(**data) for data in patients_data]
    except FileNotFoundError:
        return []

def save_patients(filename, patients):
    with open(filename, 'w') as f:
        json.dump([patient.to_dict() for patient in patients], f)

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
    patients.append(new_patient)

def print_prescription_ticket(patient):
    print("\nPatient data recorded successfully.")
    print("\n**MEDICAL PRESCRIPTION TICKET**")
    print(f"Name: {patient.name}")
    print(f"Age: {patient.age} ({categorize_age(patient.age)})")
    print(f"Temperature: {patient.temperature}°C ({categorize_temperature(patient.temperature)})")
    print(f"Respiration Rate: {patient.respiration_rate} breaths/minute ({categorize_respiration_rate(patient.respiration_rate)})")
    print(f"Weight: {patient.weight}kg ({categorize_weight(patient.weight)})")
    print(f"Medicine: {patient.medicine}")
    print(f"Doctor: {patient.doctor} (Approval)")
    print("\n-----------------------------\n")

def main():
    print_intro()
    filename = 'patients.json'
    patients = load_patients(filename)
    while True:
        start = input("Start using the app? (Y/N): ").upper()
        if start != 'Y':
            print("Thank you, it was a pleasure to have you.")
            break
        patient_data = get_patient_data()
        if not patient_data:
            continue
        name, age, weight, temperature, respiration_rate, service, hospital, doctor = patient_data
        new_patient = Patient(name, age, weight, temperature, respiration_rate, service, hospital, doctor)
        suggest_medicine(patients, new_patient)
        patients.append(new_patient)
        save_patients(filename, patients)
        print_prescription_ticket(new_patient)
        print("Current Patients:")
        for patient in patients:
            print(patient)
        print()

if __name__ == "__main__":
    main()