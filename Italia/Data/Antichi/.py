import pandas as pd
ANNO = 2023

df = pd.read_csv('Data.csv')

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

# Trasformazione delle date (2205 -> 22-05)
df[' Data'] = df[' Data'].astype(str)
df[' Data'] = df[' Data'].str.zfill(4).str.replace(r'^(\d{2})(\d{2})$', r'\1-\2', regex=True)

# Leggend le date per aggiungere l'anno che è stato impostato
df[' Data'] = pd.to_datetime(df[' Data'].astype(str), format='%d-%m').dt.strftime('%d-%m-2023')

# Creando la colonna dei "Giorni della settimana" e i "Mesi" in base alla colonna "Data"
df[' Giorno della settimana'] = pd.to_datetime(df[' Data']).dt.day_name()
df[' Mese'] = pd.to_datetime(df[' Data']).dt.month_name()
df[' Anno'] = ANNO

# Applicando il modello per la traduzione
df[" Giorno della settimana"] = df[" Giorno della settimana"].replace(mapping_day)
df[" Mese"] = df[" Mese"].replace(mapping_month)

# Creazione dell'indice
totale, _ = df.shape
totale = totale + 1
index = list(map(lambda x: x, range(1, totale)))

df = df.assign(Index=index) # Agggiungendo l'indice

df = df.rename(columns={' Slide':'Lezione', ' Data':'Data',
                        ' Professoressa':'Professoressa', ' Livello':'Livello',
                        ' Giorno della settimana':'Giorno della settimana',
                        ' Mese':'Mese', ' Anno':'Anno'})

df = df.reindex(columns=['Index', 'Data', 'Ora', 'Professoressa',
                         'Livello', 'Lezione', 'Giorno della settimana',
                         'Mese', 'Anno']) # Riordinando le colonne

def conclusione(operazione:int, csv:None):
    op = operazione
    if op == 1:
        dataframe = pd.read_csv(csv)
        dataframe = dataframe.drop('Unnamed: 0', axis=1)

        df_finale = pd.concat([dataframe, df])
        df_finale.to_csv('Lezioni1.csv')
        return df_finale
    elif op == 2:
        df.to_csv('Lezioni.csv')

#conclusione(1, 'Lezioni.csv')
conclusione(2, None)

# Correzione degli spazi

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

# Creato da Enzo Schitini