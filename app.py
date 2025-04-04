from algoritmhs.data_generator import BogotaMedicalGenerator
from algoritmhs import constants
import pandas as pd

if __name__ == "__main__":
    generator = BogotaMedicalGenerator()
    data = [generator.generate_patient() for _ in range(constants.ROW_NUMBER)]

    # Create DataFrame
    df = pd.DataFrame(data)

    # Data validations
    df['Fecha Consulta'] = pd.to_datetime(df['Fecha Consulta'], dayfirst=True)
    df = df.sort_values('Fecha Consulta')

    df.insert(0, '#Fila', range(1, len(df) + 1))
    # Save to CSV
    df.to_csv('bogota_medical_records.csv', index=False)

    # Show sample
    print(df.head(3).to_markdown(index=False, numalign="left", stralign="left"))
