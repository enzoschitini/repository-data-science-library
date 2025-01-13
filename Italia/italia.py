import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide', page_title='')
st.sidebar.write('#')

df = pd.read_csv('Lezioni.csv').drop(columns='Unnamed: 0')
df['MESE_ANNO'] = df['Mese'].astype(str) + '_' + df['Anno'].astype(str)
df['Data'] = pd.to_datetime(df['Data'])

# Grafici
####################################################################################################################
####################################################################################################################
####################################################################################################################

def grafico_linea(dizionario_ordinato):
    # Crea il grafico a linee
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list(dizionario_ordinato.keys()), y=list(dizionario_ordinato.values()), mode='lines+markers', name='Linea'))

    # Aggiungi titolo e etichette agli assi
    fig.update_layout(
        title='Quantità di Livelli per MESE_ANNO',
        xaxis_title='MESE_ANNO',
        yaxis_title='Quantità',
        legend_title='Livelli',
        template='plotly_white'
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

####################################################################################################################
####################################################################################################################
####################################################################################################################

df_ascending_false = df.sort_values(by='Data', ascending=False)

MESE_ANNO_ORDINE =['Maggio_2023', 'Giugno_2023', 'Luglio_2023', 'Settembre_2023', 'Ottobre_2023',
                   'Novembre_2023', 'Dicembre_2023', 'Gennaio_2024', 'Febbraio_2024', 'Marzo_2024',
                   'Aprile_2024', 'Maggio_2024', 'Giugno_2024', 'Luglio_2024', 'Agosto_2024']

dic = df_ascending_false.groupby('MESE_ANNO')['Index'].count()
dizionario_ordinato = {chiave: dic[chiave] for chiave in MESE_ANNO_ORDINE if chiave in dic}

grafico_linea(dizionario_ordinato)