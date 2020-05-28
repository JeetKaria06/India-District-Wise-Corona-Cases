import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import csv
import plotly.graph_objects as go
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-mode", "--mode", required=True, help="Set the Dark/Light Mode. 'dark' for Dark and 'light' for Light mode.")
args = vars(ap.parse_args())

if args['mode']!='dark' and args['mode']!='light':
    print("[ERROR] Invalid Mode")
    exit()
print("[INFO] Fetching Data...")
response = requests.get("https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/")

soup = BeautifulSoup(response.text, 'lxml')

covidData = {}
dfcovid = pd.DataFrame({'state':[], 'district':[], 'latitude':[], 'longitude':[], 'situation':[], 'number':[]})

soup = soup.find_all('div', {'class':'skgm-states'})
print()
for state in soup:
    stateData = state.find('div', {'class':'skgm-tr'}).find_all('div', {'class':'skgm-td'})
    stateName = stateData[0].text.strip()
    covidData[stateName] = {}

    disData = state.find('div', {'class':'skgm-districts'}).find_all('div', {'class':'skgm-tr'})
    print("[INFO] "+stateName+" ...")
    for dist in disData:
        distInfo = dist.find_all('div', {'class':'skgm-td'})
        distName = distInfo[0].text.strip()
        cured = distInfo[2].text.strip()
        active = distInfo[3].text.strip()
        deaths = distInfo[4].text.strip()
        if int(active)<0:
            active=0
        if int(cured)<0:
            cured=0
        if int(deaths)<0:
            deaths=0

        covidData[stateName][distName] = {}
        covidData[stateName][distName]['cured'] =  cured
        covidData[stateName][distName]['deaths'] = deaths
        covidData[stateName][distName]['active'] = active

        csv_file = csv.reader(open('district-wise-centroids.csv'), delimiter=',')

        # distInfo = []
        for row in csv_file:
            if row[0] == stateName and row[1] == distName:
                distLoc = row
        # print(distName)
        dfcovid = dfcovid.append({'state':stateName, 'district':distName, 'latitude':float(distLoc[2]), 'longitude':float(distLoc[3]), 'situation':'cured', 'number':int(cured)}, ignore_index=True)
        dfcovid = dfcovid.append({'state':stateName, 'district':distName, 'latitude':float(distLoc[2]), 'longitude':float(distLoc[3]), 'situation':'deaths', 'number':int(deaths)}, ignore_index=True)
        dfcovid = dfcovid.append({'state':stateName, 'district':distName, 'latitude':float(distLoc[2]), 'longitude':float(distLoc[3]), 'situation':'active', 'number':int(active)}, ignore_index=True)

print()
print("[INFO] Loading Map... ")
dfactive = dfcovid.query("situation=='active'")
dfcured = dfcovid.query("situation=='cured'")
dfdeath = dfcovid.query("situation=='deaths'")
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]

fig = go.Figure(go.Scattermapbox(
        lat=dfactive['latitude'],
        lon=dfactive['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=12,
            color=colors[1],
            opacity=0.7
        ),
        name='Active Case',
        text=dfactive['state']+"<br>"+dfactive['district']+"<br>"+dfactive['situation']+" "+list(map(str,dfactive['number'])),
        hoverinfo='text'
    ))

fig.add_trace(go.Scattermapbox(
    lat=dfcured['latitude'],
    lon=dfcured['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=13,
        color=colors[0],
        opacity=0.7
    ),
     name='Cured Case',
     text=dfcured['state']+"<br>"+dfcured['district']+"<br>"+dfcured['situation']+" "+list(map(str,dfcured['number'])),
     hoverinfo='text'
))

fig.add_trace(go.Scattermapbox(
    lat=dfdeath['latitude'],
    lon=dfdeath['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=14,
        color=colors[3],
        opacity=0.7
    ),
    name='Death Case',
     text=dfdeath['state']+"<br>"+dfdeath['district']+"<br>"+dfdeath['situation']+" "+list(map(str,dfdeath['number'])),
     hoverinfo='text'
))

fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=open('public_access_token.txt', 'r').read(),
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=20.5937,
            lon=78.9629
        ),
        pitch=0,
        zoom=5,
        style=args['mode']
    ),
    autosize=True,
    title="India's Districtwise Corona Cases<br>"+"<a href='https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/'>Source</a>"
)

fig.show()
