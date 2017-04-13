//parses the csv from sacramento city to useful JSON
///Users/kenkoyanagi/Projects/SacBusinesses/testcsv.csv
//load("/Users/kenkoyanagi/Projects/SacBusinesses/rawparse.js")
function csvtojson(csv) {
    print("Starting Script");

    //split to single lines
    var lines = csv.split("&");                 //Wonder if '\r' is what we should split by instead of '\n'

    //create the array to hold the objects
    var result = [];

    //grab the header from the first line
    var headers = lines[0].split(",");

    for(var i = 1; i < lines.length; i++) {
        var currentline = lines[i].split(",");

        //CSV [ COLUMN NAME ]                   [ RELEVANT? ]
        //1.  Account Number                    - Keep
        //2.  Business Name                     - Keep
        //3.  Business Description              - Definitely Keep
        //4.  Application Date                  - Keep (Date)
        //5.  Business Start Date               - Keep (Date)
        //6.  Business Close Date               - Keep (Date)
        //7.  Current License Status            - License Cancelled / License Expired / ...
        //8.  Location Street Number            - Throw Away
        //9.  Location Direction                - Throw Away
        //10. Location Street Name              - Throw Away
        //11. Location Street Type              - Throw Away
        //12. Location Unit                     - Throw Away
        //13. Location City                     - Have to check to see if SACRAMENTO, then throw
        //14. Location State                    - Throw Away
        //15. Location Zip code                 - Keep (Only first 5 digits?)
        //16. Mail Street Number                - Throw Away
        //17. Mail Street Direction             - Throw Away
        //18. Mail Unit                         - Throw Away
        //19. Mail City                         - Throw Away
        //20. Mail State                        - Throw Away
        //21. Mail Zip code                     - Throw Away
        //22. Primary Phone Number              - Throw Away
        //23. Principal Owner First name        - Throw Away
        //24. Principal Owner Last Name         - Throw Away
        //25. BIA Area                          - Throw Away

        //First check if business is from Sacramento 
        if(currentline[12] == "SACRAMENTO"){
            var obj = {};

            obj["AccountNumber"] = (currentline[0]).substring(1);       //Account Number
            obj["BusinessName"] = currentline[1];                       //Business Name

            //if no description for the business, make it OTHER
            if(currentline[2] == ""){
                obj["Description"] = "OTHER"
            }
            else {
                obj["Description"] = currentline[2];
            }
            
            obj["ApplicationDate"] = currentline[3]; 
            obj["BusinessStartDate"] = currentline[4]; 
            obj["BusinessCloseDate"] = currentline[5]; 

            //Refer to Maddie's google docs for the different categories
            switch(currentline[6]) {
                case "":
                    //if no status, which should never happen, make it 99
                    obj["CurrentLicenseStatus"] = 99;
                    break;

                case "Application Active":
                    obj["CurrentLicenseStatus"] = 1;
                    break;
                
                case "Application Canceled":
                    obj["CurrentLicenseStatus"] = 2;
                    break;

                case "Application Pending":
                    obj["CurrentLicenseStatus"] = 3;
                    break;
                
                case "Application Rejected":
                    obj["CurrentLicenseStatus"] = 4;
                    break;

                case "License Canceled":
                    obj["CurrentLicenseStatus"] = 5;
                    break;

                case "License Expired":
                    obj["CurrentLicenseStatus"] = 6;
                    break;

                case "License Issued":
                    obj["CurrentLicenseStatus"] = 7;
                    break;

                case "License Renewed":
                    obj["CurrentLicenseStatus"] = 8;
                    break;

                case "Renewal Active":
                    obj["CurrentLicenseStatus"] = 9;
                    break;

                case "Renewal Canceled":
                    obj["CurrentLicenseStatus"] = 10;
                    break;

                case "Renewal Pending":
                    obj["CurrentLicenseStatus"] = 11;
                    break;

                case "Renewal Rejected":
                    obj["CurrentLicenseStatus"] = 12;
                    break;
            }


            //Only the first 5 digits of zip are relevant for us
            obj["Zip"] = (currentline[14]).substring(0,5);

            result.push(obj);
        }     
    }
    return JSON.stringify(result);
}