#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 08:43:53 2017

@author: ruben
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


#indice = sys.argv[1]
indice = 'CABK'
df = pd.read_pickle('./data/'+indice+'2Y')

# PARAMETROS
POR_CAIDA = 0.07
POR_WIN = 0.05

# Buscamos tres caidas consecutivas
ant = -1000000
antant = -100000
   
# Buscamos tres caidas consecutivas
fechas = df.index.tolist()
close = df['Close'].values
indList = []
for i in range(0,len(close)):
   c = close[i]
   caida = (antant-c)/antant
   if (((ant > c) and (antant > ant)) and (caida > POR_CAIDA)):
       #print (i,fechas[i],c,ant,antant,caida)
       indList.append(i)
   antant = ant
   ant = c

dinero = 3000
for ind in indList:
    ap = ind
    compro = close[ap]
    close[ap+1:ap+6]
    maximo = max(close[ap+1:ap+6])
    if (((maximo-compro)/compro)>POR_WIN):
        rentabilidad = 1 + POR_WIN
    else:
        rentabilidad = (1+(close[ap+6]-compro)/compro)
    dinero = dinero * (rentabilidad)
    dinero = dinero - 16
    print (dinero, rentabilidad,((maximo-compro)/compro))    

print (indice+","+str(len(indList))+","+str(dinero)+","+str((dinero-3000)/3000)+","+str((dinero-3000)))

