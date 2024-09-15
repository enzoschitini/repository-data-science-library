import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from collections import Counter

df = pd.read_csv('Lezioni.csv').drop(columns='Unnamed: 0')
#pd.DataFrame(df[(df['Index'] >= 269) & (df['Index'] <= 294)]['Professoressa'].value_counts().head(25))
df['MESE_ANNO'] = df['Mese'].astype(str) + '_' + df['Anno'].astype(str)

df_ascending_false = df.sort_values(by='Data', ascending=False)

# Definisci l'ordine dei mesi e anni
MESE_ANNO_ORDINE = ['Maggio_2023', 'Giugno_2023', 'Luglio_2023', 'Agosto_2023', 'Settembre_2023', 'Ottobre_2023',
                'Novembre_2023', 'Dicembre_2023', 'Gennaio_2024', 'Febbraio_2024', 'Marzo_2024',
                'Aprile_2024', 'Maggio_2024', 'Giugno_2024', 'Luglio_2024', 'Agosto_2024', 'Settembre_2024']

def ordina_in_base_al_periodo(dizionario_da_ordinare):
    dizionario_ordinato = {chiave: dizionario_da_ordinare[chiave] for chiave in MESE_ANNO_ORDINE if chiave in dizionario_da_ordinare}
    return dizionario_ordinato

def grafico_di_linea(list_dic, names, title, xaxis_title, yaxis_title, legend_title):
    # Crea il grafico a linee
    fig = go.Figure()

    # Itera attraverso i dizionari e i nomi
    for dic, name in zip(list_dic, names):
        fig.add_trace(go.Scatter(x=list(dic.keys()), y=list(dic.values()), 
                                 mode='lines+markers', name=name))

    # Aggiungi titolo e etichette agli assi
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
        template='plotly_white',
        xaxis=dict(
            tickmode='linear'  # Forza la visualizzazione di tutti i mesi sull'asse X
        )
    )

    # Mostra il grafico
    st.plotly_chart(fig)

def distribuzione_delle_categorie(colonna:str):
    # Imposta l'ordine personalizzato per la colonna 'MESE_ANNO'
    df['MESE_ANNO'] = pd.Categorical(df['MESE_ANNO'], categories=MESE_ANNO_ORDINE, ordered=True)

    # Raggruppa i dati per livello e MESE_ANNO e conta il numero di lezioni
    data_grouped = df.groupby(['MESE_ANNO', colonna]).size().reset_index(name='Numero di Lezioni')

    # Crea il grafico a linee
    fig = px.line(data_grouped, x='MESE_ANNO', y='Numero di Lezioni', color=colonna, 
                title=f'Distribuzione delle Lezioni per {colonna} e Mese',
                labels={'MESE_ANNO': 'Mese e Anno', 'Numero di Lezioni': 'Numero di Lezioni'})

    # Aggiungi titolo e etichette agli assi
    fig.update_layout(
        template='plotly_white'
    )

    # Mostra il grafico
    st.plotly_chart(fig)

def differenza_giorni(dataframe):
    # Conversione della colonna 'Data' in datetime
    dataframe['Data'] = pd.to_datetime(dataframe['Data'])
    
    # Calcolo delle differenze in giorni tra le date consecutive
    dataframe = dataframe.sort_values('Data')
    dataframe['Differenza'] = dataframe['Data'].diff().dt.days
    
    # Calcolo della media e della differenza massima
    differenze = dataframe['Differenza'].dropna()
    media_differenza = round(differenze.mean(), 1)
    max_differenza = differenze.max()
    
    # Restituzione dei risultati
    testo = f'La media della differenza dei giorni tra le lezioni: {media_differenza} giorni. (Massimo: {max_differenza})'
    maggiori_differenze = differenze.tolist()
    maggiori_differenze.sort(reverse=True)
    
    return media_differenza, testo, maggiori_differenze

def intervalloCV(dataframe, mese_anno):
    # Filtraggio per MESE_ANNO e conteggio delle differenze
    df_mese_anno = dataframe[dataframe['MESE_ANNO'] == mese_anno]
    differenze = differenza_giorni(df_mese_anno)[2]
    conteggio = Counter(differenze)
    
    chiave = sum(conteggio.keys())
    valore = sum(conteggio.values())
    
    return f'{mese_anno} -> {chiave} -- {valore}', valore - chiave, chiave, valore

def show_intervalloCV():
    # Filtraggio dei mesi e anni specifici
    mesi_anno = df['MESE_ANNO'].unique().tolist()
    intervalloCV_differenze = []
    intervalloCV_chiavi = []
    intervalloCV_valori = []

    for mese_anno in mesi_anno:
        _, differenza, chiave, valore = intervalloCV(df, mese_anno)
        intervalloCV_differenze.append(differenza)
        intervalloCV_chiavi.append(chiave)
        intervalloCV_valori.append(valore)

    # Creazione del grafico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mesi_anno, y=intervalloCV_differenze, mode='lines', name='Differenza'))
    fig.add_trace(go.Scatter(x=mesi_anno, y=intervalloCV_chiavi, mode='lines', name='Giorni'))
    fig.add_trace(go.Scatter(x=mesi_anno, y=intervalloCV_valori, mode='lines', name='Ripetizione'))

    fig.update_layout(
        title='IntervalloCV',
        xaxis=dict(title='Mese e Anno'),
        yaxis=dict(title='Punteggi'),
        template='plotly_white'
    )

    st.plotly_chart(fig)