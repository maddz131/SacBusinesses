
#!/usr/bin/env python
"""parse.py: Takes Windows CSV, cleans the data and exports as JSON"""

import json
import pandas as pd
import os

os.system('clear')
print("Starting parse.py")

#CSV needs for be formatted as a Windows CSV, should not be OSX CSV.
csvFilename = "/Users/kenkoyanagi/Projects/SacBusinesses/testCSV.csv"

#Only relevant fields should be read from the CSV
fields = ["Account Number", "Business Name", "Business Description", "Application Date", "Business Start Date", "Business Close Date", "Current License Status", "Location City", "Location Zip code"]
df = pd.read_csv(csvFilename, skipinitialspace=True, usecols=fields)

#We only want the businesses that are in Sacramento
df = df[df['Location City'] == "SACRAMENTO"]

#Replace NaN for Business Description with "OTHER"
df['Business Description'] = df['Business Description'].fillna(value="OTHER")

#Snip extended zip codes to just five characters
df['Location Zip code'] = df['Location Zip code'].map(lambda x: str(x)[:5])

#Output the cleansed data to CSV
df.to_csv("output.csv", index=False)


#Check the datafield - for testing small amounts
print(df)


