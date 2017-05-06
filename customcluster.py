import click
import re
import numpy 
import random
import pandas as pd 
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import collections

@click.command()
@click.argument('filename')
@click.option('--clusters', default=10, help='Number of clusters')
@click.option('--sample', default=10, help='Number of samples to print')

def cluster_lines(filename, clusters, sample):
    #Read the rows from CSV
    lines = numpy.array(list(readFromCSV(filename)))

    doc_feat = TfidfVectorizer().fit_transform(lines)
    km = KMeans(clusters).fit(doc_feat)

    k = 0
    clusters = defaultdict(list)
    for i in km.labels_:
      clusters[i].append(lines[k])
      k += 1

    s_clusters = sorted(clusters.values(), key=lambda l: -len(l))

    f = open("clusters.txt", 'w')
    writelines =[]

    for cluster in s_clusters:

        s =  'Cluster [%s]:' % len(cluster)
        writelines.append(s)
        print(s)
    
        for line in cluster:
            writelines.append(line)
        writelines.append('--------')

        if len(cluster) > sample:
            out = random.sample(cluster, sample)
            #print(out)

        words = []
        for line in cluster:
            word = line.split(" ")
            for w in word:
                if w != "":
                    words.append(w)
            
        counter = collections.Counter(words)
        #print(counter.most_common(5))
        #print("\n")

        #Care only about the good clusters if they have 90% representation
        representation = 0
        for i,j in counter.most_common(1):
            representation = j
        representation = j * 1.00 / len(cluster)
        if (representation) > .9:
            print("Good cluster with %f representation" % representation)
            print(counter.most_common(3))
    
    for l in writelines:
        f.write("%s\n" % l)
    f.close()


def cleanRow(line):
    #Remove stop words
    stop = ['AND', 'OF', 'FOR', 'THE', 'A']
    querywords = line.split()
    resultwords = [word for word in querywords if word not in stop]
    line = ' '.join(resultwords)
    return line


def readFromCSV(filename):
    data = pd.read_csv(filename)
    data['Business Description']
    doc = data['Business Description'].values
    for line in doc:
        yield cleanRow(line)

if __name__ == '__main__':
    cluster_lines()