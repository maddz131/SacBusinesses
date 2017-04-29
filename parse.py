
#!/usr/bin/env python
""" parse.py: Takes Windows CSV, preprocesses and cleans the data, exports to CSV
    then inserts the data in the mongo database 
"""

import pandas as pd
import os

def main():
    os.system('clear')
    print("Starting parse.py ...")

    #File of the CSV
    csvFilename = "/Users/kenkoyanagi/Projects/SacBusinesses/testCSV.csv"
    cleanCSV(csvFilename)

    #Import the data in the mongodb
    mongoImport("output.csv", "sacbusinesses", "test3")


def cleanCSV(csvFile):
    #Only relevant fields should be read from the CSV
    fields = ["Account Number", "Business Name", "Business Description", "Application Date", "Business Start Date", "Business Close Date", "Current License Status", "Location City", "Location Zip code"]
    df = pd.read_csv(csvFile, skipinitialspace=True, usecols=fields)

    #We only want the businesses that are in Sacramento
    df = df[df['Location City'] == "SACRAMENTO"]

    #Replace NaN for Business Description with "OTHER"
    df['Business Description'] = df['Business Description'].fillna(value="OTHER")
    #Need to strip Business Description of special characters
    df['Business Description'] = df['Business Description'].str.replace('\W+', ' ')

    #Snip extended zip codes to just five characters
    df['Location Zip code'] = df['Location Zip code'].map(lambda x: str(x)[:5])

    #Sort in ascending order by Business Description
    df.sort_values(['Business Description'], ascending=True, inplace=True)

    #Output the cleansed data to CSV
    df.to_csv("output.csv", index=False)

    #Check the datafield - for testing small amounts
    print(df)

def mongoImport(fileName, database, collection):
    command = "mongoimport -d " + database  + " -c " + collection + " --type csv --file " + fileName + " --headerline"
    os.system(command)

if __name__ == '__main__':
    main()











