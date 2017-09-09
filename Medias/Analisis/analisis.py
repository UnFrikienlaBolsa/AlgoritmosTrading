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

ops = df['Ops'].sum()

benef = df['Benef'].sum()

num_indices = len(df['Ind'].values)

salidas_win = df['SalidaWin'].sum()

salidas_lost = df['SalidaLost'].sum()

print ('Beneficio: ' + str(benef))
print ('Beneficio / Ops: ' + str(benef/ops))
print ('Total Ops: ' + str(ops))
print ('Ops / Indice: ' + str(ops/num_indices))
print ('Max Ops: ' + str(df['Ops'].max()))
print ('Win / Ops (%): ' + str((salidas_win*100/ops)))
print ('Lost / Ops (%): ' + str((salidas_lost*100/ops)))
