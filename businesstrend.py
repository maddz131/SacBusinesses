#!/usr/bin/env python
import pandas as pd
import os

def main():
    os.system('clear')
    print("Starting businesstrend.py ...")

    #File of the CSV
    csvFile = "/Users/kenkoyanagi/Projects/SacBusinesses/clusteredOutput.csv"
    
    fields = ["Business Start Date", "Business Close Date"]
    df = pd.read_csv(csvFile, skipinitialspace=True, usecols=fields)

    #take off days from the dates
    df['Business Start Date'] = df['Business Start Date'].map(lambda x: str(x)[:7])
    df['Business Close Date'] = df['Business Close Date'].map(lambda x: str(x)[:7])

    #sort by business start date
    df.sort_values(['Business Start Date'], ascending=True, inplace=True)

    monthly = {}

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

if __name__ == '__main__':
    main()










