import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import streamlit as st 

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(plt)
    return None

st.set_page_config(layout='wide', page_title='Análise SINASC',
                   page_icon="https://www.nicepng.com/png/detail/353-3532899_flag-map-of-rondonia-mapa-de-rondonia-png.png")
st.write('# Análise SINASC')

sinasc = pd.read_csv('./input/SINASC_RO_2019.csv')

sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)
max_data = sinasc.DTNASC.max()
min_data = sinasc.DTNASC.min()

#st.write(max_data)
#st.write(min_data)

data_inicial = st.sidebar.date_input('Data inicial',
              value=min_data,
              min_value=min_data,
              max_value=max_data)
st.sidebar.write(data_inicial)

data_final = st.sidebar.date_input('Data final',
              value=max_data,
              min_value=min_data,
              max_value=max_data)
st.sidebar.write(data_final)

sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]
#st.write(sinasc['DTNASC'])

#max_data = sinasc.DTNASC.max()[:7]
#print(max_data)
#os.makedirs('./output/'+max_data, exist_ok=True)

plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
#plt.savefig('./output/'+max_data+'/media idade mae por data.png')

plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
#plt.savefig('./output/'+max_data+'/media idade mae por sexo.png')

plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
#plt.savefig('./output/'+max_data+'/media peso bebe por sexo.png')

plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
#plt.savefig('./output/'+max_data+'/PESO mediano por escolaridade mae.png')

plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')
#plt.savefig('./output/'+max_data+'/media apgar1 por gestacao.png')