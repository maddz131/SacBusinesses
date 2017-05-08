import click
import re
import numpy 
import random
import pandas as pd 
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_samples, silhouette_score
from scipy.spatial.distance import cdist, pdist

import collections
import matplotlib.pyplot as plt
#import pylab as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns


#Get rid of rows that don't have a Business Description (NaN)
#Do not want to do this for the ones we will put in the database. Do this in clustering
#df = df.dropna(subset = ['Business Description'])
    
@click.command()
@click.argument('filename')
@click.option('--clusters', default=10, help='Number of clusters')
@click.option('--sample', default=10, help='Number of samples to print')

def cluster(filename, clusters, sample):
    #Read the rows from CSV
    lines = numpy.array(list(readFromCSV(filename)))

    doc_feat = TfidfVectorizer().fit_transform(lines)
    #print(doc_feat.get_shape())
    km = KMeans(clusters).fit(doc_feat)

    elbow(lines)

    return

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
    
    return line


def readFromCSV(filename):
    data = pd.read_csv(filename)
    data = data.dropna(subset = ['Business Description'])
    doc = data['Business Description'].values
    for line in doc:
        yield cleanRow(line)

'''http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
    https://datascience.stackexchange.com/questions/6508/k-means-incoherent-behaviour-choosing-k-with-elbow-method-bic-variance-explain
'''
def siltest(lines):
    sizes = [10,20,30]
    s = []
    d = TfidfVectorizer().fit_transform(lines)
    for n_clusters in sizes:
        km = KMeans(n_clusters)
        km.fit(d)

        labels = km.labels_
        centroids = km.cluster_centers_

        s.append(silhouette_score(d, labels, metric='euclidean', sample_size=50))

    plt.plot(s)
    #plt.xlim(xmin=2)
    plt.ylabel("Silouette")
    plt.xlabel("k")
    plt.title("Silouette for K-means")
    sns.despine()
    plt.show()


def elbow(lines):
    K = range(1,3)
    dt_trans = TfidfVectorizer().fit_transform(lines)
    
    KM = [KMeans(n_clusters=k).fit(dt_trans) for k in K]
    centroids = [k.cluster_centers_ for k in KM]

    D_k = [cdist(dt_trans.toarray(), cent) for cent in centroids]
    cIdx = [np.argmin(D,axis=1) for D in D_k]
    dist = [np.min(D,axis=1) for D in D_k]
    avgWithinSS = [sum(d)/dt_trans.shape[0] for d in dist]

    # Total with-in sum of square
    wcss = [sum(d**2) for d in dist]
    tss = sum(pdist(dt_trans.toarray())**2)/dt_trans.shape[0]
    bss = tss-wcss

    kIdx = 10-1

    # elbow curve
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(K, avgWithinSS, 'b*-')
    ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
    markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(K, bss/tss*100, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Percentage of variance explained')
    plt.title('Elbow for KMeans clustering')
    plt.show()

if __name__ == '__main__':
    cluster()