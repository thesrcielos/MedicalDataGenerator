import random
from faker import Faker
import numpy as np

fake = Faker('es_CO')  
random.seed(42)
np.random.seed(42)

BOGOTA_DISTRICTS = [
    'Usaquén', 'Chapinero', 'Santa Fe', 'La Candelaria',
    'Suba', 'Engativá', 'Kennedy', 'Fontibón', 'Bosa',
    'San Cristóbal', 'Rafael Uribe Uribe', 'Ciudad Bolívar'
]

HOSPITALS_BOGOTA = {
    'Hospital San Ignacio': {'address': 'Cra. 7 #40-62', 'district': 'Santa Fe'},
    'Clínica Colsubsidio': {'address': 'Calle 26 #69A-40', 'district': 'Engativá'},
    'Fundación Santa Fe': {'address': 'Cra. 7 #117-15', 'district': 'Chapinero'},
    'Hospital Militar Central': {'address': 'Cra. 50 #18-09', 'district': 'Suba'},
    'Clínica Bogotá': {'address': 'Calle 63 #24-09', 'district': 'Kennedy'}
}

class BogotaMedicalGenerator:
    def __init__(self):
        self.symptoms_diagnoses = {
            'Fiebre': {
                'diagnoses': [
                    ('A15.0', 'Gripe viral'), 
                    ('A90', 'Dengue'),
                    ('A92.0', 'Chikungunya') 
                ],
                'age_probability': {'<18': 0.35, '18-60': 0.25, '>60': 0.15}
            },
            'Tos persistente': {
                'diagnoses': [
                    ('J20.9', 'Bronquitis aguda'), 
                    ('J18.9', 'Neumonía'),
                    ('J45.9', 'Asma')
                ],
                'age_probability': {'<18': 0.25, '18-60': 0.35, '>60': 0.40}
            },
            'Dolor de cabeza': {
                'diagnoses': [
                    ('G43.9', 'Migraña'), 
                    ('I10', 'Hipertensión esencial'), 
                    ('R51', 'Cefalea')
                ],
                'age_probability': {'<18': 0.15, '18-60': 0.30, '>60': 0.25}
            }
        }
        
        self.chronic_diseases = {
            'Hipertensión': {'age_range': (40, 100), 'probability': 0.25},
            'Diabetes tipo 2': {'age_range': (30, 100), 'probability': 0.15},
            'Asma': {'age_range': (5, 70), 'probability': 0.10}
        }

    def generate_age(self):
        return int(np.clip(np.random.normal(35, 15), 15, 100))

    def generate_blood_pressure(self, age, bmi):
        base_systolic = 110 + (age / 30) + (bmi / 2)
        base_diastolic = 70 + (age / 40) + (bmi / 4)
        
        systolic = np.clip(np.random.normal(base_systolic, 8), 90, 180)
        diastolic = np.clip(np.random.normal(base_diastolic, 5), 60, 120)
        
        return f"{int(systolic)}/{int(diastolic)} mmHg"

    def generate_symptoms_diagnosis(self, age):
        symptoms = []
        for symptom, data in self.symptoms_diagnoses.items():
            age_group = '<18' if age < 18 else '18-60' if age <=60 else '>60'
            if random.random() < data['age_probability'][age_group]:
                symptoms.append(symptom)
        
        if not symptoms:
            symptoms.append('Chequeo rutinario')
            return symptoms, ('Z00.0', 'Examen médico general'), False
        
        main_symptom = random.choice(symptoms)
        code, diagnosis = random.choice(self.symptoms_diagnoses[main_symptom]['diagnoses'])
        
        # Add chronic diseases
        chronic = []
        for disease, params in self.chronic_diseases.items():
            if age >= params['age_range'][0] and random.random() < params['probability']:
                chronic.append(disease)
        
        return symptoms, (code, diagnosis), chronic

    def generate_patient(self):
        gender = random.choice(['M', 'F'])
        age = self.generate_age()
        weight = np.clip(np.random.normal(70, 15), 45, 120)
        height = np.clip(np.random.normal(170, 9), 150, 200)
        bmi = weight / ((height/100) ** 2)
        
        symptoms, diagnosis, chronic = self.generate_symptoms_diagnosis(age)
        blood_pressure = self.generate_blood_pressure(age, bmi)
        
        hospital = random.choice(list(HOSPITALS_BOGOTA.keys()))
        
        return {
            'ID_Paciente': fake.uuid4()[:8],
            'Nombre': fake.name_female() if gender == 'F' else fake.name_male(),
            'Género': gender,
            'Edad': age,
            'Peso (kg)': round(weight, 1),
            'Altura (cm)': int(height),
            'IMC': round(bmi, 1),
            'Presión Arterial': blood_pressure,
            'Síntomas': ', '.join(symptoms),
            'Diagnóstico (CIE-10)': f"{diagnosis[0]} - {diagnosis[1]}",
            'Enfermedades Crónicas': ', '.join(chronic) if chronic else 'Ninguna',
            'Fecha Consulta': fake.date_between(start_date='-2y').strftime("%d/%m/%Y"),
            'Hospital': hospital,
            'Dirección Hospital': HOSPITALS_BOGOTA[hospital]['address'],
            'Localidad': HOSPITALS_BOGOTA[hospital]['district'],
            'Nivel Socioeconómico': random.choices(
                                        population=['Bajo', 'Medio', 'Alto'],
                                        weights=[0.55, 0.35, 0.10],
                                        k=1
                                    )[0],
            'Seguro Médico': random.choices(
                                        population=[
                                            'SISBÉN', 
                                            'EPS Sura', 
                                            'Sanitas', 
                                            'Nueva EPS', 
                                            'Salud Total', 
                                            'Coomeva', 
                                            'Particular'
                                        ],
                                        weights=[0.42, 0.15, 0.12, 0.18, 0.07, 0.04, 0.02], 
                                        k=1
                                    )[0]
        }

