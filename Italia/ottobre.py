import pandas as pd
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from memoria import guida as gd

# I dati
df = pd.read_csv('Lezioni.csv')
df = df.drop(columns='Unnamed: 0', axis=1)

# Dividiamo i nostri dat
df1 = df[(df['Mese'] == 'Giugno') | (df['Mese'] == 'Luglio') | (df['Mese'] == 'Agosto') | (df['Mese'] == 'Settembre') | (df['Mese'] == 'Ottobre')]
df2 = df[(df['Mese'] == 'Novembre') | (df['Mese'] == 'Dicembre') | (df['Mese'] == 'Gennaio') | (df['Mese'] == 'Febbraio')]

# Impostazione
DATA = df1
mostrare_boxplot = False

months_order = ['Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre',
       'Novembre', 'Dicembre', 'Gennaio', 'Febbraio']

# Le prime metriche

def differenza_giorni(dataframe):
    le_date = dataframe['Data']
    data = []
    
    for x in le_date:
        x = str(x)
        data.append(x[0:10])
    
    # Conversione delle stringhe in oggetti datetime
    oggetti_data = [datetime.strptime(data, "%Y-%m-%d") for data in data]
    differenze = []

    # Calcolo delle differenze in giorni
    for i in range(len(oggetti_data)-1):
        delta = oggetti_data[i+1] - oggetti_data[i]
        differenze.append(delta.days)
    
    differenza = round((sum(differenze)/len(differenze)), 1)
    testo = f'La media della differenza dei giorni tra le lezioni: {differenza} giorni. (Massimo: {max(differenze)})'
    
    maggiori_differenze = differenze
    maggiori_differenze = [int(valore) for valore in maggiori_differenze]
    #maggiori_differenze = list(set(maggiori_differenze))
    maggiori_differenze.sort(reverse=True)

    return differenza, testo, maggiori_differenze[:-1]

# DF1 Calcoli

quantita, _ = df1.shape # Di lezioni
densita = round((quantita / ((df1.Mese.nunique()) * 30)), 2) # Densità
percentuale = round((densita * 100), 1) # Percentuale

print(f'\nCi sono state {quantita} ore di lezioni durante più o meno {(df1.Mese.nunique()) * 30} giorni.')
print(f'\nLa densità di lezioni al giorno {round(densita, 1)}')
print(f'La percentuale di lezioni che copre il periodo è {percentuale}%')
print(differenza_giorni(df1)[1])
print('-------------------------------------------------------------------------------------')

from collections import Counter
conteggio = Counter(differenza_giorni(df1)[2])

for numero, ripetizioni in conteggio.items():
    print(f'{numero} -> {ripetizioni}')

# Gli orari 

print(f'\n{df1.Ora.value_counts()}')

# Condizionali
######################################################################
if mostrare_boxplot == True:
    sns.boxplot(x=df1.Ora.tolist())
    plt.xlabel('Le ore')
    plt.show()
    sns.boxplot(x=df2.Ora.tolist())
    plt.xlabel('Le ore')
    plt.show()

# Grafico dei mesi
######################################################################
tutti_i_mesi = DATA.Mese.unique().tolist()

def plot_grafico(dizionari, nome):
    x = list(dizionari.keys())
    y1 = list(dizionari.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name='f', line=dict(color='lightseagreen')))

    fig.update_layout(title=nome,
                      xaxis_title='Mesi',
                      yaxis_title='Valori')

    fig.show()

# Media degli orari, Percentuale, Distanza tra le lezioni

orari = (DATA.groupby('Mese')['Ora'].mean()).round().to_dict()
percentuali = ((DATA.groupby('Mese')['Index'].count() / 30) * 100).round().to_dict()

dizionario_differenza_media = {}
dizionario_differenza_max = {}

def differenza(data): # Lista con le date
    oggetti_data = [datetime.strptime(data, "%Y-%m-%d") for data in data]
    differenze = []

    for i in range(len(oggetti_data)-1):
        delta = oggetti_data[i+1] - oggetti_data[i]
        differenze.append(delta.days)
    return differenze

for x in tutti_i_mesi:
    dfx = DATA[DATA['Mese'] == x]
    valori = differenza(dfx.Data.to_list())
    
    dizionario_differenza_media[x] = round((sum(valori) / len(valori)), 2)
    dizionario_differenza_max[x] = max(valori)


orari = {k: v for k, v in sorted(orari.items(), key=lambda item: months_order.index(item[0]))}
percentuali = {k: v for k, v in sorted(percentuali.items(), key=lambda item: months_order.index(item[0]))}

plot_grafico(dizionario_differenza_media, 'NOME')

# Le professoresse del periodo
######################################################################
from itertools import islice

insegnati_dizionario = DATA.Professoressa.value_counts().to_dict() # Dizionario delle professoresse

insegnati_dizionario = dict(islice(insegnati_dizionario.items(), 5)) # Filtrare le 5 prime
insegnanti_del_periodo = list(insegnati_dizionario.keys())

# Percentuali dei livelli ad ogni mese
######################################################################

livello_totale = []

for x in tutti_i_mesi:
    livelli = ['B1', 'B2', 'C1']
    percentuale_per_livello = []
    dfz = DATA[DATA['Mese'] == x]
    quantita, _ = dfz.shape

    for i in livelli:
        dfx, _ = dfz[dfz['Livello'] == i].shape
        percentuale = int(round(((dfx / quantita) * 100), 0))
        percentuale_per_livello.append(percentuale)

    lista = [x, percentuale_per_livello[0], percentuale_per_livello[1], percentuale_per_livello[2]]
    livello_totale.append(lista)

punteggi_dei_livelli = []

print('\n')
for x in livello_totale:
    posizione = [0, x[1], x[2], x[3]]
    posizione = posizione.index(max(posizione))
    punteggi_dei_livelli.append(posizione)
    print(f'{x[0]} --> B1: {x[1]}% -- B2: {x[2]}% -- C1: {x[3]}%')

punteggio_del_periodo = sum(punteggi_dei_livelli) / len(punteggi_dei_livelli)
print(f'Livello del periodo {livelli[int(punteggio_del_periodo - 1)]}')

# Livello di ogni professoressa per mese
######################################################################

def percentuale_livello_insegnante(professoressa:str):
    data = DATA[['Professoressa', 'Livello', 'Mese']]

    # Calcolo delle frequenze dei livelli per ogni professoressa
    pivot_table = pd.pivot_table(data, index=['Professoressa', 'Mese'], columns='Livello', aggfunc=len, fill_value=0)

    # Calcolo delle percentuali
    percentuali_df = round((pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100), 1)

    # Resettiamo l'indice per ottenere un dataframe piatto
    percentuali_df = percentuali_df.reset_index()

    # Rinominiamo le colonne per soddisfare il formato richiesto
    percentuali_df.columns.name = None
    percentuali_df.columns = ['Professoressa', 'Mese', 'Percentuale B1', 'Percentuale B2', 'Percentuale C1']

    #percentuali_df = pd.merge(percentuali_df.reset_index(), lezioni_totali, on='Professoressa')
    #lezioni_totali = pd.merge(percentuali.reset_index(), lezioni_totali, on='Professoressa')

    if professoressa != '':
        percentuali_df = percentuali_df[percentuali_df['Professoressa'] == professoressa]
        return percentuali_df
    else:
        return percentuali_df
    
print(percentuale_livello_insegnante('Lorella'))

# Quantità di lezione delle professoresse al mese
######################################################################

def quantita_lezione_professoressa(professoressa):
    insegnante = df[df['Professoressa'] == professoressa]
    insegnante = (insegnante.groupby('Mese')['Index'].count()).round()
    insegnante = insegnante.to_dict()

    mesi = list(insegnante.keys())
    differenza = list(set(months_order) - set(mesi))

    if len(differenza) > 0:
        for x in differenza:
            insegnante[x] = 0

    insegnante = {k: v for k, v in sorted(insegnante.items(), key=lambda item: months_order.index(item[0]))}
    
    return insegnante

quantita_lezione_professoressa(insegnanti_del_periodo[0]) # Dizionario

# Grafico

# Dati per le due linee
x = months_order
y1 = list(quantita_lezione_professoressa(insegnanti_del_periodo[0]).values())
y2 = list(quantita_lezione_professoressa(insegnanti_del_periodo[1]).values()) 
y3 = list(quantita_lezione_professoressa(insegnanti_del_periodo[2]).values()) 
y4 = list(quantita_lezione_professoressa(insegnanti_del_periodo[3]).values()) 
y5 = list(quantita_lezione_professoressa(insegnanti_del_periodo[4]).values())

# Creare il grafico di linea con due linee
fig = go.Figure()

# Aggiungere la prima linea con colore blu
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name=insegnanti_del_periodo[0], line=dict(color='green')))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers', name=insegnanti_del_periodo[1], line=dict(color='red')))
fig.add_trace(go.Scatter(x=x, y=y3, mode='lines+markers', name=insegnanti_del_periodo[2], line=dict(color='lightseagreen')))
fig.add_trace(go.Scatter(x=x, y=y4, mode='lines+markers', name=insegnanti_del_periodo[3], line=dict(color='orange')))
fig.add_trace(go.Scatter(x=x, y=y5, mode='lines+markers', name=insegnanti_del_periodo[4], line=dict(color='blue')))

# Aggiungere etichette e titoli
fig.update_layout(title='Grafico dei livelli',
                  xaxis_title='Mesi',
                  yaxis_title='Valori')

# Mostrare il grafico
#fig.show()

# Le carateristiche
######################################################################

import plotly.graph_objects as go

def valore(dizionario:dict):
    return round((sum(list(dizionario.values())) / len(list(dizionario.values()))), 1)

df = pd.DataFrame(dict(
categorie = ["Percentuale", "Orari", "Distanza", "Distanza massima", "Livelli"],
periodo = [float(list(str(valore(percentuali)))[0]), valore(orari), 
           valore(dizionario_differenza_media), max(dizionario_differenza_max.values()), 
           punteggio_del_periodo]))

fig = go.Figure()

def aggiungi_traccia(fig, df, colonna):
    fig.add_trace(go.Scatterpolar(
        r = df[colonna],
        theta = df["categorie"],
        fill = "toself",
        name = "Janeiro",
        line = dict(color = "#63A644"),
        fillcolor = "#63A644",
        opacity = 0.2
    ))

for x in df.columns[1:].to_list():
    aggiungi_traccia(fig, df, x)

#fig.show()
#import plotly.io as pio
#pio.write_image(fig, 'grafico.png')

# Creato da Enzo Schitini 😉