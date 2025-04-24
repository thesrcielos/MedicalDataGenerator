from algorithms import constants
from algorithms.data_generator import BogotaMedicalGenerator
import pandas as pd
from data_visualization import generate_graphics

def create_file_data():
    generator = BogotaMedicalGenerator()
    data = [generator.generate_patient() for _ in range(constants.ROW_NUMBER)]
    df = pd.DataFrame(data)

    df['Fecha Consulta'] = pd.to_datetime(df['Fecha Consulta'], dayfirst=True)
    df = df.sort_values('Fecha Consulta')

    df.insert(0, '#Fila', range(1, len(df) + 1))
    df.to_csv('bogota_medical_records.csv', index=False)

    print(df.head(3).to_markdown(index=False, numalign="left", stralign="left"))
if __name__ == "__main__":
    generate_graphics()
