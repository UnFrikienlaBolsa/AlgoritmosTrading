#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:07:21 2017

@author: ruben
"""

import numpy as np
import sys
import pandas as pd

df = pd.read_csv('salida.out', sep=',')

#df = df[df['RSI']>50]
#df = df[df['BajaLow']>0.040]

dias = df['Dias'].sum()

benef = df['Benef'].sum()

ops = len(df['Ind'].values)


print ('Beneficio: ' + str(benef))
print ('Beneficio / Ops: ' + str(benef/ops))
print ('Total Ops: ' + str(ops))
print ('Dias / Ops: ' + str(dias/ops))
