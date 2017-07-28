#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:17:25 2017

@author: jorgemauricio
"""

#%% import libraries
import pandas as pd
import os

#%% Clear terminal
os.system('clear')

#%% chance workdirectory
os.chdir('/Users/jorgemauricio/Documents/Research/noRainyDaysIndex')

#%% load data from csv file
data = pd.read_csv('datos_diarios_precipitacion_1.csv')

#%% Display head of file
data.head()

#%% How many rows the dataset
data['number'].count()

#%% Drop NA values from the rows
data = data.dropna()

#%% How many rows the dataset after drop NA
data['number'].count()

#%% Create Fecha Format AAAA-MM
data['fechaFormato'] = data.apply(lambda x: '%d-%d' % (x['anio'], x['mes']), axis=1)

#%% column precipitacion to vReal
data['vReal'] = data['precipitacion']

#%% Create Rainy days column
data['rainyDays'] = [1 if x > 0.0 else 0 for x in data['vReal']]

#%% Create No rainy days column
data['noRainy'] = [1 if x == 0.0 else 0 for x in data['vReal']]

#%% grouped classification 0 - 5
data['0_5'] = [1 if x > 0.0 and x <= 5.0 else 0 for x in data['vReal']]

#%% grouped classification 5 - 10
data['5_10'] = [1 if x > 5.0 and x <= 10.0 else 0 for x in data['vReal']]

#%% grouped classification 10 - 15
data['10_15'] = [1 if x > 10.0 and x <= 15.0 else 0 for x in data['vReal']]

#%% grouped classification 15 - 20
data['15_20'] = [1 if x > 15.0 and x <= 20.0 else 0 for x in data['vReal']]

#%% grouped classification > 20
data['20_'] = [1 if x > 20.0 else 0 for x in data['vReal']]

#%% Aggregation
aggregations = {
        'vReal' : ['sum', 'min', 'max', 'median', 'mean', 'std'],
        'rainyDays' : ['sum'],
        'noRainy' : ['sum'],
        '0_5' : ['sum'],
        '5_10' : ['sum'],
        '10_15' : ['sum'],
        '15_20' : ['sum'],
        '20_' : ['sum']
        }

#%% Apply aggregation
data.groupby('fechaFormato').agg(aggregations)

#%% data head
data.head()

#%% Save to CSV
grouped = data.groupby(['lat', 'long','number','fechaFormato']).agg(aggregations)
grouped.columns = ["_".join(x) for x in grouped.columns.ravel()]
grouped.to_csv('baseTotalGroupedYearMonth.csv')

#%% grouped data head()
grouped.head()
