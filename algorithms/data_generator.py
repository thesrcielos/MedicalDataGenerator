import random
from faker import Faker
import numpy as np

fake = Faker('es_CO')  
random.seed(42)

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
            # Existing symptoms
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
            },
            
            'Dolor abdominal': {
                'diagnoses': [
                    ('K35', 'Apendicitis aguda'),
                    ('K29.7', 'Gastritis'),
                    ('N20.0', 'Cálculo renal')
                ],
                'age_probability': {'<18': 0.20, '18-60': 0.35, '>60': 0.25}
            },
            'Mareos': {
                'diagnoses': [
                    ('I95.1', 'Hipotensión ortostática'),
                    ('H81.4', 'Vértigo central'),
                    ('R55', 'Síncope')
                ],
                'age_probability': {'<18': 0.10, '18-60': 0.20, '>60': 0.35}
            },
            'Dificultad respiratoria': {
                'diagnoses': [
                    ('J44.9', 'EPOC'),
                    ('I50.9', 'Insuficiencia cardíaca'),
                    ('J45.0', 'Asma alérgica')
                ],
                'age_probability': {'<18': 0.15, '18-60': 0.25, '>60': 0.40}
            }
        }

        self.chronic_diseases = {
            'Hipertensión': {'age_range': (40, 100), 'probability': 0.25},
            'Diabetes tipo 2': {'age_range': (30, 100), 'probability': 0.15},
            'Asma': {'age_range': (5, 70), 'probability': 0.10},
            
            'Enfermedad coronaria': {
                'age_range': (50, 100),
                'probability': 0.18  
            },
            'Artritis reumatoide': {
                'age_range': (30, 80),
                'probability': 0.08  
            },
            'Enfermedad renal crónica': {
                'age_range': (40, 100),
                'probability': 0.12  
            },
            'Epilepsia': {
                'age_range': (5, 70),
                'probability': 0.05  
            },
            'Cáncer de pulmón': {
                'age_range': (40, 100),
                'probability': 0.005
            }
        }

    def generate_height(self,age,gender):
        if gender == 'M':
            mean_height = 171
            std_dev = 9
        elif gender == 'F':
            mean_height = 158
            std_dev = 9
        else:
            return None  

        if age < 18:
            height = np.clip(np.random.normal(mean_height - 5, std_dev), 140, 190)
        elif age >= 18 and age <= 40:
            height = np.clip(np.random.normal(mean_height, std_dev * 0.8), 145, 200)
        elif age > 40 and age <= 60:
            height = np.clip(np.random.normal(mean_height, std_dev * 0.6), 145, 200)
        else:
            height = np.clip(np.random.normal(mean_height - 2, std_dev * 0.6), 145, 200)

        return round(height, 2)

    def generate_weight(self, age, sex, height):
        ideal_weight = height - 100
        if age < 18:
            ideal_weight *= np.random.normal(0.9, 0.2)
        elif age > 60:
            ideal_weight *= np.random.normal(0.85, 0.15)  

        if sex == 'M':
            ideal_weight *= np.random.normal(1.1, 0.2)  
        elif sex == 'F':
            ideal_weight *= np.random.normal(0.9, 0.2)

        randomness_factor = np.random.uniform(0.90, 1.10)
        estimated_weight = ideal_weight * randomness_factor

        return round(estimated_weight, 2)
    
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
        age_group = '<18' if age < 18 else '18-60' if age <=60 else '>60'
        for symptom, data in self.symptoms_diagnoses.items():
            if random.random() < data['age_probability'][age_group]:
                symptoms.append(symptom)
        
        if not symptoms:
            symptoms.append('Chequeo rutinario')
            return symptoms, ('Z00.0', 'Examen médico general'), []  # Fixed
        
        main_symptom = random.choice(symptoms)
        code, diagnosis = random.choice(self.symptoms_diagnoses[main_symptom]['diagnoses'])
        
        chronic = []
        for disease, params in self.chronic_diseases.items():
            if age >= params['age_range'][0] and random.random() <= params['probability']:
                chronic.append(disease)
        
        return symptoms, (code, diagnosis), chronic

    def generate_health_insurance(self):
        return random.choices(population=[
            'SISBÉN', 
            'EPS Sura', 
            'Sanitas', 
            'Nueva EPS', 
            'Salud Total', 
            'Coomeva', 
            'Particular'],
            weights=[0.42, 0.15, 0.12, 0.18, 0.07, 0.04, 0.02], 
            k=1)[0]
    
    def generate_socioeconomic_level(self):
        return random.choices(population=['Bajo', 'Medio', 'Alto'],
            weights=[0.55, 0.35, 0.10],
            k=1)[0]
    
    def generate_patient(self):
        gender = random.choice(['M', 'F'])
        age = self.generate_age()
        height = self.generate_height(age, gender)
        weight = self.generate_weight(age, gender, height)
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
            'Nivel Socioeconómico': self.generate_socioeconomic_level(),
            'Seguro Médico': self.generate_health_insurance()
        }