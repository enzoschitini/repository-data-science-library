import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import utils as uts

# Imposta il colore dello sfondo della pagina e della barra laterale
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Lezioni di Babbel")

st.sidebar.image("https://q8v3g6g4.rocketcdn.me/wp-content/uploads/2019/12/image1-3.png", width=200)
st.sidebar.write('# Lezioni di Babbel')
st.sidebar.write('')

# Contenuto della tua app Streamlit
st.image("https://th.bing.com/th/id/R.48651b91715991f28ac67418cececd1f?rik=3nKg00xYvodT5Q&pid=ImgRaw&r=0", width=50)
st.write("# Benvenuto nella mia app Streamlit!")
st.write("---")

df = pd.read_csv('Lezioni.csv').drop(columns='Unnamed: 0')
#pd.DataFrame(df[(df['Index'] >= 269) & (df['Index'] <= 294)]['Professoressa'].value_counts().head(25))
df['MESE_ANNO'] = df['Mese'].astype(str) + '_' + df['Anno'].astype(str)

df_ascending_false = df.sort_values(by='Data', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.write("Bem Vindo(a)!!!")
with col2:
    st.write("Bem Vindo(a)!!!")
st.write("---") 

# Definisci l'ordine dei mesi e anni
MESE_ANNO_ORDINE = ['Maggio_2023', 'Giugno_2023', 'Luglio_2023', 'Agosto_2023', 'Settembre_2023', 'Ottobre_2023',
                'Novembre_2023', 'Dicembre_2023', 'Gennaio_2024', 'Febbraio_2024', 'Marzo_2024',
                'Aprile_2024', 'Maggio_2024', 'Giugno_2024', 'Luglio_2024', 'Agosto_2024', 'Settembre_2024']


dizionario_ordinato = uts.ordina_in_base_al_periodo(df_ascending_false.groupby('MESE_ANNO')['Index'].count())
ora_media = uts.ordina_in_base_al_periodo(round(df_ascending_false.groupby('MESE_ANNO')['Ora'].mean()))

# Esempio di chiamata alla funzione
uts.grafico_di_linea(
    list_dic=[dizionario_ordinato, ora_media], 
    names=['Lezioni', "L'ora media"], 
    title='Quantità di Lezioni per periodi', 
    xaxis_title='Periodo', 
    yaxis_title='Quantità', 
    legend_title=''
)

uts.distribuzione_delle_categorie('Livello')
uts.show_intervalloCV()