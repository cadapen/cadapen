#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 21:45:48 2021

@author: CADAPEN NEEVEN
"""

import os
import csv
from termcolor import colored, cprint
#os.chdir("C:\\users\\msellami\\PythonTraining\\")

import datetime
import json
import urllib.request
#Il faut specifier aussi les données sous forme JSON ou XML et l'unité de temperature (°C,F).
# Pour Fahrenheit, on utilise unité=imperial, pour Celsius, on utilise unité= metric, et par defaut Kelvin. 

def url_builder(city_id,city_name,country):
    user_api = '978ee10c1dee098294ccfa5041ab4a94'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    if(city_name!=""):
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' # "http://api.openweathermap.org/data/2.5/weather?q=Tunis,fr
        full_api_url = api + str(city_name) +','+ str(country)+ '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
   
    return full_api_url

#Maintenant on passe à definir une fonction qui permet de récuperer le fichier JSON a partir
# de cette URL en utilisant urllib.request.urlopen(), str.read.decode('utf-8') pour l'encodage et json.load() pour charger une structire SJON a partir des fichier
def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    print (data)
    return data

def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], m_symbol, data['sky'])
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('')
    #Il faut specifier aussi les données sous forme JSON ou XML et l'unité de temperature (°C,F). Pour Fahrenheit, on utilise unité=imperial, pour Celsius, on utilise unité= metric, et par defaut Kelvin. 
    print('Wind Speed: {}, Degree: {}'.format(data['wind'], data['wind_deg']))
    print('Humidity: {}'.format(data['humidity']))
    print('Cloud: {}'.format(data['cloudiness']))
    print('Pressure: {}'.format(data['pressure']))
    print('Sunrise at: {}'.format(data['sunrise']))
    print('Sunset at: {}'.format(data['sunset']))
    print('')
    print('Last update from the server: {}'.format(data['dt']))
    print('---------------------------------------')

def WriteCSV(data):
    #headerList = ['city','country','temp','temp_max','temp_min','humidity','pressure','sky','sunrise','sunset','wind','wind_deg','dt','cloudiness']
    with open('weatherOpenMap.csv', 'a+') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, data.keys())
 #       w.writeheader()
        w.writerow(data)
        
        
def  ReadCSV():
    try:
    #ouverture de fichier en mode lecture en specifiant le encodage
        with open("weatherOpenMap.csv",'r') as Fichier:
        #lecture – utilisation du parseur csv en specifiant délimiteur
            csv_contenu = csv.reader(Fichier,delimiter=",") 
            reader = csv.DictReader(Fichier)
            dic={}
            for row in reader:
                print (row['city'])
                dic.update(row)
            #fermeture du fichier avec la méthode close()
            Fichier.close()
            return dic
    except IOError:
        print("Fichier n'est pas trouvé")  
        
import pandas as pd
import json 
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening json in pandas df

#load json object

def getVilles():
    with open('city.list.json') as f:
        d = json.load(f)
        villes=pd.DataFrame(d)   
        return villes;
        
villes=getVilles()
villesdefrance = villes[villes["country"]=='FR']['id']     
sous_villesdefrance=villesdefrance.head(900)



if __name__ == '__main__':
    try:
        city_name=''
        country='FR'
        city_id='2464470'
        compteur=0
#        for uneville in villesdefrance:
        for uneville in sous_villesdefrance:    
            city_id=uneville
        #Generation de l url
            print(colored('Generation de l url ', 'red',attrs=['bold']))
            url=url_builder(city_id,city_name,country)
        
        #Invocation du API afin de recuperer les données
            print(colored('Invocation du API afin de recuperer les données', 'red',attrs=['bold']))
            data=data_fetch(url)
        #print(json.dumps(data, sort_keys=True, indent=2));
        #Formatage des données
            print(colored('Formatage des donnée', 'red',attrs=['bold']))
            data_orgnized=data_organizer(data)
        #Affichage de données
            print(colored('Affichage de données ', 'red',attrs=['bold']))
            data_output(data_orgnized)
        #Enregistrement des données à dans un fichier CSV 
            print(colored('Enregistrement des données à dans un fichier CSV ', 'green',attrs=['bold']))
            WriteCSV(data_orgnized)
        #WriteCassandra(data_orgnized)
            print(colored('Lecture des données à partir un fichier CSV ', 'green',attrs=['bold']))
            print(colored('Affichage des données lues de CSV ', 'green',attrs=['bold']))
            compteur=compteur+1
        print(compteur)
    except IOError:
        print('no internet')   
        



