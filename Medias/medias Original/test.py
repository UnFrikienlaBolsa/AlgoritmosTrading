#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 08:43:53 2017

Estimacion de inversion a partir de Bandas de Bollinger.

"""

import googlefinance.client as gfc
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd


# PARAMETROS
indice = sys.argv[1]

# Cargamos Vectores
param = {
    'q': indice, # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "BME", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "5Y" # Period (Ex: "1Y" = 1 year)
}                
df = gfc.get_price_data(param)

# Calculamos las medias
df['7SMA'] = pd.rolling_mean(df['Close'], 7)
df['13SMA'] = pd.rolling_mean(df['Close'], 13)

# Dibujamos las medias
df = df.drop('Open',1)
df = df.drop('High',1)
df = df.drop('Low',1)
df = df.drop('Volume',1)
#df.plot(figsize=(15, 5))

# Buscamos los cruces de las medias
fechas = df.index.tolist()
close = df['Close'].values

df['Diff'] = df['7SMA'] - df['13SMA'] 
#df.plot(y=['Diff'])
diff = df['Diff'].values
         
# Seleccionamios aquellos que nos ofrecen rentabilidad alta
# El en array de operaciones.
indList = []
ant = 0
operaciones = [] # Alternativamente Compra - Vento o Venta - Compra segun tipo
tipo = 0 # 1 -> Compra - Venta o 2 -> Venta - Compra
for i in range(0,len(close)):
   d = diff[i]
   if ((d>0) and (ant<0)):
       #print (i,'cruze A - Compra')
       operaciones.append(i)
       if (len(operaciones)==1):
           tipo = 1
   if ((d<0) and (ant>0)):
       #print (i,'cruze B - Vende')
       # Este momento determina la compra
       operaciones.append(i)
       if (len(operaciones)==1):
           tipo = 2
   ant = d          

# Ajustamos el vector
if (tipo==1):
    # El primer valor indica venta hay que eliminarlo
    operaciones = operaciones[1:]

# Realizamos las inversiones en los seleccionados
dinero = 3000
beneficio = 0
if (1 == 1):
    for ind in range(0,len(operaciones),2):
        compro = close[operaciones[ind]]
        if ((ind+1)==len(operaciones)):
            break
        vendo = close[operaciones[ind+1]]
        rentabilidad = (vendo-compro)/compro
        beneficio = beneficio + (dinero*rentabilidad)
        beneficio = beneficio - 16
        #print (beneficio, dinero, (dinero*rentabilidad),operaciones[ind+1]-operaciones[ind])    

    print (indice+","+str(len(operaciones)/2)+","+str(dinero)+","+str((beneficio)/3000)+","+str((beneficio))+","+str((beneficio)/len(operaciones)))
