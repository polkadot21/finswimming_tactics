import pandas as pd
import numpy as np

from scipy.cluster.vq import kmeans2

from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

### LOAD DATA ###
_PATH_ = 'Work table.csv'
dataset = pd.read_csv(_PATH_, sep = ';', header = None)
dataset = dataset.applymap(lambda x: str(x.replace(',','.'))) #comma to dots
dataset = dataset.astype('float32') #str to float

## NORMALIZE DATA ###
dataset_matrix = dataset.to_numpy() #vectorize

def scale(arr):
    mean_list = []
    std_list = []
    arr_normalized = np.zeros(shape = arr.shape)
    for i in range(arr.shape[0]):
        mean_list.append(np.mean(arr[i, :]))
        std_list.append(np.std(arr[i, :], ddof = 1))
        arr_normalized[i, :]  = (arr[i, :] - mean_list[i]) / std_list[i]

    return mean_list, std_list, arr_normalized

mean_list, std_list, scaled_matrix = scale(dataset_matrix)

"""
### Agglomerarive Clustering
Z = hierarchy.linkage(scaled_matrix, 'single')
plt.figure()
dn = hierarchy.dendrogram(Z) # 6 categories
"""
print(mean_list)
print(scaled_matrix)

#KMeans
centroid, label = kmeans2(scaled_matrix, 3, minit='random')
print('labels are {}'.format(label))

### ADD LABELS TO THE TABLE ###
dataset['label'] = np.asarray(label)

def sort_elements(kmeans):
    zero = []
    first = []
    second = []
    third = []
    forth = []


    for element in kmeans.labels_:
        if element ==0:
            zero.append(element)
        elif element == 1:
            first.append(element)
        elif element == 2:
            second.append(element)
        elif element == 3:
            third.append(element)
        elif element == 4:
            forth.append(element)

    print('the number of class zero is {}'.format(len(zero)))
    print('the number of class one is {}'.format(len(first)))
    print('the number of class two is {}'.format(len(second)))
    print('the number of class three is {}'.format(len(third)))
    print('the number of class four is {}'.format(len(forth)))
    return

if __name__ == '__main__':
    filename = 'Work_table_with_lables.xlsx'
    dataset.to_excel(filename)
    #sort_elements(kmeans)
