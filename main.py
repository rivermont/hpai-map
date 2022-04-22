#!/usr/bin/env python3

import requests
import csv
import json


def clean(geo, btype, data):
    '''Strips geojson input of unneeded properties and adds new properties looked up in data.'''
    out = {"type": "Feature", "geometry": geo["geometry"], "name": geo["properties"]["NAMELSAD"], "properties": {
           "STATE_NAME": geo["properties"]["STATE_NAME"],
           "NAME": geo["properties"]["NAME"]
    }}
    
    out['properties']['description'] = data[out['properties']['STATE_NAME']]['counties'][out['properties']['NAME']]['description']
    out['properties']['num_report_' + btype] = data[out['properties']['STATE_NAME']]['counties'][out['properties']['NAME']]['num_report_' + btype]
    if btype == 'cap':
        out['properties']['num_birds_' + btype] = data[out['properties']['STATE_NAME']]['counties'][out['properties']['NAME']]['num_birds_' + btype]
    
    return out


## DOWNLOAD FROM USDA ##

overwrite = False  # for overwriting data files

if overwrite:
    # get data from usda csvs
    commercial = requests.get("https://www.aphis.usda.gov/animal_health/data-csv/hpai-commercial-backyard-flocks.csv").text
    wild = requests.get("https://www.aphis.usda.gov/animal_health/data-csv/hpai-wild-birds.csv").text

    # check whether files exist
    # save files
    with open("./data/hpai-commercial-backyard-flocks.csv", "w+") as f:
        f.write(commercial)

    with open("./data/hpai-wild-birds.csv", "w+") as f:
        f.write(wild)


## PROCESS COMMERCIAL FLOCK DATA ##

data = {}

with open("./data/hpai-commercial-backyard-flocks.csv", "r") as f:
    creader = csv.reader(f, delimiter=',', quotechar='"')
    header = next(creader)
    
    for row in creader:
        state = row[0]
        county = row[1]
        ftype = row[3]
        fsize = row[4]
        
        if state not in data:
            data[state] = {'counties': {}, 'num_birds_cap': 0, 'num_report_cap': 0}
        
        if county not in data[state]['counties']:
            data[state]['counties'][county] = {'description': '', 'num_birds_cap': 0, 'num_report_cap': 0}
        
        data[state]['counties'][county]['description'] += ftype + ': ' + fsize + '<br>'
        data[state]['counties'][county]['num_birds_cap'] += int(fsize.replace(',', ''))
        data[state]['counties'][county]['num_report_cap'] += 1
        data[state]['num_birds_cap'] += int(fsize.replace(',', ''))  # can also automate this at the end
        data[state]['num_report_cap'] += 1



# create set of (state, county) pairs
x = set()
for s in data:
    for c in data[s]['counties']:
        x.add((s, c))
        # print(data[s]['counties'][c]['num_report_cap'])  # data for histogram


out = {"type": "FeatureCollection", "name": "HPAI Counties CAPTIVE", "features": [],
       "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4269"}}
       }  # geojson to export

with open("./data/cb_2020_us_county_20m.geojson", 'r') as f:
    counties = json.loads(f.read())
    for county in counties['features']:
        if (county['properties']['STATE_NAME'], county['properties']['NAME']) in x:
            x.remove((county['properties']['STATE_NAME'], county['properties']['NAME']))
            out['features'].append(clean(county, 'cap', data))
    print(x)  # TODO: fix these counties not being found

with open("./hpai_counties_cap.geojson", "a", encoding="utf-8") as f:
    json.dump(out, f)


## PROCESS WILD BIRD DATA ##

data = {}

with open("./data/hpai-wild-birds.csv", "r") as f:
    creader = csv.reader(f, delimiter=',', quotechar='"')
    header = next(creader)
    
    for row in creader:
        state = row[0]
        county = row[1]
        date = row[2]
        ftype = row[4]
        
        if state not in data:
            data[state] = {'counties': {}, 'num_report_wild': 0}
        
        if county not in data[state]['counties']:
            data[state]['counties'][county] = {'description': '', 'num_report_wild': 0}
        
        data[state]['counties'][county]['description'] += date + ': ' + ftype + '<br>'
        data[state]['counties'][county]['num_report_wild'] += 1
        data[state]['num_report_wild'] += 1


# create set of (state, county) pairs
x = set()
for s in data:
    for c in data[s]['counties']:
        x.add((s, c))
        # print(data[s]['counties'][c]['num_report_wild'])  # data for histogram


out = {"type": "FeatureCollection", "name": "HPAI Counties WILD", "features": [],
       "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::4269"}}
       }  # geojson to export

with open("./data/cb_2020_us_county_20m.geojson", 'r') as f:
    counties = json.loads(f.read())
    for county in counties['features']:
        if (county['properties']['STATE_NAME'], county['properties']['NAME']) in x:
            x.remove((county['properties']['STATE_NAME'], county['properties']['NAME']))
            out['features'].append(clean(county, 'wild', data))
    print(x)  # TODO: fix these counties not being found

with open("./hpai_counties_wild.geojson", "a", encoding="utf-8") as f:
    json.dump(out, f)

