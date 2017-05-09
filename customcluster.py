import click
import re
import numpy 
import random
import pandas as pd 
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import collections
import os

#50 clusters seem to be near a sweet spot
    
@click.command()
@click.argument('filename')
@click.option('--clusters', default=10, help='Number of clusters')
@click.option('--sample', default=10, help='Number of samples to print')

def cluster(filename, clusters, sample):
    
    #Read the rows from CSV
    df = pd.read_csv(filename)
    df = df.dropna(subset = ['Business Description'])
    doc = df['Business Description'].values

    #rows of businessdescriptions to use
    lines = numpy.array(doc)

    #vectorize words 
    doc_feat = TfidfVectorizer().fit_transform(lines)

    #kmeans
    km = KMeans(clusters)
    km.fit(doc_feat)

    k = 0
    clusters = defaultdict(list)
    for i in km.labels_:
      clusters[i].append(lines[k])
      k += 1

    s_clusters = sorted(clusters.values(), key=lambda l: -len(l))

    #columns to add
    goodCluster = {}
    clusterDescription = {}
    representationPer = {}
    clusterLabel = {}

    clusterMapping = {}

    for idx, cluster in enumerate(s_clusters):

        s =  'Cluster [%s] and Cluster #%d:' % (len(cluster), idx)
        print(s)

        words = []
        for line in cluster:
            #Creating a mapping dictionary from description to cluster number
            if line not in clusterMapping:
                clusterMapping[line] = idx;

            #work on the words
            word = line.split(" ")
            for w in word:
                if w != "":
                    words.append(w)
            
        counter = collections.Counter(words)

        #Care only about the good clusters if they have 90% representation
        representation = 0
        for i,j in counter.most_common(1):
            representation = j
        representation = j * 1.00 / len(cluster)
        if (representation) > .9 and len(cluster) > 20:
            print("Good cluster with %f representation" % representation)
            print(counter.most_common(3))
            print("\n")
            goodCluster[idx] = "GOOD"
        else:
            print("Bad cluster with %f representation" % representation)
            print(counter.most_common(3))
            print("\n")
            goodCluster[idx] = "BAD"

        des = ""
        label = ""
        for x, y in counter.most_common(3):
            percentage = y * 1.00 / len(cluster) 
            if percentage > .5 :
                des += str(x)
                des += " ("
                des += str(percentage)
                des += ")  "
                label += str(x)
                label += "/"
        label = label[:-1]
        clusterDescription[idx] = des
        representationPer[idx] = representation
        clusterLabel[idx] = label

    #Create a new column named 'Cluster' to show which cluster the row is in
    x = km.predict(doc_feat)
    print(x)
    df['Cluster'] = df["Business Description"].map(clusterMapping)

    #Map the dictionaries to the dataframe based on the cluster number
    df["Good Cluster"] = df["Cluster"].map(goodCluster)
    df["Representation"] = df["Cluster"].map(representationPer)
    df["Cluster Description"] = df["Cluster"].map(clusterDescription)
    df["Cluster Label"] = df["Cluster"].map(clusterLabel)

    #Order the rows by cluster 
    df.sort_values(['Cluster'], ascending=True, inplace=True)

    #Write dataframe to CSV
    df.to_csv("clusteredOutput.csv", index=False)

    #Put in mongo
    mongoImport("clusteredOutput.csv", "sacbusinesses", "clustered")


def mongoImport(fileName, database, collection):
    remove = "db." + collection + ".drop()"
    os.system(remove)
    command = "mongoimport -d " + database  + " -c " + collection + " --type csv --file " + fileName + " --headerline"
    #mongoimport -d sacbusinesses -c clustered --type csv --file clusteredOutput.csv --headerline
    os.system(command)
    print("Imported into Mongo DB = [%s]; Collection = [%s] " % (database, collection))

if __name__ == '__main__':
    cluster()