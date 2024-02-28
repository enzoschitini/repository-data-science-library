import pandas as pd
from datetime import datetime
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from memoria import guida as gd

df = pd.read_csv('Lezioni.csv')
df = df.drop(columns='Unnamed: 0', axis=1)
df.head(5)

df1 = df[(df['Mese'] == 'Giugno') | (df['Mese'] == 'Luglio') | (df['Mese'] == 'Agosto') | (df['Mese'] == 'Settembre') | (df['Mese'] == 'Ottobre')]
df2 = df[(df['Mese'] == 'Novembre') | (df['Mese'] == 'Dicembre') | (df['Mese'] == 'Gennaio') | (df['Mese'] == 'Febbraio')]

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

quantita, _ = df1.shape # Di lezioni
densita = round((quantita / ((df1.Mese.nunique()) * 30)), 2) # Densità
percentuale = round((densita * 100), 1) # Percentuale

print(f'Ci sono state {quantita} ore di lezioni durante più o meno {(df1.Mese.nunique()) * 30} giorni.')
print(f'La densità di lezioni al giorno {round(densita, 1)}')
print(f'La percentuale di lezioni che copre il periodo è {percentuale}%')
print(differenza_giorni(df1)[1])

from collections import Counter
conteggio = Counter(differenza_giorni(df1)[2])

for numero, ripetizioni in conteggio.items():
    print(f'{numero} -> {ripetizioni}')

quantita, _ = df2.shape # Di lezioni
densita = round((quantita / ((df2.Mese.nunique()) * 30)), 2) # Densità
percentuale = round((densita * 100), 1) # Percentuale

print(f'Ci sono state {quantita} ore di lezioni durante più o meno {(df2.Mese.nunique()) * 30} giorni.')
print(f'La densità di lezioni al giorno {round(densita, 1)}')
print(f'La percentuale di lezioni che copre il periodo è {percentuale}%')
print(differenza_giorni(df2)[1])

conteggio = Counter(differenza_giorni(df2)[2])

for numero, ripetizioni in conteggio.items():
    print(f'{numero} -> {ripetizioni}')

df1.Ora.value_counts()
df2.Ora.value_counts()

sns.boxplot(x=df1.Ora.tolist())
plt.xlabel('Le ore')
plt.show()
sns.boxplot(x=df2.Ora.tolist())
plt.xlabel('Le ore')
plt.show()

months_order = ['Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre',
       'Novembre', 'Dicembre', 'Gennaio', 'Febbraio']

tutti_i_mesi = df1.Mese.unique().tolist()

def plot_grafico(dizionari, nome):
    x = list(dizionari.keys())
    y1 = list(dizionari.values())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers', name='f', line=dict(color='lightseagreen')))

    fig.update_layout(title=nome,
                      xaxis_title='Mesi',
                      yaxis_title='Valori')

    fig.show()

orari = (df1.groupby('Mese')['Ora'].mean()).round().to_dict()
percentuali = ((df1.groupby('Mese')['Index'].count() / 30) * 100).round().to_dict()

orari = {k: v for k, v in sorted(orari.items(), key=lambda item: months_order.index(item[0]))}
percentuali = {k: v for k, v in sorted(percentuali.items(), key=lambda item: months_order.index(item[0]))}

def differenza(data): # Lista con le date
    oggetti_data = [datetime.strptime(data, "%Y-%m-%d") for data in data]
    differenze = []

    for i in range(len(oggetti_data)-1):
        delta = oggetti_data[i+1] - oggetti_data[i]
        differenze.append(delta.days)
    return differenze

dizionario_differenza_media = {}
dizionario_differenza_max = {}

for x in tutti_i_mesi:
    dfx = df1[df1['Mese'] == x]
    valori = differenza(dfx.Data.to_list())
    
    dizionario_differenza_media[x] = round((sum(valori) / len(valori)), 2)
    dizionario_differenza_max[x] = max(valori)

insegnati_dizionario = df1.Professoressa.value_counts().to_dict()
#insegnati_piu_di_dieci = {k: v for k, v in insegnati_dizionario.items() if v > 9}
from itertools import islice
insegnati_dizionario = dict(islice(insegnati_dizionario.items(), 5))
insegnanti_del_periodo = list(insegnati_dizionario.keys())

tutti_i_mesi = df1.Mese.unique().tolist()
livello_totale = []

for x in tutti_i_mesi:
    livelli = ['B1', 'B2', 'C1']
    percentuale_per_livello = []
    dfz = df1[df1['Mese'] == x]
    quantita, _ = dfz.shape

    for i in livelli:
        dfx, _ = dfz[dfz['Livello'] == i].shape
        percentuale = int(round(((dfx / quantita) * 100), 0))
        percentuale_per_livello.append(percentuale)

    lista = [x, percentuale_per_livello[0], percentuale_per_livello[1], percentuale_per_livello[2]]
    livello_totale.append(lista)

punteggi_dei_livelli = []

for x in livello_totale:
    posizione = [0, x[1], x[2], x[3]]
    posizione = posizione.index(max(posizione))
    punteggi_dei_livelli.append(posizione)
    print(f'{x[0]} --> B1: {x[1]}% -- B2: {x[2]}% -- C1: {x[3]}%')

def calcola_differenza(professoressa):
    insegnante = df[df['Professoressa'] == professoressa]
    insegnante = (insegnante.groupby('Mese')['Index'].count()).round()
    insegnante = insegnante.to_dict()

    #months_order = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

    mesi = list(insegnante.keys())
    differenza = list(set(months_order) - set(mesi))

    if len(differenza) > 0:
        for x in differenza:
            insegnante[x] = 0

    insegnante = {k: v for k, v in sorted(insegnante.items(), key=lambda item: months_order.index(item[0]))}
    
    return insegnante

# Dati per le due linee
x = months_order
y1 = list(calcola_differenza(insegnanti_del_periodo[0]).values())
y2 = list(calcola_differenza(insegnanti_del_periodo[1]).values()) 
y3 = list(calcola_differenza(insegnanti_del_periodo[2]).values()) 
y4 = list(calcola_differenza(insegnanti_del_periodo[3]).values()) 
y5 = list(calcola_differenza(insegnanti_del_periodo[4]).values())

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
fig.show()

punteggio_del_periodo = sum(punteggi_dei_livelli) / len(punteggi_dei_livelli)
sum(list(dizionario_differenza_media.values()))

import plotly.graph_objects as go

def valore(dizionario:dict):
    return round((sum(list(dizionario.values())) / len(list(dizionario.values()))), 1)

df = pd.DataFrame(dict(
categorie = ["Percentuale", "Orari", "Distanza", "Distanza massima", "Livelli"],
periodo = [float(list(str(valore(percentuali)))[0]), valore(orari), 
           valore(dizionario_differenza_media), max(dizionario_differenza_max.values()), 
           punteggio_del_periodo]))
df

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

fig.show()
#import plotly.io as pio
#pio.write_image(fig, 'grafico.png')