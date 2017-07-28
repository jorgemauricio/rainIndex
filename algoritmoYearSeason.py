#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:56:59 2017

@author: jorgemauricio
"""
#%% import libraries
import pandas as pd
import os

#%% Function seasonOfNumber
def seasonOfNumber(mes):
    seasonSelected = ''
    if (mes == 3 or mes == 4 or mes == 5):
        seasonSelected = 'spring'
    elif (mes == 6 or mes == 7 or mes == 8):
        seasonSelected = 'summer'
    elif (mes == 9 or mes == 10 or mes == 11):
        seasonSelected = 'fall'
    elif (mes == 12 or mes == 1 or mes == 2):
        seasonSelected = 'winter'
    else:
        print('Error')
    return seasonSelected

#%% Clear terminal
os.system('clear')

#%% chance workdirectory
os.chdir('/Users/jorgemauricio/Documents/Research/rainIndex')

#%% load data from csv file
data = pd.read_csv('../rawData/rawDataRainIndexReference.csv')

#%% Display head of file
data.head()

#%% How many rows the dataset
data['number'].count()

#%% Drop NA values from the rows
data = data.dropna()

#%% How many rows the dataset after drop NA
data['number'].count()

#%% column precipitacion to vReal
data['vReal'] = data['precipitacion']

#%% create season column
data['season'] = 'season'

#%% data classification per season: spring, summer, fall, winter
data['season'] = data.apply(lambda x: seasonOfNumber(x['mes']), axis=1)

#%% Create Fecha Format anio-season
data['yearSeason'] = data.apply(lambda x: '%d-%s' % (x['anio'], x['season']), axis=1)

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
grouped = data.groupby(['lat', 'long','number','yearSeason']).agg(aggregations)

#%% Change Columns names
grouped.columns = ["_".join(x) for x in grouped.columns.ravel()]

#%% Save to CSV
grouped.to_csv('result/baseTotalGroupedYearSeason.csv')

#%% grouped head
grouped.head()
