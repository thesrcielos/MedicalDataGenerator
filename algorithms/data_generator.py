import random
from faker import Faker
import numpy as np
from algorithms.data import symptoms_diagnoses, chronic_diseases, HOSPITALS_BOGOTA

fake = Faker('es_CO')  
random.seed(42)

class BogotaMedicalGenerator:      
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
            height = np.clip(np.random.normal(mean_height - 8, std_dev), 140, 185)
        elif age >= 18 and age <= 40:
            height = np.clip(np.random.normal(mean_height, std_dev * 0.8), 145, 200)
        elif age > 40 and age <= 60:
            height = np.clip(np.random.normal(mean_height, std_dev * 0.6), 145, 200)
        else:
            height = np.clip(np.random.normal(mean_height - 2, std_dev * 0.6), 145, 200)

        return round(height, 1)

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

        return round(estimated_weight, 1)
    
    def generate_age(self):
        return int(np.clip(np.random.normal(35, 15), 15, 100))

    def generate_blood_pressure(self, age, bmi):
        base_systolic = 110 + (age / 30) + (bmi / 2)
        base_diastolic = 70 + (age / 40) + (bmi / 4)
        
        systolic = np.clip(np.random.normal(base_systolic, 8), 90, 180)
        diastolic = np.clip(np.random.normal(base_diastolic, 5), 60, 120)
        
        return f"{int(systolic)}/{int(diastolic)} mmHg"

    def get_bmi_category(self, bmi):
        if bmi < 18.5: return 'Underweight'
        elif 18.5 <= bmi < 25: return 'Normal'
        elif 25 <= bmi < 30: return 'Overweight'
        else: return 'Obese'

    def generate_symptoms_diagnosis(self, age, bmi):
        bmi_category = self.get_bmi_category(bmi)
        age_group = '<18' if age < 18 else '18-60' if age <=60 else '>60'
        symptoms = []
        for symptom, data in symptoms_diagnoses.items():
            base_prob = data['age_probability'][age_group]
            bmi_factor = data.get('bmi_factor', {}).get(bmi_category, 1.0)
            adjusted_prob = base_prob * bmi_factor
            
            if random.random() < adjusted_prob:
                symptoms.append(symptom)

        if not symptoms:
            return (
                ['Chequeo rutinario'],
                ('Z00.0', 'Examen médico general'),
                []
            )

        main_symptom = random.choice(symptoms)
        diagnoses = symptoms_diagnoses[main_symptom]['diagnoses']
        
        if 'bmi_diagnosis_weights' in symptoms_diagnoses[main_symptom]:
            weights = [
                symptoms_diagnoses[main_symptom]['bmi_diagnosis_weights'].get(
                    code[0], 1.0
                ) for code, _ in diagnoses
            ]
            selected_diagnosis = random.choices(diagnoses, weights=weights, k=1)[0]
        else:
            selected_diagnosis = random.choice(diagnoses)

        return (
            symptoms,
            selected_diagnosis,
            self.generate_chronic_conditions(age, bmi)
        )

    def generate_chronic_conditions(self, age, bmi):
        bmi_category = self.get_bmi_category(bmi)
        chronic = []
        for disease, params in chronic_diseases.items():
            if age >= params['age_range'][0]:
                base_prob = params['base_probability']
                bmi_multiplier = params['bmi_multipliers'].get(bmi_category, 1.0)
                if random.random() < (base_prob * bmi_multiplier):
                    chronic.append(disease)
        return chronic

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
        
        symptoms, diagnosis, chronic = self.generate_symptoms_diagnosis(age, bmi)
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