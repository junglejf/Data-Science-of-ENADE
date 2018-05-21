# -*- coding: utf-8 -*-
"""
Created on Sat May 20 21:04:34 2017

@author: jungl
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

adf = [0]*4
df = [0]*4
ano = 2005
cont = 0
notasCC = []
colunas= ['','']
for i in range (2005,2015,3):
    ### Criando nosso data FRame ###
    filtro = ['nt_ce','nt_ger','co_curso']
    cod = str(ano)
    print(cod, i)
    pdf = pd.read_csv('C:/Users/jungl/Documents/PythonProjects/me'+str(ano)+'.csv',encoding = "latin1" , sep = ";" , usecols = filtro)#Reading the dataset in a dataframe using Pandas
    #print(pdf.head(5))
    pdf = pdf.rename(columns={'nt_ger': 'nt_ger'+cod , 'nt_ce' : 'nt_ce'+cod})
    colunas[0]=('nt_ger'+cod)
    colunas[1]=('nt_ce'+cod)
    ### Filtrando df pelo código do curso de Ciência da Computação-UFF ###
    filtro_curso_ICUFF = 12710
    pdf = pdf[(pdf.co_curso == filtro_curso_ICUFF)]
    pdf = pdf.drop('co_curso', 1)
    
    #print(pdf)
    ### ELIMINAR OS FALTOSOS ###
    pdf = pdf.dropna()
    adf[cont] = pdf
    pdf = pdf[pdf != 0.].dropna(axis=0) # to remove the rows with 0
    #print(pdf)
    #print(pdf.head(6))
    pdf.sort_values(colunas, inplace=True,ascending = True)
    #print(pdf)
    pdf.index = range(len(pdf))
    df[cont] = pdf
    ano += 3
    cont += 1
    
for i in range(4):
    print (df[i])

#aa = df[0].plot(kind = 'scatter' , x = 'nt_ger2005', y = 'nt_ce2005')
#df[0].plot(kind = 'scatter' , x = 'nt_ger2008', y = 'nt_ce2008',color='DarkGreen',label='2008',aa= aa)
ax = df[0].plot(kind='scatter', x = 'nt_ger2005', y = 'nt_ce2005',color='Black',label="2005")
df[1].plot(kind='scatter', x = 'nt_ger2008', y = 'nt_ce2008',ax=ax,color='DarkGreen',label="2008")
df[2].plot(kind='scatter', x = 'nt_ger2011', y = 'nt_ce2011',ax=ax,color='Red',label="2011")
df[3].plot(kind='scatter', x = 'nt_ger2014', y = 'nt_ce2014',ax=ax,label="2014")
ax.set_xlabel("Nota Geral")
ax.set_ylabel("Nota Conhecimentos Específicos")

for i in range(4):
    df[i]['ano'] = 2005+(i*3)
    print(df[i].describe())

ax = df[0].plot( x = 'nt_ger2005', y = 'nt_ce2005',label="2005")
df[1].plot( x = 'nt_ger2008', y = 'nt_ce2008', ax=ax,label="2008")
df[2].plot( x = 'nt_ger2011', y = 'nt_ce2011',ax=ax,label="2011")
df[3].plot( x = 'nt_ger2014', y = 'nt_ce2014',ax=ax,label="2014")
ax.set_xlabel("Nota Geral")
ax.set_ylabel("Nota Conhecimentos Específicos")     

lm = [0]*4    
# create a fitted model in one line
for i in range(4):
    ano = str(2005+(i*3))
    p1 = 'nt_ger'+ano
    p2 = 'nt_ce'+ano
    lm[i] = smf.ols(formula= p2 +'~'+ p1, data=df[i]).fit()
    print(lm[i].params)  

vmData = {'ano':[2005,2008,2011,2014],
'media':[df[0]["nt_ger2005"].mean(),df[1]["nt_ger2008"].mean(),df[2]["nt_ger2011"].mean(),df[3]["nt_ger2014"].mean()],
'max':[df[0]["nt_ger2005"].max(),df[1]["nt_ger2008"].max(),df[2]["nt_ger2011"].max(),df[3]["nt_ger2014"].max()],
'min':[df[0]["nt_ger2005"].min(),df[1]["nt_ger2008"].min(),df[2]["nt_ger2011"].min(),df[3]["nt_ger2014"].min()] }    
vm = pd.DataFrame(vmData,columns=['ano','media','min','max'])

gvm = vm.plot(kind='scatter', x = 'ano', y = 'media',color='red')
vm.plot(kind='scatter', x = 'ano', y = 'min',color='blue',ax=gvm)
vm.plot(kind='scatter', x = 'ano', y = 'max',color='black',ax=gvm)

vm2 = pd.DataFrame(vmData, columns=['ano','media'])
lm.append(smf.ols(formula= 'media~ano', data=vm2).fit())

nextEnades = pd.DataFrame({'ano': [2017,2020,2023,2026,2029,2032,2035]})
lm[-1].predict(nextEnades)
projection = pd.DataFrame(np.array([[2017,52],[2020,55],[2023,58],[2026,61],[2029,64],[2032,67],[2035,70]]),columns=['ano','media'])#path =r'C:/Users/jungl/Documents/PythonProjects' # use your path
vm2 = vm2.append(projection)

vm_MinMax = pd.DataFrame(vmData, columns=['min','max','ano'])


preds=[0]*5
X_new = pd.DataFrame({'nt_ger2005': [df[0].nt_ger2005.min(), df[0].nt_ger2005.max()]})
X_new.head()
preds[0] = lm[0].predict(X_new)

X_new1 = pd.DataFrame({'nt_ger2008': [df[0].nt_ger2005.min(), df[0].nt_ger2005.max()]})
X_new1.head()
preds[1] = lm[1].predict(X_new1)

X_new2 = pd.DataFrame({'nt_ger2011': [df[0].nt_ger2005.min(), df[0].nt_ger2005.max()]})
X_new2.head()
preds[2] = lm[2].predict(X_new2)

X_new3 = pd.DataFrame({'nt_ger2014': [df[0].nt_ger2005.min(), df[0].nt_ger2005.max()]})
X_new3.head()
preds[3] = lm[3].predict(X_new3)

#df[0].plot(kind='scatter', x = 'nt_ger2005', y = 'nt_ce2005',color='Black',label="2005")
#plt.plot(X_new, preds[0], c='black', linewidth=2)
ax = df[0].plot(kind='scatter', x = 'nt_ger2005', y = 'nt_ce2005',color='Black',label="2005")
plt.plot(X_new, preds[0], c='black', linewidth=2)
df[1].plot(kind='scatter', x = 'nt_ger2008', y = 'nt_ce2008',ax=ax,color='DarkGreen',label="2008")
plt.plot(X_new1, preds[1], c='DarkGreen', linewidth=2)
df[2].plot(kind='scatter', x = 'nt_ger2011', y = 'nt_ce2011',ax=ax,color='Red',label="2011")
plt.plot(X_new2, preds[2], c='Red', linewidth=2)
df[3].plot(kind='scatter', x = 'nt_ger2014', y = 'nt_ce2014',ax=ax,label="2014")
plt.plot(X_new3, preds[3],  linewidth=2)
ax.set_xlabel("Nota Geral")
ax.set_ylabel("Nota Conhecimentos Específicos")

for i in range(5):
    print(lm[i].rsquared)

X_new4 = pd.DataFrame({'ano': [vm2.media.min(), vm2.media.max()]})
X_new4.head()
preds[4] = lm[4].predict(X_new4)    
bx = vm2.plot( x = 'ano', y = 'media',color='black')
bx.plot(kind='scatter',x = 'ano', y = 'media',color='red')

ideb = pd.DataFrame({'ano': [2005,2007,2009,2011,2013,2015,2017,2019,2021],'media':[33,32,33,37,40,40,46,49,51]})
ax = vm2.plot( x = 'ano', y = 'media',color='red',label ='enade CC-UFF')
vm2.plot(kind='scatter',x = 'ano', y = 'media',ax=ax,color='black')
ideb.plot(x = 'ano', y = 'media',ax=ax,color='purple',label='ideb RJ')
ideb.plot(kind ='scatter',x = 'ano', y = 'media',ax=ax,color='black')


#########################################################
### Notas com variáveis ruins (Alunos que tiraram 0) ####
### ALunos que tiraram (0) foram excluídos do modelo ####
###########DADOS ANTES DE SEREM AJUSTADOS ###############
#########################################################
vmDataLixo = {'ano':[2005,2008,2011,2014],
'media':[adf[0]["nt_ger2005"].mean(),adf[1]["nt_ger2008"].mean(),adf[2]["nt_ger2011"].mean(),adf[3]["nt_ger2014"].mean()],
'max':[adf[0]["nt_ger2005"].max(),adf[1]["nt_ger2008"].max(),adf[2]["nt_ger2011"].max(),adf[3]["nt_ger2014"].max()],
'min':[adf[0]["nt_ger2005"].min(),adf[1]["nt_ger2008"].min(),adf[2]["nt_ger2011"].min(),adf[3]["nt_ger2014"].min()] }    

lmx = [0]*4    
# create a fitted model in one line
for i in range(4):
    ano = str(2005+(i*3))
    p1 = 'nt_ger'+ano
    p2 = 'nt_ce'+ano
    lmx[i] = smf.ols(formula= p2 +'~'+ p1, data=adf[i]).fit()
    print(lmx[i].params)
predsx=[0]*5
xX_new = pd.DataFrame({'nt_ger2005': [adf[0].nt_ger2005.min(), adf[0].nt_ger2005.max()]})
xX_new.head()
predsx[0] = lmx[0].predict(xX_new)

xX_new1 = pd.DataFrame({'nt_ger2008': [adf[0].nt_ger2005.min(), adf[0].nt_ger2005.max()]})
xX_new1.head()
predsx[1] = lmx[1].predict(xX_new1)

xX_new2 = pd.DataFrame({'nt_ger2011': [adf[0].nt_ger2005.min(), adf[0].nt_ger2005.max()]})
xX_new2.head()
predsx[2] = lmx[2].predict(xX_new2)

xX_new3 = pd.DataFrame({'nt_ger2014': [adf[0].nt_ger2005.min(), adf[0].nt_ger2005.max()]})
xX_new3.head()
predsx[3] = lmx[3].predict(xX_new3)

ax = adf[0].plot(kind='scatter', x = 'nt_ger2005', y = 'nt_ce2005',color='Black',label="2005")
plt.plot(xX_new, predsx[0], c='black', linewidth=2)
adf[1].plot(kind='scatter', x = 'nt_ger2008', y = 'nt_ce2008',ax=ax,color='DarkGreen',label="2008")
plt.plot(xX_new1, predsx[1], c='DarkGreen', linewidth=2)
adf[2].plot(kind='scatter', x = 'nt_ger2011', y = 'nt_ce2011',ax=ax,color='Red',label="2011")
plt.plot(xX_new2, predsx[2], c='Red', linewidth=2)
adf[3].plot(kind='scatter', x = 'nt_ger2014', y = 'nt_ce2014',ax=ax,label="2014")
plt.plot(xX_new3, predsx[3],  linewidth=2)
ax.set_xlabel("Nota Geral")
ax.set_ylabel("Nota Conhecimentos Específicos")

vma = pd.DataFrame(vmDataLixo,columns=['ano','media','min','max'])

ax = vma.plot( x = 'ano', y = 'media',color='red')
vma.plot(kind='scatter',x = 'ano', y = 'media',ax=ax,color='black')
##################################################################################
### Modelo anterior foi reformulado ##############################################
##################################################################################
