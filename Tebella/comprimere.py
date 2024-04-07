import os
from pathlib import Path
import pandas as pd

class Parquet(object):
    def __init__(self, percorso_cartella:str) -> None:
        self.percorso_cartella = percorso_cartella

    def trova_csv(self):
        elenco_csv = []
        peso = []
        # Scandisce tutti i file nella cartella
        for file in os.listdir(self.percorso_cartella):
            if file.endswith(".csv"):  # Verifica se il file è un file CSV
                file_path = os.path.join(self.percorso_cartella, file)  # Ottiene il percorso completo del file
                file_size = os.path.getsize(file_path)  # Ottiene il peso del file in byte
                file_size = round((file_size / (1024 * 1024)), 2)
                peso.append(file_size)
                elenco_csv.append(file)  # Aggiunge il nome del file CSV alla lista
        return elenco_csv, peso

    def trasformare(self, lista_datasets:list):
        if type(lista_datasets) == list:
         
         for data in lista_datasets:
            data = str(data)
            #terminazione = data[data.find('.'):(data.find(data[-1])+2)]
            data = data.replace('.csv', '')
            df = pd.read_csv(f'{self.percorso_cartella}/{data}.csv')
            #df = pd.read_csv(data)
            df.to_parquet(f'{self.percorso_cartella}/{data}.parquet')
    
    def elimina_csv(self):
        # Scandisce tutti i file nella cartella
        for file in os.listdir(self.percorso_cartella):
            if file.endswith(".csv"):  # Verifica se il file è un file CSV
                percorso_file = os.path.join(self.percorso_cartella, file)  # Ottiene il percorso completo del file
                os.remove(percorso_file)  # Elimina il file
    
    def risparmio(self):
        nuovo_peso = []
        for file in os.listdir(self.percorso_cartella):
            if file.endswith(".parquet"):
                file_path = os.path.join(self.percorso_cartella, file)
                file_size = os.path.getsize(file_path)
                file_size = round((file_size / (1024 * 1024)), 2)
                nuovo_peso.append(file_size)
        return round((sum(nuovo_peso)), 2)

# Sostituisci 'percorso_della_cartella' con il percorso della tua cartella contenente i file CSV
#percorso_della_cartella = "Set di dati Libri"

def nome_cartella_genitore():
    # Ottieni il percorso del file script corrente
    percorso_script = Path(__file__).resolve()

    # Ottieni il percorso della cartella genitore
    percorso_cartella_genitore = percorso_script.parent
    
    # Estrai il nome della cartella genitore
    nome_cartella_genitore = percorso_cartella_genitore.name
    return nome_cartella_genitore

# Ottieni e stampa il nome della cartella genitore
nome_cartella = nome_cartella_genitore()
print("\nIl nome della cartella genitore è:", nome_cartella, '\n')

cartella = Parquet(nome_cartella)
elenco_della_cartella = cartella.trova_csv()[0] # Lista coi CSV 
peso_csv = cartella.trova_csv()[1] # Lista coi pesi degli archivi

if len(elenco_della_cartella) == 0:
    print('Non ci sono csv in questa cartella.')
else:
    print("Archivi CSV trovati:")
    ordine = 0
    for csv in elenco_della_cartella:
        print(f"{csv} -- {peso_csv[ordine]}Mb")
        ordine += 1
    cartella.trasformare(elenco_della_cartella)
    cartella.elimina_csv()
    print("\nTutti gli archivi CSV sono stati trasformati in parquet.")
    print(f"{round((sum(peso_csv)), 2)}Mb --> {cartella.risparmio()}Mb (Risparmio di {round((sum(peso_csv) - cartella.risparmio()), 2)}Mb)\n")

# By Enzo Schitini 07 Abril 2024