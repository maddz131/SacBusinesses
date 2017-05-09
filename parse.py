#!/usr/bin/env python
""" parse.py: Takes CSV, preprocesses (data reduction and data cleaning) the data, 
    exports to CSV, then inserts the data in the mongo database.
"""

import pandas as pd
import os

def main():
    os.system('clear')
    print("Starting parse.py ...")

    #File of the CSV
    csvFilename = "/Users/kenkoyanagi/Projects/SacBusinesses/realdata.csv"
    cleanCSV(csvFilename)

    #Import the data in the mongodb
    mongoImport("output.csv", "sacbusinesses", "test4")

def cleanCSV(csvFile):
    #Only relevant fields should be read from the CSV
    fields = ["Account Number", "Business Name", "Business Description", "Application Date", "Business Start Date", "Business Close Date", "Current License Status", "Location City", "Location Zip code"]
    df = pd.read_csv(csvFile, skipinitialspace=True, usecols=fields)

    #We only want the businesses that are in Sacramento
    df = df[df['Location City'] == "SACRAMENTO"]

    #Replace 'A/C' with AC
    df['Business Description'] = df['Business Description'].str.replace('A/C', 'AC')

    #Need to strip Business Description of special characters and numbers. Strip leading and trailing spaces. 
    #All uppercase characters.
    df['Business Description'] = df['Business Description'].str.replace('[^a-zA-Z]', ' ').str.strip().str.upper()

    #Remove stopwords and special (whole) words from the column.
    stop = [r'\bA\b', r'\bAND\b', r'\bFOR\b', r'\bTHE\b', r'\bOF\b', r'\bSERVICES\b', r'\bSERVICE\b']
    for word in stop: df['Business Description'] = df['Business Description'].str.replace(word, '')
    #Remove multiple spaces that may the result of removal of special characters. Also remove leading space.
    df['Business Description'] = df['Business Description'].replace('\s+', ' ', regex=True).str.lstrip(' ')

    #Snip extended zip codes to just five characters
    df['Location Zip code'] = df['Location Zip code'].map(lambda x: str(x)[:5])

    #ake the license status uppercase
    df['Current License Status'] = df['Current License Status'].str.upper()

    #Fix the formatting of the dates so R can recognize it as a valid date. 
    #Formatting it to YYYY/MM/DD
    df['Application Date'] = pd.to_datetime(df['Application Date'])
    df['Business Start Date'] = pd.to_datetime(df['Business Start Date'])
    df['Business Close Date'] = pd.to_datetime(df['Business Closec Date'])

    #Sort in ascending order by Business Description
    df.sort_values(['Business Description'], ascending=True, inplace=True)

    #Output the cleansed data to CSV
    df.to_csv("output.csv", index=False)

    #Check the datafield - for testing small amounts
    print(df)
    print("Clean Data to output.csv")

def mongoImport(fileName, database, collection):
    command = "mongoimport -d " + database  + " -c " + collection + " --type csv --file " + fileName + " --headerline"
    os.system(command)
    print("Imported into Mongo DB = [%s]; Collection = [%s] " % (database, collection))

if __name__ == '__main__':
    main()











