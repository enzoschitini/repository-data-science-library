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
MESE_ANNO_ORDINE = ['Maggio_2023', 'Giugno_2023', 'Luglio_2023', 'Agosto_2023', 'Settembre_2023', 'Ottobre_2023',
                'Novembre_2023', 'Dicembre_2023', 'Gennaio_2024', 'Febbraio_2024', 'Marzo_2024',
                'Aprile_2024', 'Maggio_2024', 'Giugno_2024', 'Luglio_2024', 'Agosto_2024', 'Settembre_2024', 'Ottobre_2024', 'Novembre_2024',
                'Dicembre_2024']

def dic_foto(professoressa):
    persona = {
        "Miriam": "https://d2y3m460t2850n.cloudfront.net/v1/7ae6d76e6a2aec931ec1c49f02179d3d.png",
        "Rita": "https://d2y3m460t2850n.cloudfront.net/v1/9c62efc728cc7e22f265e918a6488fe9.png",
        "Chiara": "https://d2y3m460t2850n.cloudfront.net/v1/7fb94870c705e92df15c4584ba1da0fb.png",
        "Martina": "https://d2y3m460t2850n.cloudfront.net/v1/2613a995711ce9294bf86980f2448fe5.png",
        "Graziana": "https://d2y3m460t2850n.cloudfront.net/v1/31ce18b2cf3a1282aaada22f7a296bca.png",
        "Marina": "https://d2y3m460t2850n.cloudfront.net/v1/76acfed815c6725def94e9a764432654.png",
        "Francesca": "https://d2y3m460t2850n.cloudfront.net/v1/a22fd4e3c531cba65b84c8c57c3c595f.png",
        "Asia": "https://d2y3m460t2850n.cloudfront.net/v1/7383286c722711edba7328ef4124a4e6.png",
        "Anna": "https://d2y3m460t2850n.cloudfront.net/v1/310a25fd644a1da0121ecae7c0c945d7.png",
        "Marta": "https://d2y3m460t2850n.cloudfront.net/v1/5efbf5d17cc1a320f0bc186a97b72ad7.png",
        "Giulia 2": "https://d2y3m460t2850n.cloudfront.net/v1/e0c97a1f7ce874990c14be00c3e252d8.png",
        "Giusy": "https://d2y3m460t2850n.cloudfront.net/v1/7e1bd181b071c801d7486ef20d75c20f.png",
        "Francesca 2": "https://d2y3m460t2850n.cloudfront.net/v1/44c123a922be07f0d950dd3f39d5a6a3.png",
        "Sofia": "https://d2y3m460t2850n.cloudfront.net/v1/53bc9ef55d741c6ed7cac2d56754b7e6.png",
        "Giada": "https://d2y3m460t2850n.cloudfront.net/v1/7af6f24bbde110ef08d1ca5aac89e058.png",
        "Maddalena": "https://d2y3m460t2850n.cloudfront.net/v1/4cd183f75d0d49d6277f5a5693b49059.png",
        "Cecilia": "https://d2y3m460t2850n.cloudfront.net/v1/94fb07f9e2d34f9e63e7e94f5ce36517.png",
        "Lorella": "https://d2y3m460t2850n.cloudfront.net/v1/4531db58c76d7b48ff2cb55eb029a3b7.png",
        "Clara": "https://d2y3m460t2850n.cloudfront.net/v1/7673cf1f3ad9c90861a9b4262503b893.png",
        "Antonella": "https://d2y3m460t2850n.cloudfront.net/v1/31f90cb23981e9df64d9a7768fb138f1.png",
        "Simona": "https://d2y3m460t2850n.cloudfront.net/v1/1f48e14dff076b9468f4b2d707c585f2.png",
        "Raffaella": "https://d2y3m460t2850n.cloudfront.net/v1/b4ccb87e0ef57338d221c4bce739f242.png",
        "Jessica": "https://d2y3m460t2850n.cloudfront.net/v1/45e77c0edb570c0a8364a5608ab14fb7.png",
        "Jlenia": "https://d2y3m460t2850n.cloudfront.net/v1/39bb46177c893e153431c9a4d078c01f.png",
        "Silvia": "https://d2y3m460t2850n.cloudfront.net/v1/adf288ff54b58906a9005fb0ff7bf118.png",
        "Giulia": "https://d2y3m460t2850n.cloudfront.net/v1/005f78f6922ea01ebe91c996b84ad72e.png",
        "Valentina": "https://d2y3m460t2850n.cloudfront.net/v1/4b411c9b239fecf8c10b03164767a7f8.png",
        "Laura": "https://d2y3m460t2850n.cloudfront.net/v1/05d6dd3e25cdb325eecf822f6cf7282f.png"
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