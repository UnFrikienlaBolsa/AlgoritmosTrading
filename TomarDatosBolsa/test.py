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
    'p': "5d" # Period (Ex: "1Y" = 1 year)
}                
df = gfc.get_price_data(param)

print('----------------------------------------------------')
print(indice)
print(df)
print('----------------------------------------------------')
