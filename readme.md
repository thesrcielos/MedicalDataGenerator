# Bogotá Medical Data Generator

A Python-based synthetic medical data generator that creates realistic (but fictional) patient records for Bogotá, Colombia. Designed for testing healthcare applications, academic research, and data analysis projects while maintaining privacy compliance.

## Features

- **Demographic Data**: Names, ages, genders with Colombian distributions
- **Medical Metrics**: Weight, height, BMI, blood pressure (age-adjusted)
- **Clinical Data**: 
  - Symptoms with ICD-10 coded diagnoses
  - Chronic conditions (hypertension, diabetes, asthma)
- **Geographical Context**:
  - Real Bogotá hospitals with addresses
  - Accurate district distribution
- **Socioeconomic Factors**:
  - Income levels matching Bogotá's distribution
  - Healthcare provider probabilities

## Installation

```bash
pip install -r requirements.txt

from medical_generator import BogotaMedicalGenerator

# Initialize generator
generator = BogotaMedicalGenerator()

# Generate single patient
patient = generator.generate_patient()

# Generate 1000-patient dataset
import pandas as pd
records = [generator.generate_patient() for _ in range(1000)]
df = pd.DataFrame(records)

# Export to CSV
df.to_csv('bogota_patients.csv', index=False, encoding='utf-8-sig')
````
## Data Dictionary

| Field                  | Type    | Description                          | Example               |
|------------------------|---------|--------------------------------------|-----------------------|
| `ID_Paciente`          | string  | Unique patient ID                    | `"a5b8c2"`            |
| `Nombre`               | string  | Full name                            | `"María González"`    |
| `Género`               | string  | M/F                                  | `"F"`                 |
| `Edad`                 | int     | Age in years                         | `42`                  |
| `Peso (kg)`            | float   | Weight                               | `68.5`                |
| `Altura (cm)`          | int     | Height                               | `165`                 |
| `IMC`                  | float   | Body Mass Index                      | `24.8`                |
| `Presión Arterial`     | string  | Blood pressure                       | `"120/80 mmHg"`       |
| `Síntomas`             | string  | Comma-separated symptoms             | `"Fiebre, Tos"`       |
| `Diagnóstico (CIE-10)` | string  | ICD-10 code + description            | `"A90 - Dengue"`      |
| `Enfermedades Crónicas`| string  | Chronic conditions                   | `"Hipertensión"`      |
| `Fecha Consulta`       | string  | Consultation date (DD/MM/YYYY)       | `"15/03/2023"`        |
| `Hospital`             | string  | Hospital name                        | `"Hospital San Ignacio"` |
| `Dirección Hospital`   | string  | Full address                         | `"Cra. 7 #40-62"`     |
| `Localidad`            | string  | Bogotá district                      | `"Santa Fe"`          |
| `Nivel Socioeconómico` | string  | Income level (Bajo/Medio/Alto)       | `"Medio"`             |
| `Seguro Médico`        | string  | Health insurance provider            | `"EPS Sura"`          |

## Example Data

| #Fila | ID_Paciente | Nombre                             | Género | Edad | Peso (kg) | Altura (cm) | IMC  | Presión Arterial | Síntomas                                      | Diagnóstico (CIE-10)                | Enfermedades Crónicas           | Fecha Consulta | Hospital                  | Dirección Hospital      | Localidad | Nivel Socioeconómico | Seguro Médico |
|-------|-------------|------------------------------------|--------|------|-----------|-------------|------|-------------------|-----------------------------------------------|--------------------------------------|-------------------------------|----------------|---------------------------|-------------------------|-----------|-----------------------|---------------|
| 1     | b1c42740    | Luz Mayra Restrepo                | F      | 20   | 81.8      | 180         | 25.1 | 116/81 mmHg       | Chequeo rutinario                            | Z00.0 - Examen médico general        | Ninguna                       | 2023-04-05     | Clínica Colsubsidio       | Calle 26 #69A-40        | Engativá  | Medio                 | Coomeva       |
| 2     | dc680dd5    | Nohora Carolina Cardona Perdomo   | F      | 45   | 77.1      | 169         | 26.9 | 118/70 mmHg       | Chequeo rutinario                            | Z00.0 - Examen médico general        | Ninguna                       | 2023-05-05     | Clínica Bogotá            | Calle 63 #24-09         | Kennedy   | Bajo                  | SISBÉN        |
| 3     | 566dcee1    | Bernardo Antonio Ortiz            | M      | 55   | 68.9      | 179         | 21.5 | 125/73 mmHg       | Dolor de cabeza                              | I10 - Hipertensión esencial          | Hipertensión                  | 2023-06-17     | Hospital San Ignacio      | Cra. 7 #40-62           | Santa Fe  | Bajo                  | EPS Sura      |
| 4     | 6914db84    | Alejandra Martínez                | F      | 67   | 55.1      | 164         | 20.3 | 123/74 mmHg       | Dolor de cabeza                              | R51 - Cefalea                        | Asma                          | 2023-06-26     | Clínica Colsubsidio       | Calle 26 #69A-40        | Engativá  | Bajo                  | SISBÉN        |
| 5     | 1ba0992b    | Enrique Romero Chacón             | M      | 41   | 98.3      | 171         | 33.4 | 130/79 mmHg       | Fiebre, Dolor de cabeza                      | G43.9 - Migraña                      | Hipertensión, Diabetes tipo 2 | 2023-07-01     | Hospital Militar Central  | Cra. 50 #18-09          | Suba      | Bajo                  | Nueva EPS     |
| 6     | 48d127e6    | Arturo Pérez Muñoz                | M      | 40   | 93.1      | 169         | 32.3 | 140/65 mmHg       | Dolor de cabeza                              | R51 - Cefalea                        | Hipertensión                  | 2023-07-23     | Clínica Colsubsidio       | Calle 26 #69A-40        | Engativá  | Alto                  | Nueva EPS     |
| 7     | 3b906155    | Yuly Duque                        | F      | 28   | 63.0      | 172         | 21.3 | 106/67 mmHg       | Tos persistente                              | J20.9 - Bronquitis aguda             | Asma                          | 2023-07-27     | Hospital San Ignacio      | Cra. 7 #40-62           | Santa Fe  | Bajo                  | SISBÉN        |
| 8     | 7ab70747    | Álvaro Jorge Cardona Torres       | M      | 23   | 68.3      | 174         | 22.4 | 128/70 mmHg       | Fiebre                                       | A15.0 - Gripe viral                  | Ninguna                       | 2023-08-07     | Hospital Militar Central  | Cra. 50 #18-09          | Suba      | Bajo                  | Nueva EPS     |
| 9     | 2ccee2fc    | Elizabeth Díaz Silva              | F      | 15   | 69.6      | 170         | 23.9 | 142/75 mmHg       | Fiebre                                       | A92.0 - Chikungunya                  | Ninguna                       | 2023-08-12     | Hospital San Ignacio      | Cra. 7 #40-62           | Santa Fe  | Medio                 | EPS Sura      |
| 10    | f58472d1    | Diana Mejía Gonzáles              | F      | 56   | 66.6      | 170         | 22.9 | 111/74 mmHg       | Dolor de cabeza                              | I10 - Hipertensión esencial          | Ninguna                       | 2023-10-05     | Hospital Militar Central  | Cra. 50 #18-09          | Suba      | Bajo                  | Sanitas       |
| 11    | 0a16a7e9    | Michel Myriam Álvarez             | F      | 24   | 63.1      | 179         | 19.6 | 123/66 mmHg       | Fiebre, Tos persistente, Dolor de cabeza     | G43.9 - Migraña                      | Ninguna                       | 2023-10-11     | Hospital Militar Central  | Cra. 50 #18-09          | Suba      | Medio                 | SISBÉN        |
| 12    | 19575961    | Tatiana Lida Díaz Escobar         | F      | 46   | 51.4      | 158         | 20.6 | 125/77 mmHg       | Tos persistente                              | J20.9 - Bronquitis aguda             | Asma                          | 2023-10-14     | Fundación Santa Fe        | Cra. 7 #117-15          | Chapinero | Medio                 | Sanitas       |
| 13    | e83ed4f7    | Carlos Henao                      | M      | 29   | 62.9      | 164         | 23.3 | 136/78 mmHg       | Chequeo rutinario                            | Z00.0 - Examen médico general        | Ninguna                       | 2023-10-18     | Hospital San Ignacio      | Cra. 7 #40-62           | Santa Fe  | Alto                  | SISBÉN        |
| 14    | a8e0e699    | Omaira Vásquez                    | F      | 15   | 71.0      | 160         | 27.6 | 128/72 mmHg       | Chequeo rutinario                            | Z00.0 - Examen médico general        | Ninguna                       | 2023-10-19     | Clínica Colsubsidio       | Calle 26 #69A-40        | Engativá  | Bajo                  | EPS Sura      |

## Medical Realism

- **Blood pressure**: Calculated using age and BMI-adjusted formulas  
  _Example: Systolic = 110 + (age/30) + (BMI/2)_
  
- **Diagnoses**: Probability-weighted by age groups  
  ```python
  age_probability: {'<18': 0.35, '18-60': 0.25, '>60': 0.15}
    Chronic diseases: Prevalence matches Colombian epidemiology
        Hypertension (25%)
        Diabetes (15%)
        Asthma (10%)
    Hospitals: Real institutions with correct district mapping
        Verified addresses from Bogotá's health registry
# Customization
Modify these variables in the code:

## Symptoms and diagnoses
symptoms_diagnoses = {
    'Fiebre': {
        'diagnoses': [('A15.0', 'Gripe viral'), ...],
        'age_probability': {'<18': 0.3, '18-60': 0.5, '>60': 0.2}
    }
}

## Chronic disease parameters
```python 
chronic_diseases = {
    'Hipertensión': {'age_range': (40, 100), 'probability': 0.25}
}

# Hospital database
HOSPITALS_BOGOTA = {
    'Hospital San Ignacio': {'address': 'Cra. 7 #40-62', 'district': 'Santa Fe', ...}
} 
````

## Test Coverage

| File                             | Statements | Missed | Coverage |
|----------------------------------|------------|--------|----------|
| `algoritmhs/__init__.py`         | 0          | 0      | 100%     |
| `algoritmhs/data_generator.py`   | 46         | 0      | 100%     |
| `test/__init__.py`               | 0          | 0      | 100%     |
| `test/test_data_generator.py`    | 67         | 1      | 99%      |
| **TOTAL**                        | 113        | 1      | **99%**  |

## Limitations ⚠️
### **Synthetic Data**
- 🚫 Not real patient records  
- 🧪 For testing/development only  
- 🔒 Contains no actual PHI (Protected Health Information)
### **Language Support**  
- 🇪🇸 Spanish-only output:  
  - Names (Colombian Spanish)  
  - Medical diagnoses (local terminology)  
  - Addresses (Bogotá format)
### **Geographical Scope**  
- 📍 Bogotá-specific healthcare system:  
  - Hospital network covers only 12 districts  
  - Insurance providers reflect local market (SISBÉN, EPS Sura, etc.)  
  - Does not include rural healthcare facilities
  
### License

MIT License - Free for academic and commercial use