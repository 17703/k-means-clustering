# K-means_clustering.py
# Song Li
# 11/15/2021

import pandas as pd
import math
from numpy.random import seed
from numpy.random import randint

# adjustable parameters
distance_threshold = 3
K = 2

def KMeansClustering(src_data):
    clusters = [] # list of lists
    outliers = []

    # initialize clusters
    for i in range(0, K):
        clusters.append([])

    # randomly specify K centroids limited to the points in src_data
    # seed(0) # seed random number generator
    rand_indexes = randint(0, len(src_data), K) # generate K random integers within range from 0 to len(src_data)-1

    # variables holding centroids' coordinates
    cen_x = []
    cen_y = []
    
    
    # get centroids' coordinates
    for i in range(0, K):
        cen_x.append(src_data['x'][rand_indexes[i]])
        cen_y.append(src_data['y'][rand_indexes[i]])
    
    
    # test with the example from assignment 2
    #
    # initial centroids: (2, 2), (6, 7)
    """
    cen_x.append(2)
    cen_x.append(6)
    cen_y.append(2)
    cen_y.append(7)

    cen_x.append(5)
    cen_y.append(3)
    """

    # variables holding redefined centroids' coordinates
    cen_x_new = []
    cen_y_new = []

    while cen_x_new != cen_x or cen_y_new != cen_y: # while centroids do not converge, stop when centroids converge/do not change
        for index, row in src_data.iterrows():
            captured = False
            for i in range(0, K):
                
                if Distance(row['x'], row['y'], cen_x[i], cen_y[i]) <= distance_threshold: # captured by a cluster
                    clusters[i].append((row['x'], row['y']))
                    captured = True
            if not captured: # is an outlier when not captured by any cluster
                outliers.append((row['x'], row['y']))

        # output current clustering assignment
        print("centroids: ")
        for i in range(0, K):
            print(f"({cen_x[i]}, {cen_y[i]})")

        print("clusters: ")
        for i in range(0, K):
            print(clusters[i])
        
        print("outliers: ")
        print(outliers, '\n')

        # redefine centroids
        cen_x_new.clear() #debug*#
        cen_y_new.clear()

        for i in range(0, K):
            cen_x_new.append(round(RedefineCentroids(clusters[i])[0], 2))
            cen_y_new.append(round(RedefineCentroids(clusters[i])[1], 2))

        # swap old and new centroids
        cen_x_new, cen_x = cen_x, cen_x_new
        cen_y_new, cen_y = cen_y, cen_y_new

        # clear clusters and outliers for the next iteration
        for i in range(0, K):
            clusters[i].clear()

        outliers.clear()

    return

def Distance(x, y, centroid_x, centroid_y):
    return math.sqrt(((y - centroid_y) ** 2) + ((x - centroid_x) ** 2))

def RedefineCentroids(cluster):
    x_sum = 0
    y_sum = 0

    for point in cluster:
        x_sum += point[0]
        y_sum += point[1]
    
    return x_sum/len(cluster), y_sum/len(cluster)

# main
if __name__ == '__main__':
    src_data = pd.read_csv('k_means_clustering_source_file.csv')

    print(f"distance_threshold = {distance_threshold}")
    print(f"K = {K}")
    print("initial centroids: ", end = '')
    print("(2, 2), (6, 7)", '\n')

    KMeansClustering(src_data)