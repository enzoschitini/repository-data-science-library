import pandas as pd

"""
from tabella import guida
guida(df)
"""

def guida(data_frame): # 14/02/2024
    righe, qnt_colonne = data_frame.shape
    quantita_righe = format(righe, ",").replace(',', '.')
    sequenza = list(range(qnt_colonne + 1))
    sequenza = sequenza[1:]

    colonne = data_frame.columns.to_list()
    types_list = [str(type(data_frame[col][0])).split("'")[1] for col in data_frame.columns]
    lista_categorie = [data_frame[col].nunique() for col in data_frame.columns]

    elementi_nulli = data_frame.isnull().sum()
    elementi_nulli = elementi_nulli.to_list()

    memory = (data_frame.memory_usage(deep=True) / (1024 ** 2)).round() # Mb
    memory_list = memory.to_list()
    memory_list = memory_list[1:]

    memory = data_frame.memory_usage(deep=True) # Totale Mb
    memory_totale = round(memory.sum() / (1024 ** 2), 2)

    percentuale_dati_nulli = round((data_frame.isnull().sum() / righe) * 100)
    percentuale_dati_nulli = percentuale_dati_nulli.to_list()

    data = pd.DataFrame({'Nome': colonne, 
                         'Tipo': types_list, 
                         'qunt_categorie': lista_categorie,
                         'Dati nulli' : elementi_nulli,
                         'Dati nulli %' : percentuale_dati_nulli,
                         'Memoria (Mb)': memory_list}, index=sequenza)
    
    # Intestazioni
    print('Teabella Esplorativa')
    print(f'In questi dati abbiamo {quantita_righe} righe e {qnt_colonne} colonne.')
    print(f'Consumassione di memoria: {memory_totale}Mb.')
    
    return data