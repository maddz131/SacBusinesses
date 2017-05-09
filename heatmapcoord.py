#!/usr/bin/env python
""" heatmapcoord.py
"""

import pandas as pd
import os 
from geopy.geocoders import Nominatim

def main():
    os.system('clear')
    print("Starting parse.py ...")

    #File of the CSV
    csvFilename = "/Users/kenkoyanagi/Projects/SacBusinesses/output.csv"
    createCordinateFile(csvFilename)


def createCordinateFile(csvFile):
    #Only relevant fields should be read from the CSV
    fields = ["Business Start Date", "Business Close Date", "Current License Status", "Location Zip code"]
    df = pd.read_csv(csvFile, skipinitialspace=True, usecols=fields)

    #Take the first four digits of our date, which will give us just the year
    df['Business Start Date'] = df['Business Start Date'].map(lambda x: str(x)[:4])

    #Only businesses that started in 2017
    df = df[df['Business Start Date'] == '2017' ]

    #Change zip codes to integer 
    df = df[pd.notnull(df['Location Zip code'])]
    df['Location Zip code'] = df['Location Zip code'].astype(int)

    print(df['Location Zip code'].value_counts())
    counts = df['Location Zip code'].value_counts().to_dict()
    print("Counts:")
    print(counts)

    geolocator = Nominatim()

    #new google.maps.LatLng(37.786905, -122.440270),

    dataStr = "data: ["
    for key, value in counts.items():
        location = geolocator.geocode(key)
        if location is not None:
            longitude = location.longitude
            latitude = location.latitude
            
            for x in range(0,value):
                dataStr = dataStr + "new google.maps.LatLng(" + str(latitude) + ", " + str(longitude) + "),\n "
    dataStr = dataStr + "]"

    print(dataStr)

if __name__ == '__main__':
    main()











