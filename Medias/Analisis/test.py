#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 08:43:53 2017

"""

import googlefinance.client as gfc
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd


# FUNCIONES
def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
    pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)


# PARAMETROS
indice = sys.argv[1]
POR_LOST = 0.05
POR_WIN = 0.085
RSI_MIN_COMPRA = 30

# Cargamos Vectores
param = {
    'q': indice, # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "BME", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "2Y" # Period (Ex: "1Y" = 1 year)
}                
df = gfc.get_price_data(param)

# Calculamos las medias
df['7SMA'] = pd.rolling_mean(df['Close'], 5)
df['13SMA'] = pd.rolling_mean(df['Close'], 13)

# Calculamos el RSI
df['RSI'] = RSI(df['Close'], 14)

# Dibujamos las medias
df = df.drop('Open',1)
#df = df.drop('High',1)
#df = df.drop('Low',1)
df = df.drop('Volume',1)
#df.plot(figsize=(15, 5))

# Buscamos los cruces de las medias
fechas = df.index.tolist()
close = df['Close'].values
minimos = df['Low'].values
maximos = df['Low'].values

df['Diff'] = df['7SMA'] - df['13SMA'] 
#df.plot(y=['RSI'])
diff = df['Diff'].values
rsi = df['RSI'].values         
         
# FILTRO OPERACIONES
# Seleccionamios aquellos que hacen cruce
# 
# El en array de operaciones.
indList = []
ant = 0
operaciones = [] # Alternativamente Compra - Vento o Venta - Compra segun tipo
tipo = 0 # 1 -> Compra - Venta o 2 -> Venta - Compra
for i in range(0,len(close)):
   d = diff[i]
   r = rsi[i]
   #if ((d<0) and (ant>0) and (r<RSI_MIN_COMPRA)):
   if ((r<RSI_MIN_COMPRA) and (d<0)):
       #print (i,'cruze B - Vende')
       # Este momento determina la compra
       operaciones.append(i)
   ant = d          

# Realizamos las inversiones en los seleccionados
dinero = 3000
beneficio = 0
salida_lost = 0
salida_win = 0
for ap in operaciones:
    compro = close[ap]
    if ((ap+6)>=len(close)):
        break
    close[ap+1:ap+6]
    minimo = min(minimos[ap+1:ap+6])
    maximo = max(maximos[ap+1:ap+6])
    if (((maximo-compro)/compro)>POR_WIN):
        rentabilidad = 1 + POR_WIN
        salida_win = salida_win + 1
    else:
        if (((compro-minimo)/compro)>POR_LOST):
            rentabilidad = 1 - POR_LOST
            salida_lost = salida_lost + 1
        else:
            rentabilidad = (1+(close[ap+6]-compro)/compro)
    beneficio = dinero * (rentabilidad-1) + beneficio
    beneficio = beneficio - 16
    
if (beneficio==0):
    print (indice+","+str(len(operaciones))+","+str(dinero)+","+str((0))+","+str((beneficio))+","+str(0)+","+str(0)+","+str(0))    
else:
    print (indice+","+str(len(operaciones))+","+str(dinero)+","+str((beneficio)/3000)+","+str((beneficio))+","+str((beneficio)/len(operaciones))+","+str(salida_lost)+","+str(salida_win))
