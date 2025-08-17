import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from collections import Counter

df = pd.read_csv('C:/Users/schit/Documents/Lezioni/Lezioni.csv')#.drop(columns='Unnamed: 0')
#pd.DataFrame(df[(df['Index'] >= 269) & (df['Index'] <= 294)]['Professoressa'].value_counts().head(25))
df['MESE_ANNO'] = df['Mese'].astype(str) + '_' + df['Anno'].astype(str)

df_ascending_false = df.sort_values(by='Data', ascending=False)

# Definisci l'ordine dei mesi e anni
MESE_ANNO_ORDINE = [
                # 2023
                'Maggio_2023', 'Giugno_2023', 'Luglio_2023', 'Agosto_2023', 'Settembre_2023', 'Ottobre_2023',
                'Novembre_2023', 'Dicembre_2023', 
                # 2024
                'Gennaio_2024', 'Febbraio_2024', 'Marzo_2024', 'Aprile_2024', 'Maggio_2024', 'Giugno_2024', 'Luglio_2024', 'Agosto_2024', 
                'Settembre_2024', 'Ottobre_2024', 'Novembre_2024', 'Dicembre_2024',
                # 2025
                'Gennaio_2025', 'Febbraio_2025', 'Marzo_2025', 'Aprile_2025', 'Maggio_2025', 'Giugno_2025', 'Luglio_2025', 'Agosto_2025',
                'Settembre_2025', 'Ottobre_2025', 'Novembre_2025', 'Dicembre_2025']

def dic_foto(professoressa):
    persona = {
        "Miriam": "app/immagini_persone/miriam.png",
        "Rita": "app/immagini_persone/rita.png",
        "Chiara": "app/immagini_persone/chiara.png",
        "Martina": "app/immagini_persone/martina.png",
        "Graziana": "app/immagini_persone/graziana.png",
        "Marina": "app/immagini_persone/marina.png",
        "Francesca": "app/immagini_persone/francesca.png",
        "Asia": "app/immagini_persone/asia.png",
        "Anna": "app/immagini_persone/anna.png",
        "Marta": "app/immagini_persone/marta.png",
        "Giulia 2": "app/immagini_persone/giulia_2.png",
        "Giusy": "app/immagini_persone/giusy.png",
        "Francesca 2": "app/immagini_persone/francesca_2.png",
        "Sofia": "app/immagini_persone/sofia.png",
        "Giada": "app/immagini_persone/giada.png",
        "Maddalena": "app/immagini_persone/maddalena.png",
        "Cecilia": "app/immagini_persone/cecilia.png",
        "Lorella": "app/immagini_persone/lorella.png",
        "Clara": "app/immagini_persone/clara.png",
        "Antonella": "app/immagini_persone/antonella.png",
        "Simona": "app/immagini_persone/simona.png",
        "Raffaella": "app/immagini_persone/raffaella.png",
        "Jessica": "app/immagini_persone/jessica.png",
        "Jlenia": "app/immagini_persone/jlenia.png",
        "Silvia": "app/immagini_persone/silvia.png",
        "Giulia": "app/immagini_persone/giulia.png",
        "Valentina": "app/immagini_persone/valentina.png",
        "Laura": "app/immagini_persone/laura.png",
        "Maria Francesca": "app/immagini_persone/maria_francesca.png",
        "Milica": "app/immagini_persone/milica.png",
        "Anna 3": "app/immagini_persone/anna_3.png",
        "Beatrice 3": "app/immagini_persone/beatrice_3.png",
        "Elena 2": "app/immagini_persone/elena_2.png",
        "Giovanna": "app/immagini_persone/giovanna.png",
        "Katia": "app/immagini_persone/katia.png",
        "Cristina": "app/immagini_persone/cristina.png",
        "Francesca 3": "app/immagini_persone/francesca_3.png",
        "Silvia 2": "app/immagini_persone/silvia_2.png",
        "Federico": "app/immagini_persone/federico.png"
    }
    
    return persona.get(professoressa, "Professoressa non trovata")

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

def distribuzione_delle_categorie(colonna:str, df, tipo):
    # Imposta l'ordine personalizzato per la colonna 'MESE_ANNO'
    df['MESE_ANNO'] = pd.Categorical(df['MESE_ANNO'], categories=MESE_ANNO_ORDINE, ordered=True)

    # Raggruppa i dati per livello e MESE_ANNO e conta il numero di lezioni
    data_grouped = df.groupby(['MESE_ANNO', colonna]).size().reset_index(name='Numero di Lezioni')

    # Calcola la percentuale di lezioni per ogni categoria
    totale_lezioni = data_grouped['Numero di Lezioni'].sum()
    data_grouped['Percentuale'] = (data_grouped['Numero di Lezioni'] / totale_lezioni * 100).round(2)

    # Crea il sottotitolo con le percentuali di ogni categoria
    percentuali_categorie = round(data_grouped.groupby(colonna)['Percentuale'].sum().reset_index(), 2)
    sottotitolo = ' | '.join([f"{row[colonna]}: {row['Percentuale']}%" for _, row in percentuali_categorie.iterrows()])

    if tipo == 'Line':
        # Crea il grafico a linee
        fig = px.line(data_grouped, x='MESE_ANNO', y='Numero di Lezioni', color=colonna, 
                    title=f'Distribuzione delle Lezioni per {colonna} e Mese',
                    labels={'MESE_ANNO': 'Mese e Anno', 'Numero di Lezioni': 'Numero di Lezioni'})
    elif tipo == 'BarO':
        # Crea il grafico a barre orizzontali
        fig = px.bar(data_grouped, x='MESE_ANNO', y='Numero di Lezioni', color=colonna, 
                    title=f'Distribuzione delle Lezioni per {colonna} e Mese',
                    labels={'MESE_ANNO': 'Mese e Anno', 'Numero di Lezioni': 'Numero di Lezioni'})
    elif tipo == 'BarV':
        # Crea il grafico a barre verticali
        fig = px.bar(data_grouped, x='Numero di Lezioni', y='MESE_ANNO', color=colonna, 
                    title=f'Distribuzione delle Lezioni per {colonna} e Mese',
                    labels={'MESE_ANNO': 'Mese e Anno', 'Numero di Lezioni': 'Numero di Lezioni'})

    # Aggiungi il sottotitolo con le percentuali
    fig.update_layout(
        template='plotly_white',
        title={
            'text': f"Distribuzione delle Lezioni per {colonna} e Mese<br><sup>{sottotitolo}</sup>",
            'x': 0.5,  # Centra il titolo
            'xanchor': 'center'
        }
    )

    # Mostra il grafico
    st.plotly_chart(fig)

def distribuzione_delle_categorie_semplice(df, colonna:str):
    giorni_valori = df[colonna].value_counts().to_dict()
    tutti = list(giorni_valori.keys())
    quantita = list(giorni_valori.values())

    fig = px.bar(x=quantita, y=tutti, 
                title=f"Distribuzione della quantità di {colonna}",
                labels={'x': 'Quantità', 'y': colonna})

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
    testo = f'| La media della differenza dei giorni tra le lezioni: {media_differenza} giorni. (Massimo: {max_differenza})'
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

def scegliere_opzione(domanda, opzioni):
    risposta = st.selectbox(domanda, opzioni)
    return risposta

def scegliere_opzione_laterale(domanda, opzioni):
    risposta = st.sidebar.selectbox(domanda, opzioni)
    return risposta

# Analisi delle professoresse