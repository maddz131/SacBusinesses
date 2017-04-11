# SacBusinesses
Data warehousing and mining on Sacramento's businesses. 

Use SacBusinesses database
    and testcollections collection for testing purposes

1. The end of the CSV file has to end with '&' instead of '\n'
    - At the top of the column, from the first row, insert the ampersand and copy all the way to the alst row

2. Use load() to load the rawparse.js file in mongo
    EX: load("/Users/kenkoyanagi/Projects/SacBusinesses/rawparse.js")

3. Copy the contents of the .csv to a variable
    EX: csv = testcsv.csv

4. Return the results from the function to a variable
    EX: var result = csvtojson(csv)

5. Copy the contents to an output.json file

6. Import the documents in the collection using mongoimport in another console
    EX: mongoimport --db sacbusinesses --collection testcollection  --file  output.json --jsonArray

7. Check to see if the contents are in the collection
    EX: db.testcollection.find()

Tips: 
    http://jsonlint.com is a good resource to verify that the JSON array is valid