import unittest
import random
import numpy as np
from unittest.mock import patch
from datetime import datetime
from algorithms import data_generator

class TestBogotaMedicalGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = data_generator.BogotaMedicalGenerator()
        random.seed(42)
        np.random.seed(42)

    def test_generate_age(self):
        ages = [self.generator.generate_age() for _ in range(100)]
        self.assertTrue(all(15 <= age <= 100 for age in ages))
        self.assertAlmostEqual(np.mean(ages), 35, delta=5)

    def test_generate_height(self):
        male_height = self.generator.generate_height(30, 'M')
        female_height = self.generator.generate_height(30, 'F')
        self.assertGreater(male_height, female_height)
        self.assertIsNone(self.generator.generate_height(30, 'X'))

    def test_generate_weight(self):
        weight = self.generator.generate_weight(30, 'M', 175)
        self.assertTrue(50 <= weight <= 120)

    def test_generate_blood_pressure(self):
        bp = self.generator.generate_blood_pressure(30, 22.5)
        systolic_part, diastolic_part = bp.split('/')
        systolic = int(systolic_part)
        diastolic = int(diastolic_part.split()[0])
        self.assertTrue(90 <= systolic <= 180)
        self.assertTrue(60 <= diastolic <= 120)

    def test_symptoms_diagnosis_generation(self):
        for age in [15, 35, 65]:
            symptoms, diagnosis, _ = self.generator.generate_symptoms_diagnosis(age)
            self.assertIsInstance(symptoms, list)

    def test_chronic_disease_distribution(self):
        young_chronic = []
        senior_chronic = []
        for _ in range(100):
            young_chronic.append(len(self.generator.generate_symptoms_diagnosis(25)[2]))
            senior_chronic.append(len(self.generator.generate_symptoms_diagnosis(70)[2]))
        self.assertGreater(np.mean(senior_chronic), np.mean(young_chronic))

    def test_full_patient_generation(self):
        patient = self.generator.generate_patient()
        self.assertIn('Hospital', patient)
        self.assertIn(patient['Hospital'], data_generator.HOSPITALS_BOGOTA)

if __name__ == '__main__':
    unittest.main()