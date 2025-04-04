import unittest
from unittest.mock import patch
import numpy as np
import random
from algoritmhs import data_generator 

class TestDataGenerator(unittest.TestCase):
    def setUp(self):
        """Initial setup for each test"""
        self.generator = data_generator.BogotaMedicalGenerator()
        random.seed(42)
        np.random.seed(42)

    def test_generate_age_range(self):
        "Verifies that the generated age is within the valid range"
        for _ in range(1000):
            age = self.generator.generate_age()
            self.assertTrue(15 <= age <= 100, f"Edad {age} fuera de rango")

    def test_generate_age_distribution(self):
        "Verifies that the age distribution is approximately normal"
        ages = [self.generator.generate_age() for _ in range(1000)]
        mean_age = np.mean(ages)
        self.assertAlmostEqual(mean_age, 35, delta=5, msg=f"Media de edad {mean_age} no cercana a 35")

    def test_blood_pressure_ranges(self):
        "Verifies valid blood pressure ranges for different cases"
        # Adulto joven con IMC normal
        bp = self.generator.generate_blood_pressure(25, 22)
        systolic, diastolic = bp.split('/')
        systolic = int(systolic)
        diastolic = int(diastolic.split(" ")[0])
        self.assertTrue(90 <= systolic <= 140)
        self.assertTrue(60 <= diastolic <= 90)

        # Adulto mayor con sobrepeso
        bp = self.generator.generate_blood_pressure(70, 30)
        systolic, diastolic = bp.split('/')
        systolic = int(systolic)
        diastolic = int(diastolic.split(" ")[0])
        self.assertTrue(120 <= systolic <= 180)
        self.assertTrue(70 <= diastolic <= 120)

    def test_symptoms_diagnosis_structure(self):
        "Verifies the return structure of symptoms and diagnoses"
        for age in [10, 30, 70]:  # Prueba diferentes grupos etarios
            symptoms, (code, diagnosis), chronic = self.generator.generate_symptoms_diagnosis(age)
            self.assertIsInstance(symptoms, list)
            self.assertTrue(all(isinstance(s, str) for s in symptoms))
            self.assertIsInstance(code, str)
            self.assertIsInstance(diagnosis, str)

    def test_patient_structure(self):
        "Verifies the complete structure of the generated patient"
        patient = self.generator.generate_patient()
        required_fields = [
            'ID_Paciente', 'Nombre', 'Género', 'Edad', 'Peso (kg)', 
            'Altura (cm)', 'IMC', 'Presión Arterial', 'Síntomas',
            'Diagnóstico (CIE-10)', 'Enfermedades Crónicas', 'Fecha Consulta',
            'Hospital', 'Dirección Hospital', 'Localidad',
            'Nivel Socioeconómico', 'Seguro Médico'
        ]
        for field in required_fields:
            self.assertIn(field, patient)

    def test_patient_values(self):
        "Verifies specific values of the generated patient"
        patient = self.generator.generate_patient()
        self.assertIn(patient['Género'], ['M', 'F'])
        self.assertIn(patient['Localidad'], data_generator.BOGOTA_DISTRICTS)
        self.assertIn(patient['Hospital'], data_generator.HOSPITALS_BOGOTA.keys())

    def test_socioeconomic_distribution(self):
        "Verifies the distribution of socioeconomic levels"
        levels = [self.generator.generate_patient()['Nivel Socioeconómico'] for _ in range(1000)]
        low_count = levels.count('Bajo')
        self.assertAlmostEqual(low_count / 1000, 0.55, delta=0.05)

    def test_health_insurance_distribution(self):
        "Verifies the distribution of medical insurance"
        insurance = [self.generator.generate_patient()['Seguro Médico'] for _ in range(1000)]
        sisben_count = insurance.count('SISBÉN')
        self.assertAlmostEqual(sisben_count / 1000, 0.42, delta=0.05)

    @patch('random.random', return_value=0.1)
    def test_deterministic_symptoms(self, mock_random):
        "Verifies deterministic generation with mock"
        _, (code, diagnosis), _ = self.generator.generate_symptoms_diagnosis(30)
        self.assertIsNotNone(code)
        self.assertIsNotNone(diagnosis)

    def test_chronic_diseases_by_age(self):
        "Verifies the occurrence of chronic diseases by age"
        _, _, young_chronic = self.generator.generate_symptoms_diagnosis(20)
        _, _, old_chronic = self.generator.generate_symptoms_diagnosis(70)
        self.assertGreaterEqual(len(old_chronic), len(young_chronic))

if __name__ == '__main__':
    unittest.main()