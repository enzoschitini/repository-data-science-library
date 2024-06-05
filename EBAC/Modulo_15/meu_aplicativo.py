import streamlit as st

st.title('Meu Primeiro Aplicativo Streamlit')
st.header('Olá, Mundo!')
st.subheader('Olá, Mundo!')
st.markdown("---")

image_url = "https://github.com/enzoschitini/repository-data-science-library/blob/main/image/Copertina-Profilo.png?raw=true"
st.image(image_url, caption='Immagine tramite link')


st.markdown('''
## **Bem-Vindo(a)! • Veja o que eu fiz de melhor com cientista de dados**
            ''')

st.write('Olá, Mundo!')

# Creiamo un input per l'utente
user_input = st.text_input("Scrivi qualcosa qui:")

# Controlliamo se l'utente ha inserito del testo
if user_input:
    # Salva il testo inserito dall'utente
    with open("testo_utente.txt", "w") as file:
        file.write(user_input)
    st.success("Testo salvato con successo!")

# Lista dei valori
valori = ["Valore 1", "Valore 2", "Valore 3", "Valore 4"]

# Creiamo un'interfaccia per selezionare un valore dalla lista
valore_selezionato = st.selectbox("Seleziona un valore:", valori)

# Controlliamo se un valore è stato selezionato
if valore_selezionato:
    # Salva il valore selezionato dall'utente
    with open("valore_selezionato.txt", "w") as file:
        file.write(valore_selezionato)
    st.success("Valore salvato con successo!")


# Divide la larghezza della schermata in due colonne
col1, col2 = st.columns(2)

# Testo per il primo paragrafo
with col1:
    st.write("Questo è il primo paragrafo. Puoi inserire qui il testo che desideri mostrare.")

# Testo per il secondo paragrafo
with col2:
    st.write("Questo è il secondo paragrafo. Puoi inserire qui un altro testo che vuoi mostrare accanto al primo.")

# ------------------------------------------------

# Creiamo un input per l'utente
user_input = st.text_input("Scrivi qualcosa qui:")

# Controlliamo se l'utente ha inserito del testo
if user_input:
    # Salva il testo inserito dall'utente
    with open("testo_utente.txt", "w") as file:
        file.write(user_input)
    st.success("Testo salvato con successo!")

# ------------------------------------------------

# Imposta il valore minimo e massimo per la barra
valore_minimo = 0
valore_massimo = 100

# Crea una barra per l'utente per impostare il valore
valore_selezionato = st.slider("Seleziona un valore:", valore_minimo, valore_massimo)

# Controlla se un valore è stato selezionato
if valore_selezionato == 10:
    st.write('OK!')

# ------------------------------------------------

