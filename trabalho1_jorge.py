# -*- coding: utf-8 -*-
"""
Created on Sat May 20 21:04:34 2017

@author: jungl
"""
from scipy import stats
from scipy.stats import linregress
import pandas as pd
import numpy as np
import matplotlib as plt
import pylab
import seaborn as sns

### Criando nosso data FRame ###
filtro = ['nu_idade','co_curso', 'tp_sexo','ano_fim_2g','ano_in_gra','nt_ger','nt_ce','CO_QPP_I9']
df = pd.read_csv('C:/Users/jungl/Documents/PythonProjects/me2011.csv',encoding = "latin1" , sep = ";" , usecols = filtro) #Reading the dataset in a dataframe using Pandas
print(df.head(5))
df = df.rename(columns={'CO_QPP_I9': 'TempoProva'})
### Filtrando df pelo código do curso de Ciência da Computação-UFF ###
filtro_curso_ICUFF = 12710
df = df[(df.co_curso == filtro_curso_ICUFF)]
print(df)

### ELIMINAR OS FALTOSOS ###
df = df.dropna()
print(df)

### Criando Coluna Delta_Ano e Redefinindo os Index of row ###
# tempo em anos
df.index = range(len(df))
# > ################## [tempo entre o Ensino Médio e a UFF]###### Tempo Entre o Fim do EM ##### ########### Tempo no curso da Graduação    
df['Delta_ano'] =  df['ano_in_gra'] - df['ano_fim_2g']  + df['nu_idade'] + 2010 - df['ano_fim_2g'] + 2011 - df['ano_in_gra'] - 22
print(df)
step = 4
bin_range = np.arange(0, 50+step, step)
out , bins = pd.cut(df['Delta_ano'],bins=bin_range ,include_lowest=True, right=False, retbins=True)
out.value_counts(sort=False).plot.bar(title = "Distribuição de 'Delta_ano'")

### HISTOGRAMA DAS NOTAS ####
# Nota Geral
step = 5
bin_range = np.arange(0, 90+step, step)
out , bins = pd.cut(df['nt_ger'],bins=bin_range ,include_lowest=True, right=False, retbins=True)
out.value_counts(sort=False).plot.bar(title = "Distribuição da Nota Geral")
# Nota de Conhecimentos Específicos
step = 10
bin_range = np.arange(0, 90+step, step)
out , bins = pd.cut(df['nt_ce'],bins=bin_range ,include_lowest=True, right=False, retbins=True)
out.value_counts(sort=False).plot.bar(title = "Distribuição da Nota de Conhecimentos Específicos")
df['TempoProva'].replace({'A' : 1,'B' : 2, 'C' : 3, 'D' : 4, 'E' : 5, '.' : np.random.randint(1,5)  },inplace=True)


#### ANÁLISE UNIVARIADA ####
### Removendo os outiliers das colunas ###
#df.boxplot(column='nt_ger')

print(df)
print('##########################1')
df_tratado = df[((df.nt_ger - df.nt_ger.mean()) / df.nt_ger.std()).abs() < 2.2]
print(df_tratado)
print('##########################2')
df_tratado = df_tratado[((df_tratado.nt_ce - df_tratado.nt_ce.mean()) / df_tratado.nt_ce.std()).abs() < 3]
print(df_tratado)
print('##########################3')
df_tratado = df_tratado[((df_tratado.Delta_ano - df_tratado.Delta_ano.mean()) / df_tratado.Delta_ano.std()).abs() < 1.5]
print(df_tratado)
print('##########################4')
df_tratado = df_tratado[((df_tratado.nu_idade - df_tratado.nu_idade.mean()) / df_tratado.nu_idade.std()).abs() < 2.8]
print(df_tratado)
df_tratado.index = range(len(df_tratado))
### DISTRIBUIÇÃO POR GENERO ###
a = df_tratado['tp_sexo'].value_counts()
print(a)


####ANÁLISE BIVARIADA ####
### Delta_ano vs Nota Geral ###
aux = pd.DataFrame(columns=['Delta_ano','nt_ger'])
aux['Delta_ano'] = df_tratado['Delta_ano']
aux['nt_ger'] = df_tratado['nt_ger']
aux.corr(method = 'pearson')

df_tratado.plot(kind = 'scatter' , x = 'nt_ger', y = 'Delta_ano')
df_tratado.plot(kind = 'scatter' , x = 'nt_ger', y = 'nu_idade')
df_tratado.plot(kind = 'scatter' , x = 'nt_ger', y = 'TempoProva')

df_tratado.boxplot(column = 'nt_ger', by = 'TempoProva')
df_tratado.boxplot(column = 'nt_ger', by = 'Delta_ano')
df_tratado.boxplot(column = 'nt_ger', by = 'tp_sexo')
df_tratado.boxplot(column = 'nt_ger', by = 'nu_idade')


###Introduzindo estrutura auxiliar ####
##tempo que levou pra sair do EM e ir para UFF ### 
di = pd.DataFrame(columns = ['Di','nt_ger']) 
di['Di'] = df_tratado['ano_in_gra'] - df_tratado['ano_fim_2g']
di['DDc'] = 2011 - df_tratado['ano_in_gra']
di['nt_ger'] = df_tratado['nt_ger']
di.boxplot(column = 'nt_ger' , by = 'Di')

### Matriz de Correlação de VAriáveis ###
# Tirar código do curso e adicionar di
df_tratado = df_tratado.drop('co_curso', axis=1)
df_tratado['DDc'] = di['DDc']
df_tratado['Di'] = di['Di']

## Plotar a matriz
corr = df_tratado.corr()
sns.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values)


