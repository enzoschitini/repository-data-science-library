import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

class conversione(object):
    def __init__(self, data_frame, colonna, valore) -> None:
        self.data_frame = data_frame
        self.colonna = colonna
        self.valore = valore
    
    def filtro(self):
         df = self.data_frame
         df = df[df[self.colonna] == self.valore]
         return df

    def sep_colonne(self):
        categorici = self.filtro()
        categorici = categorici.select_dtypes('object')
        numerici = self.filtro()
        numerici = numerici.select_dtypes('number')

        return categorici, numerici
    
    def metriche(self, variabile):
        df_grafico = self.sep_colonne()[0] # DataFrame con dati categorici
        df_grafico = df_grafico[[variabile]] # Impostando la colonna da analizzare

        frame = self.filtro() # Totale di righe
        totale_righe, _ = frame.shape

        categorie = list(set(df_grafico[variabile].to_list())) # Lista con le categorie
        valori = df_grafico[variabile].value_counts().to_list() # Valori delle categorie

        percentuali = []

        for x in valori:
            num = round(((x / totale_righe) * 100), 0)
            percentuali.append(num)
        
        percentuali = list(map(int, percentuali))

        return categorie, percentuali
    
    def grafico(self, variabile):
        x = self.metriche(variabile)[0]
        y = self.metriche(variabile)[1]

        plt.bar(x,y, color='green')
        plt.yticks(rotation=45)
        plt.title(variabile)
        plt.xlabel('')
        plt.ylabel('Percentuale')
        plt.savefig('Gráfico')
        plt.show()