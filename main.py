import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans2
from argparse import ArgumentParser
import sys

class DataClustering:

    def __init__(self, _PATH_):
        self._PATH_ = _PATH_

    def _load_data(self):
        dataset = pd.read_csv(self._PATH_, sep=';', header=None)
        dataset = pd.read_csv(self._PATH_, sep = ';', header = None)
        dataset = dataset.applymap(lambda x: str(x.replace(',','.'))) #comma to dots
        dataset = dataset.astype('float32') #str to float
        self.dataset = dataset
        return dataset.to_numpy() #vectorize

    def scale(self, arr):
        if not isinstance(arr, (np.ndarray, np.generic)):
            arr = arr.to_numpy()
        min_list = []
        max_list = []
        arr_normalized = np.zeros(shape = arr.shape)
        for i in range(arr.shape[0]):
            min_list.append(np.min(arr[i, :]))
            max_list.append(np.max(arr[i, :]))
            arr_normalized[i, :] = (arr[i, :] - np.min(arr[i, :])) / (np.max(arr[i, :]) - np.min(arr[i, :])) #MqxMinScaling


        return min_list, max_list, arr_normalized

    def kmeans_cluster(self, scaled_matrix, k):
        #KMeans
        #if scaled_matrix.ndim == 2:
         #   scaled_matrix=np.squeeze(scaled_matrix, axis=1)
        centroid, label = kmeans2(scaled_matrix, k, minit='points')
        self.label = label
        print('labels are {}'.format(label))
        return label

    def add_labels_to_DS(self):### ADD LABELS TO THE TABLE ###
        self.dataset['label'] = np.asarray(self.label)
        return print('the labels were successfully added :)')

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

    def save_new_dataframe(self, filename):

        self.dataset.to_csv(filename)
        return print('the file is successfully saved in {}'.format(filename))

if __name__ == '__main__':
    ### LOAD DATA ###
    _PATH_ = 'Work table.csv'
    cls = DataClustering(_PATH_)
    DS = cls._load_data()
    min_list, max_list, arr_normalized = cls.scale(DS)

    k = int(sys.argv[1])
    cls.kmeans_cluster(arr_normalized, k)
    cls.add_labels_to_DS()

    _SAVE_PATH_= sys.argv[2]
    cls.save_new_dataframe(_SAVE_PATH_)


