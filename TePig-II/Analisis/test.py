#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 08:43:53 2017

https://slowinver.com/invertir-en-bolsa-a-corto-plazo/

"""

import googlefinance.client as gfc
from alpha_vantage.timeseries import TimeSeries
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
RSI_MIN_COMPRA = 40

# Cargamos Vectores
ts = TimeSeries(key='K4UB1680TM6HSR87', output_format='pandas')
#data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data, meta_data = ts.get_daily(symbol=(indice+'.MC'), outputsize='full')

# Ajsutes de vectores
df = data[-600:]
df['Close'] = df['close']
df['Low'] = df['low']
df['High'] = df['high']

# Calculamos las medias
df['5SMA'] = pd.rolling_mean(df['Close'], 5)
df['100SMA'] = pd.rolling_mean(df['Close'], 100)

# Calculamos el RSI
df['RSI'] = RSI(df['Close'], 14)

# Calculando el ATR de 10 dias
distance = 10
df['TR'] = df['High'].subtract(df['Low']).rolling(distance).mean()
df['ATR'] = df['TR'].ewm(span = 10).mean()
df['ATR'] = ( df['ATR'].shift(1)*13 + df['TR'] ) /  14

# Dibujamos las medias
#df = df.drop('Open',1)
#df = df.drop('High',1)
#df = df.drop('Low',1)
#df = df.drop('Volume',1)
#df.plot(figsize=(15, 5))

# Buscamos los cruces de las medias
fechas = df.index.tolist()
close = df['Close'].values
mmBaja = df['5SMA'].values
mmAlta = df['100SMA'].values
low = df['Low'].values
atr = df['ATR'].values
high = df['High'].values        
rsi = df['RSI'].values        

# AJUSTAMOS LOS VECTORES
#close = close[-1:]
#diff = diff[-1:]
#rsi = rsi[-1:]
         
# FILTRO OPERACIONES
# Seleccionamios aquellos que hacen cruce
# 
# El en array de operaciones.
operaciones = [] 
compro = -1
esperarUnDia = 0
diaCompra = 0
fechaCompra = ''
for i in range(0,len(close)):
   if (compro < 0):
       # Calculo cuando comprar
       v = close[i]
       r = rsi[i]
       mediaB = mmBaja[i]
       mediaA = mmAlta[i]
       # Calculamos si los tres valores anteriores han sido bajistas
       bajistasAnteriores = False
       if (i>2):
           bajaLow = ((close[i-2]-close[i])/close[i])
           #if ((close[i-2]>close[i-1]) and (close[i-1]>close[i])):
           if ((close[i-1]>close[i])):
               bajistasAnteriores = True
       #if ((d<0) and (ant>0) and (r<RSI_MIN_COMPRA)):
       if ((mediaA<v) and (bajistasAnteriores)):
           # Este momento determina la compra
           compro = v - atr[i]
           if (low[i+1] > compro):
               # El dia siguiente compro más baroto, si no se cumple no compro
               compro = -1
           else:
               #print ('+++ INVERTIR en '+str(i)+' - fecha -> '+str(fechas[i])+' - compro -> '+str(compro))
               diaCompra = i
               fechaCompra = str(fechas[i])
               esperarUnDia = 5
   else:
        # Estoy en fase de venta
        rentabilidad = (close[i-1]-compro)/compro
        if (rentabilidad > 0.035):
            #print ('+++ VENDO en '+str(i)+' - fecha -> '+str(fechas[i])+' - compro -> '+str(close[i-1]))
            print (indice + '\t'+str(rentabilidad)+ '\t'+str((i-diaCompra))+ '\t'+str(rentabilidad*3000)+ '\t'+str(r)+ '\t'+str(bajaLow)+ '\t'+str(fechaCompra))
            compro = -1 
            continue
        if (esperarUnDia>0):
            esperarUnDia = esperarUnDia - 1
            continue
        else:
            print (indice + '\t'+str(rentabilidad)+ '\t'+str((i-diaCompra))+ '\t'+str(rentabilidad*3000)+ '\t'+str(r)+ '\t'+str(bajaLow)+ '\t'+str(fechaCompra))
            compro = -1 

        
