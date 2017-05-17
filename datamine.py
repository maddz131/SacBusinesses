#!/usr/bin/env python

import numpy as np
import sklearn.cluster
import distance
import pandas as pd 

data = pd.read_csv("output.csv")
data['Business Description']  # as a Series
words = data['Business Description'].values  # as a numpy array
#third column from CSV - Business Description

lev_similarity = -1 * np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])
affprop = sklearn.cluster.AffinityPropagation(affinity="euclidean", damping=0.5)
affprop.fit(lev_similarity)

for cluster_id in np.unique(affprop.labels_):
    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
    cluster_str = ", ".join(cluster)
    print(" - *%s:* %s\n" % (exemplar, cluster_str))

