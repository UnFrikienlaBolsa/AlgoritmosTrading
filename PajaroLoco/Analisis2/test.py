#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 08:43:53 2017

Estimacion de inversion a partir de Bandas de Bollinger.

"""

import googlefinance.client as gfc
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
import sys
import pandas as pd


def bbands(price, length=30, numsd=2):
    """ returns average, upper band, and lower band"""
    ave = pd.stats.moments.rolling_mean(price,length)
    sd = pd.stats.moments.rolling_std(price,length)
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)
    return np.round(ave,3), np.round(upband,3), np.round(dnband,3)

# PARAMETROS
indice = sys.argv[1]
POR_BANDAS = 0.25
POR_WIN_ESTADISTICO = 0.055
POR_LOST_ESTADISTICO = 0.07

# Cargamos Vectores
param = {
    'q': indice, # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "BME", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "2Y" # Period (Ex: "1Y" = 1 year)
}                
df = gfc.get_price_data(param)

df['BBave'], df['BBupper'], df['BBlower'] = bbands(df.Close, length=30, numsd=1)

# Dibujamos las bandas de Bollinger
#df = df.drop('Open',1)
#df = df.drop('High',1)
#df = df.drop('Low',1)
#df = df.drop('Volume',1)
#df.plot()

# Buscamos valores por debajo de la banda
fechas = df.index.tolist()
close = df['Close'].values
bblow = df['BBlower'].values
bbup = df['BBupper'].values

# Seleccionamios aquellos que nos ofrecen rentabilidad alta
indList = []
for i in range(0,len(close)):
   c = close[i]
   b = bblow[i]
   u = bbup[i]
   maxRent = (u-c)/c
   if ((c < b) and (maxRent > POR_BANDAS)):
       #print (i,fechas[i],c,b,(u-c)/c)
       indList.append(i)

# Realizamos las inversiones en los seleccionados
dinero = 3000
beneficio = 0
salidas_bollinger = 0
win_estadistico = 0
lost_estadistico = 0
for ind in indList:
    ap = ind
    compro = close[ap]
    close[ap+1:ap+6]
    maximo = max(close[ap+1:ap+6])
    POR_WIN = (bbup[ap]-compro)/compro
    if (((maximo-compro)/compro)>POR_WIN):
        rentabilidad = 1 + POR_WIN 
        salidas_bollinger = salidas_bollinger + 1
    else:
        rentabilidad = (1+(close[ap+6]-compro)/compro)
    beneficio = dinero * (rentabilidad-1) + beneficio
    beneficio = beneficio - 16
    print (indice+"\t"+str(compro)+"\t"+str(rentabilidad-1)+"\t"+str(fechas[ap]))
    #print (dinero, rentabilidad)    
    if (((maximo-compro)/compro)>POR_WIN_ESTADISTICO):
        win_estadistico = win_estadistico + 1
    minimo = min(close[ap+1:ap+6])
    if (((compro-minimo)/compro)>POR_LOST_ESTADISTICO):
        lost_estadistico = lost_estadistico + 1

#print (indice+","+str(len(indList))+","+str(dinero)+","+str((beneficio)/3000)+","+str((beneficio))+","+str((beneficio)/len(indList))+","+str(lost_estadistico)+","+str(win_estadistico)+","+str(salidas_bollinger))


