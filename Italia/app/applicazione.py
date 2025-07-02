import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import utils as uts
import datetime
import locale

# App developer:     Enzo Schitini
# Date:              20/09/2024

# Analisi del mese
# Analisi della professoressa

# Imposta il colore dello sfondo della pagina e della barra laterale
bandiera = 'https://th.bing.com/th/id/R.48651b91715991f28ac67418cececd1f?rik=3nKg00xYvodT5Q&pid=ImgRaw&r=0'
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Lezioni di Babbel", page_icon=bandiera)

# Impostazioni della barra laterale
st.sidebar.image("https://raw.githubusercontent.com/enzoschitini/repository-data-science-library/main/Italia/Image/babbel-logo.png", width=200)
st.sidebar.write('# Lezioni di Babbel')
st.sidebar.write('')

# Contenuto della tua app Streamlit
st.image(bandiera, width=50)
st.write("# Bentornato!")
st.write("---")

@st.cache_data
def load_data():
    df = pd.read_csv('C:/Users/schit/Documents/Lezioni/Lezioni.csv')#.drop(columns='Unnamed: 0')
    return df

# Load the data
#df = load_data()
df = pd.read_csv('C:/Users/schit/Documents/Lezioni/Lezioni.csv')#.drop(columns='Unnamed: 0')

#pd.DataFrame(df[(df['Index'] >= 269) & (df['Index'] <= 294)]['Professoressa'].value_counts().head(25))
df['MESE_ANNO'] = df['Mese'].astype(str) + '_' + df['Anno'].astype(str)

df_ascending_false = df.sort_values(by='Data', ascending=False)

col1, col2 = st.columns(2)
totale, colonne_totale = df.shape

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

# Impostare un periodo da analizzare 
def periodo(df, totale):
    modo = uts.scegliere_opzione_laterale('Scegli come vuoi dividere il periodo', ['Data', 'Ultimi Giorni', 'Periodo'])
    if modo == 'Data':
        df['Data'] = pd.to_datetime(df['Data'])

        # Get the min and max dates and convert them to 'date' format
        max_data = df['Data'].max().date()
        min_data = df['Data'].min().date()

        # Date inputs in the sidebar, using 'date' format
        data_iniziale = st.sidebar.date_input('Data iniziale',
                    value=min_data,
                    min_value=min_data,
                    max_value=max_data)

        data_finale = st.sidebar.date_input('Data finale',
                    value=max_data,
                    min_value=min_data,
                    max_value=max_data)

        # Filter the DataFrame based on the selected date range
        df = df[(df['Data'].dt.date >= data_iniziale) & (df['Data'].dt.date <= data_finale)]
    
    elif modo == 'Ultimi Giorni':
        # Ultimi giorni
        valori = st.sidebar.slider('Seleziona un intervallo di numeri', 
                        min_value=1, max_value=totale, value=(1, totale))

        # Filtra il DataFrame in base all'intervallo selezionato
        df = df[(df['Index'] >= valori[0]) & (df['Index'] <= valori[1])]

        st.sidebar.write(f'Da {df.head(1)['Mese'].values[0]} {df.head(1)['Anno'].values[0]} fino a {df.tail(1)['Mese'].values[0]} {df.tail(1)['Anno'].values[0]}')
    
    elif modo == "Periodo":
        lista_mesi_anno = df['MESE_ANNO'].unique()
        
        p1 = lista_mesi_anno.tolist().index(uts.scegliere_opzione_laterale('Scegli il primo mese del periodo', lista_mesi_anno))
        p2 = lista_mesi_anno.tolist().index(st.sidebar.selectbox('Scegli il secondo mese del periodo', 
                                                                 lista_mesi_anno, index=len(lista_mesi_anno) - 1))

        df = df[df['MESE_ANNO'].isin(lista_mesi_anno[p1:p2+1])]

    return df

df = periodo(df, totale)
totale, colonne_totale = df.shape

with col1:
    st.write(f"### {totale} Lezioni fatte!!!")
    st.write(f"Dal Lunedì 22 Maggio 2023 fino a {df.tail(1)['Data'].values[0]}")

    def main():
        with st.expander("Nuova Lezione"):
            st.write("### Aggiugere una nuova lezione alla raccolta")
            # Percorso del file CSV
            csv_file = 'Lezioni.csv'

            # Funzione per aggiungere una nuova riga al DataFrame e salvare su file
            def add_row(index, data, professoressa, ora, livello, lezione, giorno, mese, anno):
                global df
                new_row = {'Index': index, 'Data': data, 'Professoressa': professoressa, 'Ora': ora, 'Livello': livello, 'Lezione': lezione, 'Giorno della settimana': giorno,
                        'Mese': mese, 'Anno': anno}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                # Leggendo le date per aggiungere l'anno che è stato impostato
                df['Data'] = pd.to_datetime(df['Data'])
                df.to_csv(csv_file, index=False)  # Salva il DataFrame nel file CSV

            # Input dell'utente
            col01, col02 = st.columns(2)
            
            # Ottieni l'ora attuale
            ora_corrente = datetime.datetime.now()

            # Estrai solo l'ora e rimuovi lo zero iniziale
            ora_senza_minuti_secondi = ora_corrente.strftime("%H")
            ora_intera = int(ora_senza_minuti_secondi)

            # Imposta la localizzazione in italiano
            locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

            # Ottieni la data e l'ora attuali
            data_corrente = datetime.datetime.now()

            # Estrai il nome del giorno (in italiano)
            giorno_settimana = data_corrente.strftime("%A")

            # Mostra il nome del giorno
            #st.write(giorno_settimana)

            with col01:
                index = df.tail(1)['Index'].values[0] + 1
                professoressa = st.text_input('Professoressa')
                #livello = st.text_input('Livello', value='C1')
                livello = uts.scegliere_opzione('Livello', ['B1', 'B2', 'C1'])
                lezione = st.text_input('Lezione')
                ora = st.number_input('Ora', min_value=0, max_value=22, value=ora_intera)
            with col02:
                # Definisci la data predefinita
                data_predefinita = datetime.date.today()

                # Input per la selezione della data in Streamlit
                data = st.date_input("Seleziona una data", value=data_predefinita)
                giorno = uts.scegliere_opzione('Giorno', ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica'])
                #giorno = st.text_input('Giorno')
                mese = st.text_input('Mese', value=df.tail(1)['Mese'].values[0])
                anno = st.number_input('Anno', min_value=2022, value=2025)

            # Bottone per aggiungere una riga
            if st.button('Aggiungi'):
                add_row(index, data, professoressa, ora, livello, lezione, giorno, mese, anno)
                st.success('Dati aggiunti con successo!')

            # Mostra il DataFrame aggiornato
            st.write('DataFrame Attuale:')
            #st.dataframe(df)
            #df = pd.read_csv('Lezioni.csv').drop(columns='Unnamed: 0')
            st.write(df.tail().drop(columns='MESE_ANNO'))


    if __name__ == "__main__":
        main()
with col2:
    st.write(f"### 👨‍🏫 {df.tail(1)['Professoressa'].values[0]} {df.tail(1)['Lezione'].values[0]} - {df.tail(1)['Giorno della settimana'].values[0]} alle {df.tail(1)['Ora'].values[0]}h")
    mese_attuale = df.tail(1)['Mese'].values[0]
    status = uts.differenza_giorni(df[df['MESE_ANNO'] == df.tail(1)['MESE_ANNO'].values[0]])[1]

    st.write(f"{mese_attuale}: {df[df['MESE_ANNO'] == df.tail(1)['MESE_ANNO'].values[0]].shape[0]} {status}")

    def main():
        with st.expander("Ultime Lezione"):
            st.write(df.tail(10))

    if __name__ == "__main__":
        main()

st.write("---") 

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

def main():
    with st.expander("Analisi dei livelli"):
        uts.distribuzione_delle_categorie_semplice(df, 'Livello')

        uts.distribuzione_delle_categorie('Giorno della settimana', df, 'BarV')
        uts.distribuzione_delle_categorie('Livello', df, 'Line')
        #uts.distribuzione_delle_categorie('Giorno della settimana', df[df['Livello'] == 'B1'], 'Bar')
        #uts.distribuzione_delle_categorie('Giorno della settimana', df[df['Livello'] == 'C1'], 'Bar')
    with st.expander("Analisi degli orari"):
        uts.distribuzione_delle_categorie_semplice(df, 'Giorno della settimana')
        #df['Ora_categoria'] = df['Ora'].astype('category')
        uts.distribuzione_delle_categorie('Ora', df, 'BarV')
        uts.distribuzione_delle_categorie('Giorno della settimana', df, 'BarO')
        #df.drop(columns=['Ora_categoria'], inplace=True)

if __name__ == "__main__":
    main()

uts.show_intervalloCV()

# Professoresse
dic_di_professoresse = df['Professoressa'].value_counts()
lista = list(df['Professoressa'].value_counts().to_dict().keys())
st.write(f"### 👨‍🏫 Professoresse: {len(df['Professoressa'].unique())}")

nomi = []
quantita = []
orari = []

for x in lista:
    orari.append(round(df[df['Professoressa'] == x]['Ora'].mean()))
    quantita.append(df[df['Professoressa'] == x]['Index'].count())

df_professoresse = pd.DataFrame({'Nome': lista, 'Qauntità': quantita, 'Media Orario': orari})
#st.write(df_professoresse)

col001, col002 = st.columns([1, 3])
with col001:
    professoressa_scelta = uts.scegliere_opzione('Scegli una professoressa', lista)
    st.write('---')

    if uts.dic_foto(professoressa_scelta) != "Professoressa non trovata":
        st.image(uts.dic_foto(professoressa_scelta), width=150)

    st.write(f'## {lista.index(professoressa_scelta) + 1}° {professoressa_scelta}')
    st.write(f'### Totale di {df[df['Professoressa'] == professoressa_scelta].shape[0]} lezioni fatte')
    st.write('---')
    st.write(f"Media dell'orario: {round(df[df['Professoressa'] == professoressa_scelta]['Ora'].mean(), 2)}")
with col002:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        pass
    with col2:
        cosa_vuoi_vedere = uts.scegliere_opzione('Imposta cosa vuoi vedere', ['Professoressa', 'Livello', 'Giorno della settimana'])
    with col3:
        imposta_grafico = uts.scegliere_opzione('Imposta cosa vuoi vedere', ['BarO', 'BarV', 'Line'])
    st.write('---')
    uts.distribuzione_delle_categorie(cosa_vuoi_vedere, df[df['Professoressa'] == professoressa_scelta], imposta_grafico)


# Enzo Schitini