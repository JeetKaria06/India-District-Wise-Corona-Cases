import requests
import json
from bs4 import BeautifulSoup
import time
import argparse
import pandas as pd
import csv

response = requests.get("https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/", timeout=(3.05, 27))
locationFinder = 'https://nominatim.openstreetmap.org/search?format=json&polygon=0&addressdetails=0&q='

soup = BeautifulSoup(response.text, 'lxml')

covidData = {}
dfcovid = pd.DataFrame({'state':[], 'district':[], 'situation':[], 'number':[]})

soup = soup.find_all('div', {'class':'skgm-states'})


# Generating CSV File

with open('district-wise-centroids.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile,quotechar=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['State', 'District', 'Latitude', 'Longitude'])
    for state in soup:
        
        stateData = state.find('div', {'class':'skgm-tr'}).text.strip().split(" ")
        stateNameList = stateData[:-4]
        stateName = ""
        for i in range(0, len(stateNameList)):
            stateName = stateName+stateNameList[i]+" "
        stateName = stateName.strip()
        covidData[stateName] = {}
        
        disData = state.find('div', {'class':'skgm-districts'}).find_all('div', {'class':'skgm-tr'})
        print("[INFO] "+stateName+" ...")
        
        for dist in disData:
            soloDist = dist.text.strip().split(" ")
            distList = soloDist[:-4]
            distName = ''
           
            for i in range(0, len(distList)):
                distName = distName + distList[i] + ' '
           
            distName = distName.strip()
            if distName=='Unknown' or distName=='Other State':
                locationData = requests.get(locationFinder+stateName+',India')
                spamwriter.writerow([stateName, 'Unknown', locationData.json()[0]['lat'], locationData.json()[0]['lon']])
                spamwriter.writerow([stateName, 'Other State', locationData.json()[0]['lat'], locationData.json()[0]['lon']])
            else:
                locationData = requests.get(locationFinder+distName+','+stateName+',India')
                spamwriter.writerow([stateName, distName, locationData.json()[0]['lat'], locationData.json()[0]['lon']])
            print(distName)
print("[INFO] Data generation Done...")
