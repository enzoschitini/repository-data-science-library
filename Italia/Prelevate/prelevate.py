import pandas as pd

# 1 per sommare e 0 per creare la prima raccolta
operazione = 0

def leggi_file_dividi(nome_file):
    parti_testo = []  # Lista per memorizzare le parti divise del testo
    parte_corrente = []  # Lista temporanea per memorizzare le righe della parte corrente

    with open(nome_file, 'r') as file:
        for riga in file:
            parte_corrente.append(riga.strip())  # Aggiungi la riga alla parte corrente
            # Se abbiamo raggiunto 12 righe, aggiungi la parte corrente alla lista principale e resetta la parte corrente
            if len(parte_corrente) == 12:
                parti_testo.append(parte_corrente)
                parte_corrente = []

        # Se ci sono ancora righe nella parte corrente, aggiungila alla lista principale
        if parte_corrente:
            parti_testo.append(parte_corrente)

    return parti_testo

# Esempio di utilizzo
nome_file = "Prelevate\.txt"
parti_divise = leggi_file_dividi(nome_file)

"""
La funzione leggi_file_dividi ci offre:

['C1  â€¢  MÃ³dulo 1',
 'Parlare utilizzando espressioni latine',
 'AmanhÃ£',
 '07:00',
 '',
 'Silvia',
 'Silvia',
 '',
 'â€¢',
 '55 min',
 '',
 '1/6']
"""

# Controlla se la lista è vuota
if len(parti_divise) == 0:
    print(f"\nATTENZIONE! La lista è vuota. L'esecuzione del programma è stata fermata.")
    print(f"Si prega di controllare l'archivio --> {nome_file}\n")
    # Interrompi l'esecuzione del programma usando 'exit()'
    exit()

# Se la lista non è vuota, continua con il resto del codice
#print("La lista non è vuota. Continua con il resto del programma.")

dizionario = [] # Però non si tratta di un dizionario

# Ora selezioniamo ciò che ci interessa
for x in parti_divise:
    try:
      #print(x[5])
      prelevati = [f'Livello: {x[0]} - Titolo: {x[1]} - Data: {x[2]} - Orario: {x[3]} - Professoressa: {x[5]}']
      dizionario.append(prelevati)
    except IndexError:
       continue

"""
dizionario[1]
['Livello: C1  â€¢  MÃ³dulo 7 - Titolo: Sostenere un colloquio di lavoro - Data: AmanhÃ£ - Orario: 07:00 - Professoressa: Elisa']
"""

def SGE(tutti_i_dati:list, risultato:None = None)->list: # Staccando gli elementi
    tutti = str(tutti_i_dati)

    livello = tutti[tutti.find('Livello'):(tutti.find('Livello') + 11)].replace('Livello: ', '')
    titolo = tutti[tutti.find('Titolo:'):(tutti.find('Data') - 3)].replace('Titolo: ', '')
    data = tutti[tutti.find('Data:'):(tutti.find('Orario') - 3)].replace('Data: ', '')
    orario = tutti[tutti.find('Orario:'):(tutti.find('Professoressa') - 3)].replace('Orario: ', '')
    professoressa = tutti[tutti.find('Professoressa'): - 2].replace('Professoressa: ', '')

    from datetime import datetime, timedelta
    # Ottieni la data di oggi e aggiungi un giorno
    domani = datetime.today() + timedelta(days=1)
    domani = f'{domani.strftime("%Y-%m-%d")}'

    if data == 'AmanhÃ£':
        data = data.replace('AmanhÃ£', f'{domani}')
    elif data == 'Hoje':
        data = data.replace('Hoje', f'{datetime.today().strftime("%Y-%m-%d")}')
    if risultato == 1:
        return livello, titolo, data, orario, professoressa
    else:
        lista = f'Livello: {livello} - Professoressa: {professoressa} - Data: {data} alle: {orario} - Titolo: {titolo}'
        return lista

""" 
Uscite di SGE

SGE(dizionario[0]):
'Livello: C1 - Professoressa: Silvia - Data: 2024-03-15 alle: 07:00 - Titolo: Parlare utilizzando espressioni latine'

SGE(dizionario[x], 1):
('B1',
 'Cavarsela in un ufficio pubblico',
 '2024-03-15',
 '12:00',
 'Mariacristina')

SGE(dizionario[x], 1)[0]
'C1'
"""

Livelli = []
Professoresse = []
Date = []
Orari = []
Titolo = []

for x in range(len(dizionario)):
    Livelli.append(SGE(dizionario[x], 1)[0])
    Professoresse.append(SGE(dizionario[x], 1)[4])
    Date.append(SGE(dizionario[x], 1)[2])
    Orari.append(SGE(dizionario[x], 1)[3])
    Titolo.append(SGE(dizionario[x], 1)[1])

df = pd.DataFrame({
    'Livelli':Livelli,
    'Professoresse':Professoresse,
    'Date':Date,
    'Orari':Orari,
    'Titolo':Titolo
})

df['Livelli'].astype('category')
df['Professoresse'].astype('category')
#df['Date'] = pd.to_datetime(df['Date'])
df['Orari'].astype('category')
df['Titolo'].astype('category')

#operazione = 1

if operazione == 1:
    dataframe = pd.read_csv('Prelevate\Prelevate.csv')
    dataframe = dataframe.drop(columns='Unnamed: 0', axis=1)
    #df = df.drop(columns='Unnamed: 0', axis=1)
    df_finale = pd.concat([dataframe, df])
    df_finale.to_csv('Prelevate\Prelevate.csv')
else:
    df.to_csv('Prelevate\Prelevate.csv')

# Apri il file in modalità scrittura (sovrascrive il contenuto esistente)
with open(nome_file, 'w') as file:
    # Sovrascrivi il contenuto del file con una stringa vuota
    file.write('')

# Creato da Enzo Schitini 😉