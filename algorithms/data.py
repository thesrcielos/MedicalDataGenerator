HOSPITALS_BOGOTA = {
    'Hospital San Ignacio': {'address': 'Cra. 7 #40-62', 'district': 'Santa Fe'},
    'Clínica Colsubsidio': {'address': 'Calle 26 #69A-40', 'district': 'Engativá'},
    'Fundación Santa Fe': {'address': 'Cra. 7 #117-15', 'district': 'Chapinero'},
    'Hospital Militar Central': {'address': 'Cra. 50 #18-09', 'district': 'Suba'},
    'Clínica Bogotá': {'address': 'Calle 63 #24-09', 'district': 'Kennedy'}
}

symptoms_diagnoses = {
    'Fiebre': {
        'diagnoses': [
            ('A15.0', 'Gripe viral'),
            ('A90',   'Dengue'),
            ('A92.0', 'Chikungunya'),
            ('B34.9', 'Infección viral no especificada'),
        ],
        'age_probability': {
            '<18':   0.35,
            '18-60': 0.25,
            '>60':   0.15,
        },
        'bmi_factor': {
            'Underweight': 1.1,
            'Normal':      1.0,
            'Overweight':  0.9,
            'Obese':       0.8,
        }
    },
    'Tos persistente': {
        'diagnoses': [
            ('J20.9', 'Bronquitis aguda'),
            ('J18.9', 'Neumonía'),
            ('J45.9', 'Asma'),
            ('I50.9', 'Insuficiencia cardíaca'),
            ('J40',   'Bronquitis crónica'),
        ],
        'age_probability': {
            '<18':   0.25,
            '18-60': 0.35,
            '>60':   0.40,
        },
        'bmi_factor': {
            'Underweight': 1.0,
            'Normal':      1.0,
            'Overweight':  1.2,
            'Obese':       1.5,
        }
    },
    'Dolor de cabeza': {
        'diagnoses': [
            ('G43.9', 'Migraña'),
            ('I10',   'Hipertensión esencial'),
            ('R51',   'Cefalea'),
            ('G44.1', 'Cefalea tensional'),
        ],
        'age_probability': {
            '<18':   0.15,
            '18-60': 0.30,
            '>60':   0.25,
        },
        'bmi_factor': {
            # Aplica factor general; si quisieras algo específico por diagnóstico,
            # podrías usar 'bmi_specific' al estilo anterior
            'Underweight': 0.9,
            'Normal':      1.0,
            'Overweight':  1.3,
            'Obese':       1.6,
        }
    },
    'Dificultad respiratoria': {
        'diagnoses': [
            ('J44.9', 'EPOC'),
            ('I50.9', 'Insuficiencia cardíaca'),
            ('J45.0', 'Asma alérgica'),
            ('E66',   'Obesidad'),
            ('J96.9', 'Insuficiencia respiratoria'),
        ],
        'age_probability': {
            '<18':   0.15,
            '18-60': 0.25,
            '>60':   0.40,
        },
        'bmi_factor': {
            'Underweight': 0.8,
            'Normal':      1.0,
            'Overweight':  1.3,
            'Obese':       1.8,
        }
    },
    'Náuseas y vómitos': {
        'diagnoses': [
            ('K52.9', 'Gastroenteritis'),
            ('K21.0', 'Reflujo gastroesofágico'),
            ('R11.0', 'Vómitos'),
        ],
        'age_probability': {
            '<18':   0.30,
            '18-60': 0.20,
            '>60':   0.10,
        },
        'bmi_factor': {
            'Underweight': 1.2,
            'Normal':      1.0,
            'Overweight':  0.8,
            'Obese':       0.7,
        }
    },
    'Fatiga': {
        'diagnoses': [
            ('R53',   'Fatiga'),
            ('E11',   'Diabetes tipo 2'),
            ('F33.9', 'Depresión'),
        ],
        'age_probability': {
            '<18':   0.20,
            '18-60': 0.30,
            '>60':   0.35,
        },
        'bmi_factor': {
            'Underweight': 1.0,
            'Normal':      1.0,
            'Overweight':  1.1,
            'Obese':       1.3,
        }
    }
}

chronic_diseases = {
    'Hipertensión': {
        'age_range':        (40, 100),
        'base_probability': 0.25,
        'bmi_multipliers': {
            'Underweight': 0.8,
            'Normal':      1.0,
            'Overweight':  1.5,
            'Obese':       2.0,
        }
    },
    'Diabetes tipo 2': {
        'age_range':        (30, 100),
        'base_probability': 0.15,
        'bmi_multipliers': {
            'Underweight': 0.7,
            'Normal':      1.0,
            'Overweight':  2.0,
            'Obese':       3.5,
        }
    },
    'Enfermedad coronaria': {
        'age_range':        (50, 100),
        'base_probability': 0.18,
        'bmi_multipliers': {
            'Underweight': 0.9,
            'Normal':      1.0,
            'Overweight':  1.8,
            'Obese':       2.5,
        }
    },
    'Apnea del sueño': {
        'age_range':        (30, 100),
        'base_probability': 0.05,
        'bmi_multipliers': {
            'Underweight': 0.5,
            'Normal':      0.7,
            'Overweight':  2.0,
            'Obese':       4.0,
        }
    },
    'EPOC': {
        'age_range':        (40, 100),
        'base_probability': 0.10,
        'bmi_multipliers': {
            'Underweight': 0.7,
            'Normal':      1.0,
            'Overweight':  1.2,
            'Obese':       1.4,
        }
    },
    'Artritis reumatoide': {
        'age_range':        (20, 80),
        'base_probability': 0.02,
        'bmi_multipliers': {
            'Underweight': 0.9,
            'Normal':      1.0,
            'Overweight':  1.1,
            'Obese':       1.3,
        }
    },
    'Hipotiroidismo': {
        'age_range':        (20, 80),
        'base_probability': 0.08,
        'bmi_multipliers': {
            'Underweight': 1.2,
            'Normal':      1.0,
            'Overweight':  0.9,
            'Obese':       0.8,
        }
    }
}
