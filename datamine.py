#!/usr/bin/env python

import pandas as pd
import numpy as np 
import scipy.linalg as lin
import Levenshtein as leven
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
import itertools

fields = ["Business Description"]
df = pd.read_csv("data.csv", skipinitialspace=True, usecols=fields)

df = df["Business Description"].unique()
print(df)

pd.DataFrame(df, columns=['Business Description']).to_csv('uniquevalues.csv')

words = np.genfromtxt('uniquevalues.csv', delimiter=",")

(dim,) = words.shape

f = lambda x_y: -leven.distance(x_y[0],x_y[1])

res=np.fromiter(map(f, itertools.product(words, words)), dtype=np.uint8)
A = np.reshape(res,(dim,dim))

af = AffinityPropagation().fit(A)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

# Distances had to be converted to similarities, I did that by taking the negative of distance. The output is

unique_labels = set(labels)
for i in unique_labels:
    print(words[labels==i])