# Preparazione dei dati per le metriche

# Qui dobbiamo prendere i dati grezzi raccolti dalle lezioni 
# che sono state fatte e renderli possibili da leggere.
# Inoltre abbiamo bisogno di una sistemazione per farlo più volte
# e adattarlo in base all'anno.

# Importiamo
import pandas as pd
import os

# Impostiamo le variabili
ANNO = 2024
OPERZIONE = 1
NOME = 'Lezioni.csv'
DATI = 'Data\Da_aggiungere.csv'
#DATI = 'Data\Data.csv'

df = pd.read_csv(DATI) #Da_aggiungere

# Creazione della colonna livelli 

def livello(valore):
    valore = list(valore)
    valore = f' {valore[1]}{valore[2]}'
    return valore

df[' Livello'] = df[' Slide'].apply(livello)

# Modello per la traduzione

# Giorni della sttimana
mapping_day = {"Monday": "Lunedì", 
           "Tuesday": "Martedì", 
           "Wednesday": "Mercoledì",
           "Thursday": "Giovedì",
           "Friday": "Venerdì",
           "Saturday": "Sabato",
           "Sunday": "Domenica"}

# Mesi dell'anno
mapping_month = {"January": "Gennaio",
                 "February": "Febbraio",
                 "March": "Marzo",
                 "April": "Abrile",
                 "May": "Maggio", 
                 "June": "Giugno", 
                 "July": "Luglio",
                 "August": "Agosto",
                 "September": "Settembre",
                 "October": "Ottobre",
                 "November": "Novembre",
                 "December": "Dicembre"}

# Trasformazione delle date (2205 -> 22-05-2023)
df[' Data'] = df[' Data'].astype(str)
df[' Data'] = df[' Data'].str.zfill(4).str.replace(r'^(\d{2})(\d{2})$', r'\1-\2', regex=True)

def agg_anno(valore):
    valore = str(valore)
    valore = f'{valore}-{ANNO}'
    return valore

df[' Data'] = df[' Data'].apply(agg_anno)

# Leggend le date per aggiungere l'anno che è stato impostato
df[' Data'] = pd.to_datetime(df[' Data'].astype(str), format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
df[' Data'] = pd.to_datetime(df[' Data'].astype(str), format='%d-%m-%Y')

# Creando la colonna dei "Giorni della settimana" e i "Mesi" in base alla colonna "Data"
df[' Giorno della settimana'] = pd.to_datetime(df[' Data']).dt.day_name()
df[' Mese'] = pd.to_datetime(df[' Data']).dt.month_name()
df[' Anno'] = ANNO

df[" Giorno della settimana"] = df[" Giorno della settimana"].replace(mapping_day)
df[" Mese"] = df[" Mese"].replace(mapping_month)

# Cambiando il nome delle colonne

df = df.rename(columns={' Slide':'Lezione', ' Data':'Data',
                        ' Professoressa':'Professoressa', ' Livello':'Livello',
                        ' Giorno della settimana':'Giorno della settimana',
                        ' Mese':'Mese', ' Anno':'Anno'})

df = df.reindex(columns=['Data', 'Ora', 'Professoressa',
                         'Livello', 'Lezione', 'Giorno della settimana',
                         'Mese', 'Anno']) # Riordinando le colonne

# Operazione da eseguire

def conclusione(operazione:int, csv:None):
    op = operazione
    if op == 1:
        dataframe = pd.read_csv(csv)
        dataframe = dataframe.drop('Unnamed: 0', axis=1)
        df['Data'] = df['Data'].astype(str)

        df_finale = pd.concat([dataframe, df])
        os.remove('Lezioni.csv')
        df_finale.to_csv('Lezioni.csv')
        return df_finale
    elif op == 2:
        df.to_csv('Lezioni.csv')

conclusione(OPERZIONE, NOME) # In base ai valori impostati prima

# Correzione degli spazi

df = pd.read_csv('Lezioni.csv') # Qui i dati no già stati creati o aggiunti

def strip(valore):
    tipo = str(type(valore))
    valore = str(valore)
    valore = valore.strip()

    if tipo == "<class 'int'>":
        valore = int(valore)
    elif tipo == "<class 'str'>":
        valore = str(valore)
    else:
        valore = float(valore)

    return valore

lista_colonne = df.columns.to_list()

for x in lista_colonne:
    df[x] = df[x].apply(strip)
    df.to_csv('Lezioni.csv')

# Creazione dell'indice
totale, _ = df.shape
totale = totale + 1
index = list(map(lambda x: x, range(1, totale)))

df = df.assign(Index=index)

df = df.reindex(columns=['Index', 'Data', 'Ora', 'Professoressa',
                         'Livello', 'Lezione', 'Giorno della settimana',
                         'Mese', 'Anno']) # Riordinando le colonne

df.to_csv('Lezioni.csv')


# Creato da Enzo Schitini 😉