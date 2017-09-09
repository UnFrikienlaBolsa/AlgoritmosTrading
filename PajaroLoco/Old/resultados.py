#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 10:08:56 2017

@author: ruben
"""

import pandas as pd

df = pd.read_csv('./salida.out')

df['Dinero'].mean()
df['Rent'].mean()


df['Benef'].sum()/df['Ops'].sum()

float(df['Ops'].sum())/(365*2)
