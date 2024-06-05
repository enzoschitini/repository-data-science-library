import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()  

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None

def list_plot(data, max):
    loc = 'output'
    plota_pivot_table(data, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento','data de nascimento') #'./output/'+max+'/quantidade de nascimento.png'
    plt.savefig(loc+'\quantidade de nascimento.png')

    plota_pivot_table(data, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
    plt.savefig(loc+'\media idade mae por sexo.png') #'./output/'+max+'/media idade mae por sexo.png'

    plota_pivot_table(data, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
    plt.savefig(loc+'\media peso bebe por sexo.png') #'./output/'+max+'/media peso bebe por sexo.png'

    plota_pivot_table(data, 'PESO', 'ESCMAE', 'median', 'apgar1 medio','gestacao','sort')
    plt.savefig(loc+'\media apgar1 por escolaridade mae.png') # './output/'+max+'/media apgar1 por escolaridade mae.png'

    plota_pivot_table(data, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')
    plt.savefig(loc+'\media apgar1 por gestacao.png')  # './output/'+max+'/media apgar1 por gestacao.png'

    plota_pivot_table(data, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio','gestacao','sort')
    plt.savefig(loc+'\media apgar5 por gestacao.png') # './output/'+max+'/media apgar5 por gestacao.png'


sinasc = pd.read_csv('input\SINASC_RO_2019.csv')
max_data = sinasc.DTNASC.max()[:7]

loc = 'output' 
os.makedirs(loc, exist_ok=True)
list_plot(sinasc, max_data)