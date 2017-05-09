#!/usr/bin/env python
import pandas as pd
import os
import csv

def main():
    os.system('clear')
    print("Starting businesstrend.py ...")

    #File of the CSV
    csvFile = "/Users/kenkoyanagi/Projects/SacBusinesses/clusteredOutput.csv"
    
    fields = ["Business Start Date", "Business Close Date", "Good Cluster", "Cluster Label"]
    df = pd.read_csv(csvFile, skipinitialspace=True, usecols=fields)

    #take off days from the dates
    df['Business Start Date'] = df['Business Start Date'].map(lambda x: str(x)[:7])
    df['Business Close Date'] = df['Business Close Date'].map(lambda x: str(x)[:7])

    #sort by business start date
    df.sort_values(['Business Start Date'], ascending=True, inplace=True)

    monthly = {}

    #This is for all businesses, regardless of in good category or not, OVERALL!
    #iterate through rows
    for index, row in df.iterrows():
        if row['Business Start Date'] is not "":
            if row['Business Start Date'] in monthly:
                monthly[row['Business Start Date']] += 1
            else:
                monthly[row['Business Start Date']] = 1
        if row['Business Close Date'] is not "":
            if row['Business Close Date'] in monthly: 
                monthly[row['Business Close Date']] -= 1
            else:
                monthly[row['Business Close Date']] = -1

    #output dict to csv
    f = open( 'businesstrend.csv', 'w' )
    for key in monthly.keys():
        f.write(str(key) + " , " + str(monthly[key]) + "\n");

    #############################################################################
    #Change df to only include the good clusters
    df = df[df['Good Cluster'] == "GOOD"]

    #Get the trends for each good cluster label
    labels = []
    labels = df['Cluster Label'].unique()
    print("Good cluster labels are: " % labels)

    for label in labels:
        subMonthly = {}
        sub = df[df['Cluster Label'] == label]

        for index, row in sub.iterrows():
            if row['Business Start Date'] is not "":
                if row['Business Start Date'] in subMonthly:
                    subMonthly[row['Business Start Date']] += 1
                else:
                    subMonthly[row['Business Start Date']] = 1
            if row['Business Close Date'] is not "":
                if row['Business Close Date'] in subMonthly: 
                    subMonthly[row['Business Close Date']] -= 1
                else:
                    subMonthly[row['Business Close Date']] = -1

        fileName = "0Cluster_" + label + ".csv"
        fileName = fileName.replace("/", "-")
        
        f = open(fileName, 'w')
        for key in subMonthly.keys():
            f.write(str(key) + " , " + str(subMonthly[key]) + "\n");

if __name__ == '__main__':
    main()










