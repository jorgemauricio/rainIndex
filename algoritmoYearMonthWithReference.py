# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 09:04:48 2017

@author: jorge mauricio
"""

#%% libraries
import pandas as pd
import os
import numpy as np
import csv
import sys
import random
from time import gmtime, strftime
from os.path import expanduser

#%% Clear terminal
os.system('clear')

#%% chance workdirectory
home = expanduser("~")
home += "/Documents/Research/rainIndex"
os.chdir(home)

#%% functions
def processingFunction():
    # import reference
    print('Here goes the program')

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
        
#%% check reference data
if os.path.exists('../rawData'):
    print('Folder exist')
    if os.path.exists('../rawData/rawDataRainIndexReference.csv'):
        print('File exist')
        #processingFunction()
    else:
        print('File Doesnt exist')
else:
    print('Folder doesnt exist')

#%%
dataReference = pd.read_csv('../rawData/rawDataRainIndexReference.csv')

#%% check Columns
arrayOfColumnsFromReference = dataReference.columns

if (len(arrayOfColumnsFromReference) >= 6):
    print('Information at least is complete')
    print(arrayOfColumnsFromReference)
else:
    print('Incomplete information')
    
#%% Display head of file
dataReference.head()

#%% How many rows the dataset
dataReference['precipitacion'].count()
datosBruto = dataReference["precipitacion"].count()
print("***** Numero total de registros: {}".format(datosBruto))

#%% Drop NA values from the rows
dataReference = dataReference.dropna()

#%% How many rows the dataset after drop NA
dataReference['precipitacion'].count()
datosNetos = dataReference["precipitacion"].count()
print("***** Numero neto de registros: {}".format(datosNetos))

#%% Print % of data available
datosTotales = datosNetos / datosBruto * 100
print("***** % Datos disponibles: {}".format(datosTotales))

#%% Create Fecha Format AAAA-MM
dataReference['fechaFormato'] = dataReference.apply(lambda x: '%d-%d' % (x['anio'], x['mes']), axis=1)

#%% column precipitacion to vReal
dataReference['vReal'] = dataReference['precipitacion']

#%% Create Rainy days column
dataReference['rainyDays'] = [1 if x > 0.0 else 0 for x in dataReference['vReal']]

#%% Create No rainy days column
dataReference['noRainy'] = [1 if x == 0.0 else 0 for x in dataReference['vReal']]

#%% grouped classification 0 - 5
dataReference['0_5'] = [1 if x > 0.0 and x <= 5.0 else 0 for x in dataReference['vReal']]

#%% grouped classification 5 - 10
dataReference['5_10'] = [1 if x > 5.0 and x <= 10.0 else 0 for x in dataReference['vReal']]

#%% grouped classification 10 - 15
dataReference['10_15'] = [1 if x > 10.0 and x <= 15.0 else 0 for x in dataReference['vReal']]

#%% grouped classification 15 - 20
dataReference['15_20'] = [1 if x > 15.0 and x <= 20.0 else 0 for x in dataReference['vReal']]

#%% grouped classification > 20
dataReference['20_'] = [1 if x > 20.0 else 0 for x in dataReference['vReal']]

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
dataReference.groupby('fechaFormato').agg(aggregations)

#%% data head
dataReference.head()

#%% Save to CSV
grouped = dataReference.groupby(['lat', 'long','number','fechaFormato']).agg(aggregations)
grouped.columns = ["_".join(x) for x in grouped.columns.ravel()]
grouped.to_csv('result/baseTotalGroupedYearMonth.csv')

#%% grouped data head()
grouped.head()

#%% read csv 
newData = pd.read_csv("result/baseTotalGroupedYearMonth.csv")

#%% newData head()
newData.head()

#%% disaggregation functions
counterIterationsTotal = 0
# Dias en el mes
def daysInMonth(d):
	tempDate = d.split('-')
	year = int(tempDate[0])
	month = int(tempDate[1])
	if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
		num = 31
	elif month == 4 or month == 6 or month == 9 or month == 11:
		num = 30
	elif month == 2:
		if year % 4 == 0:
			num = 29
		else:
			num = 28
	return num, month, year

#%% Generacion de matriz aleatoria
def generateMatrixOccur(n, m , v, t):
	if v == 0:
		tempMatrix = np.zeros(n)
	elif v >= 1 and v <= 15:
		counterIterations = 0
		countT = t
		tempMatrix = np.zeros(n)
		for i in range(v):
			tempMatrix[np.random.randint(1,n)] = 1
		counterIterations += 1
		countT += 1
	elif v > 16 and v <= 29:
		counterIterations = 0
		statusProcess = True
		countT = t
		while statusProcess:
			tempMatrix = np.random.randint(2, size=n)
			if (np.sum(tempMatrix) == v):
				statusProcess = False
				print("P: {} I: {} IT: {}".format(m, counterIterations, countT))
				counterIterations = 0
			counterIterations += 1
		countT += 1
    elif v == 30:
        tempMatrix = np.ones(n)
    elif v == 31:
        tempMatrix = np.ones(n)
    else:
		print("Error")
	return tempMatrix

#%% Generacion de matriz de probabilidad de ocurrencia
def generateMatrixProbability(n):
	# Gamma
	shape, scale = 3.0, 2.0 ## mean and dispersion
	tempMatrix = np.random.gamma(shape, scale, n)
	return tempMatrix

#%% csv file structure
dataFile = "lat, long, number, year, month, day, value\n"

#%% loop the dataFrame
for index, row in newData.iterrows():
    #print(row)    
    latitude = row["lat"]
    longitude = row["long"]
    prec = float(row["vReal_sum"])
    numOfDays, month, year = daysInMonth(row["fechaFormato"])
    matrizOcurrencia = generateMatrixOccur(numOfDays, month, row["rainyDays_sum"], counterIterationsTotal)
    matrizProbabilidad = generateMatrixProbability(numOfDays)
    matrizResultado = matrizOcurrencia * matrizProbabilidad
    valorTotalMatrizResultado = matrizResultado.sum()
    matrizResultado2 = matrizResultado / valorTotalMatrizResultado
    matrizResultado2 = matrizResultado2 * prec
    days = np.linspace(1,numOfDays, num=numOfDays)
    for y in days:
        dataFile = "{},{},{},{},{},{},{}\n".format(latitude, longitude, row["number"], year, month, y, matrizResultado2[int(y)-1])

#%% save to csv
textFile = open('result/dissagregationDataWithReference.csv', "w")
textFile.write(dataFile)
textFile.close()