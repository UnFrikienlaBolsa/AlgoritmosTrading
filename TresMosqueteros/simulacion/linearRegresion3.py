#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 06:17:14 2017

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

# PARAMETROS
indice = sys.argv[1]
#indice = 'AENA'
#valorAjuste = -1*(150+15+5+0)
ganas = 0
total = 0 

# Cargamos Vectores
param = {
    'q': indice, # Stock symbol (ex: "AAPL")
    'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
    'x': "BME", # Stock exchange symbol on which stock is traded (ex: "NASD")
    'p': "2Y" # Period (Ex: "1Y" = 1 year)
}                
df = gfc.get_price_data(param)

for cuentaArray in range (155,155+80):
    valorAjuste = -1*(cuentaArray+15+5+0)
    
    valoresVol = df['High'].values
    valoresDiff = df['Volume'].values
    valoresCopiar = df['Close'].values
    fechasData = df.index.values
    
    # Ajustamos los valores
    valoresCopiar = valoresCopiar[valorAjuste:]
    valoresDiff = valoresDiff[valorAjuste:]
    valoresVol = valoresVol[valorAjuste:]
    fechasData = fechasData[valorAjuste:] 
    
    # Creamos los valores de DATA -> train
    longValores = 150
    X_train = []
    y_train = []
    for i in range(0,longValores):
        s = ''
        d = []
        for j in range(0,15):
          s = s + '' + str(valoresCopiar[i+j]) + ','
          d.append(valoresCopiar[i+j])
        for j in range(0,15):
          s = s + '' + str(valoresDiff[i+j]) + ','
          d.append(valoresDiff[i+j])
        for j in range(0,15):
          s = s + '' + str(valoresVol[i+j]) + ','
          d.append(valoresVol[i+j])
        maxValores = max(valoresCopiar[i+14+ 5:i+ 5+14+5])
        #s = s + calculaClase2(maxValores,valoresCopiar[i+j])
        s = s + str(maxValores)
        #d.append(maxValores)
        X_train.append(d)
        y_train.append(maxValores)
    
    # Escribimos los valores de TEST
    longValoresTest = 5
    s = ''
    X_test = []
    y_test = []
    for i in range(longValores+1, longValores + longValoresTest+1):
        s = ''
        d = []
        for j in range(0,15):
          s = s + '' + str(valoresCopiar[i+j]) + ','
          d.append(valoresCopiar[i+j])
          cierreEvaluar = valoresCopiar[i+j]
          fechaEvaluar = str(fechasData[i+j])
        for j in range(0,15):
          s = s + '' + str(valoresDiff[i+j]) + ','
          d.append(valoresDiff[i+j])
        for j in range(0,15):
          s = s + '' + str(valoresVol[i+j]) + ','
          d.append(valoresVol[i+j])
        #maxValores = max(valoresCopiar[longValores:i+j]) # Esta cambia porque no debemos tener los valores
        #maxValores = max(valoresCopiar[i+j:i+j+5])
        maxValores = max(valoresCopiar[i+14+ longValoresTest:i+ longValoresTest+14+5])
        #s = s + str(150)
        #d.append(150)
        X_test.append(d)
        y_test.append(maxValores)
    
    # Entrenamos
    regr = RandomForestRegressor();
    regr.fit(X_train, y_train)
    y_pred = regr.predict(X_test)

    regr2 = SVR(kernel='rbf', C=1e3, gamma=0.1)
    regr2.fit(X_train, y_train)
    y_pred2 = regr2.predict(X_test)

    regr3 = linear_model.LinearRegression()
    regr3.fit(X_train, y_train)
    y_pred3 = regr3.predict(X_test)

    # Votacion 
    # Si todos OK => Se invierte
    votacion = 0
    max_pred_array = [max(y_pred),max(y_pred2),max(y_pred3)]
    for i_voto in max_pred_array:
        ganancia_pred = (i_voto-cierreEvaluar)/cierreEvaluar
        if (ganancia_pred > 0.11):
            votacion = votacion + 1
    
    #max_pred = (max(y_pred)+max(y_pred2)+max(y_pred3))/3
    #max_test = max(y_test)
    #ganancia_pred = (max_pred-cierreEvaluar)/cierreEvaluar
    if (votacion > 2):
        #print ('-----------> CUENTA ARRAY: ' + str(cuentaArray))
        #print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
        #print("Mean absoluted error: %.2f" % mean_absolute_error(y_test, y_pred))
        # Explained variance score: 1 is perfect prediction
        #print('Variance score: %.2f' % r2_score(y_test, y_pred))
        
        #print ('% Error en Valor -> '+ str(mean_absolute_error(y_test, y_pred)/((max(valoresCopiar[-10:])+min(valoresCopiar[-10:]))/2)))
        #print ('Cierre Evaluar -> ' + str(cierreEvaluar))
        #print ('% Ganacia Predict -> ' + str(ganancia_pred))
        #print ('% Ganacia Real -> ' + str((max_test-cierreEvaluar)/cierreEvaluar))
        max_test = max(y_test)
        #print ((((max_test-cierreEvaluar)/cierreEvaluar)))
        if ((((max_test-cierreEvaluar)/cierreEvaluar))>0.035):
            print ('GANAS|'+indice+'|'+fechaEvaluar+'|'+str(cierreEvaluar)+'|0')
            ganas = ganas + 1
        else:
            print ('PIERD|'+indice+'|'+fechaEvaluar+'|'+str(cierreEvaluar)+'|'+str(y_test[-1:][0]))
        total = total + 1

#if (total>0):
#    print ('FINAL',indice,ganas, total, str(ganas*100/total))
    
    
