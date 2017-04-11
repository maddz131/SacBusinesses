#set up paths and vars
csvfile = open('testcsv.csv','r')
jsonfile = open('results.json', 'w')

arr=[]
headers = []

# Read in the headers/first row
for header in csvfile.readline().split(','):
    headers.append(header)

# Extract the information into the "xx" : "yy" format.
for line in csvfile.readlines():  
  lineStr = ''
  for i,item in enumerate(line.split(',')):
    if i < 28:  #I skip the last two columns for my application
        lineStr+='"'+headers[i] +'" : "' + item + '",\n'
  arr.append(lineStr)

csvfile.close()

#convert the array into a JSON string:
jsn = '{\n "entries":['
jsnEnd = ']\n}'
for i in range(len(arr)-1):
    if i == len(arr)-2:
        jsn+="{"+str(arr[i])[:-2]+"}\n" #Get rid of the last comma if last entry
    else:
        jsn+="{"+str(arr[i])[:-2]+"},\n" #Get rid of the last comma
jsn+=jsnEnd

#write to file
jsonfile.write(jsn)
jsonfile.close()
print "Done."