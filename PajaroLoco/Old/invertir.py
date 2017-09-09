#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 08:43:53 2017

Estimacion de inversion a partir de Bandas de Bollinger.

"""

import googlefinance.client as gfc
import numpy as np
import pandas as pd
import sys

def bbands(price, length=30, numsd=2):
    """ returns average, upper band, and lower band"""
    ave = pd.stats.moments.rolling_mean(price,length)
    sd = pd.stats.moments.rolling_std(price,length)
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return np.round(ave,3), np.round(upband,3), np.round(dnband,3)

# PARAMETROS
indice = sys.argv[1]
#indice = 'ANA'
POR_BANDAS = 0.20

# Cargamos Valores del Indice
param = {
    'q': indice, # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "BME", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "2Y" # Period (Ex: "1Y" = 1 year)
}                
df = gfc.get_price_data(param)

# Calculamos las bandas de Bollinger
df['BBave'], df['BBupper'], df['BBlower'] = bbands(df.Close, length=30, numsd=1)

# Buscamos valores por debajo de la banda
fechas = df.index.tolist()
close = df['Close'].values
bblow = df['BBlower'].values
bbup = df['BBupper'].values

# Consideramos solo el último valor
#close = close[-1:]
#bblow = bblow[-1:]
#bbup = bbup[-1:]

# Estas filas son de TEST
close = close[117:117+1]
bblow = bblow[117:117+1]
bbup = bbup[117:117+1]

# Seleccionamios aquellos que nos ofrecen rentabilidad alta
indList = []
for i in range(0,len(close)):
   c = close[i]
   b = bblow[i]
   u = bbup[i]
   maxRent = (u-c)/c
   if ((c < b) and (maxRent > POR_BANDAS)):
       indList.append(i)

# Realizamos las inversiones en los seleccionados
if ((len(indList))>0):
    print ("INVERTIR:"+ indice + " - " + str(fechas[-1:])+ " - " + str(c)+ " - " + str(maxRent)+ " - Salida: " + str((1+maxRent)*c))
else:
    print ("KO: " + indice + " - " + str(fechas[-1:]))


