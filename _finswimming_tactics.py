import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans2
from argparse import ArgumentParser
import sys
from tslearn.clustering import TimeSeriesKMeans, KShape


class FinswimmingTactics:

    def __init__(self, FILE_PATH: str):

        """
        FILE_PATH : str
            The path to an Excel file with a performance MxN matrix, where M is the number of athletes and N is the
            number of splits

        """
        self.df = None
        self.normalized_arr = None
        self.labels = None
        self.normalized_df = None

        self.FILE_PATH = FILE_PATH

    def _load_data(self):
        df = pd\
            .read_csv(self.FILE_PATH, sep = ';', header = None) \
            .applymap(lambda x: str(x.replace(',', '.')))\
            .astype('float32') #str to float

        self.df = df
        return df.to_numpy() #vectorize

    def min_max_scale(self, arr):

        """
        A custom implementation of MinMax scaling
        """

        if not isinstance(arr, (np.ndarray, np.generic)):
            arr = arr.to_numpy()
        min_list = []
        max_list = []
        arr_normalized = np.zeros(shape = arr.shape)
        for i in range(arr.shape[0]):
            min_list.append(np.min(arr[i, :]))
            max_list.append(np.max(arr[i, :]))
            arr_normalized[i, :] = (arr[i, :] - np.min(arr[i, :])) / (np.max(arr[i, :]) - np.min(arr[i, :])) #MqxMinScaling

        self.arr_normalized = arr_normalized
        return min_list, max_list, arr_normalized


    def kmeans_cluster_with_dtw(self,
                                scaled_matrix: np.array,
                                k: int,
                                metric:str = "dtw"):
        self.labels = TimeSeriesKMeans(n_clusters=k, metric=metric, max_iter=5,
                                       max_iter_barycenter = 5,
                                       random_state = 0).fit_predict(scaled_matrix)
        print('labels are {}'.format(self.labels))
        return self.labels

    def kshapes_cluster(self,
                scaled_matrix: np.array,
                k: int,
                ):
        self.labels = KShape(n_clusters=k, n_init=1, random_state=0
                             ).fit_predict(scaled_matrix)
        print('labels are {}'.format(self.labels))
        return self.labels

    def kmeans_cluster(self, scaled_matrix, k):
        #KMeans
        #if scaled_matrix.ndim == 2:
         #   scaled_matrix=np.squeeze(scaled_matrix, axis=1)
        centroid, self.labels = kmeans2(scaled_matrix, k, minit='points')
        print('labels are {}'.format(self.labels))
        return self.labels

    def add_labels_to_DS(self, normalized_values: bool = False):### ADD LABELS TO THE TABLE ###
        if normalized_values:
            normalized_df = pd.DataFrame(self.normalized_arr)
            normalized_df['label'] = np.asarray(self.labels)
            print(normalized_df)
            self.normalized_df = normalized_df
            print('the labels were successfully added to the normalized data :)')
            return self

        else:
            self.df['label'] = np.asarray(self.labels)
            print('the labels were successfully added :)')
            return self

    #TODO: customize this function for k clusters
    def sort_elements(self, kmeans):
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

    def save_new_dataframe(self, filename: str, normalized_values: bool = False):
        if not normalized_values:
            self.df.to_csv(filename)
            return print('the file is successfully saved in {}'.format(filename))
        else:
            self.normalized_df.to_csv(filename)
            return print('the file with normalized data is successfully saved in {}'.format(filename))

if __name__ == '__main__':
    ### LOAD DATA ###
    _PATH_ = 'Work table.csv'
    cls = FinswimmingTactics(_PATH_)
    DS = cls._load_data()
    min_list, max_list, arr_normalized = cls.min_max_scale(DS)

    #k = int(sys.argv[1])
    k = 3
    cls.kshapes_cluster(arr_normalized, k)
    cls.add_labels_to_DS(normalized_values=True)

    #_SAVE_PATH_= sys.argv[2]
    _SAVE_PATH_ = 'lol_kshape.csv'
    cls.save_new_dataframe(_SAVE_PATH_, normalized_values=True)

    means = [np.mean(cls.normalized_df[cls.normalized_df['label'] == i]) for i in range(0, 3)]

    #print(np.asarray(means[0][:-1]))
    """
    plt.figure(figsize = (16, 9 ))
    for i in range (0, 3):
        plt.plot(np.asarray(means[i][:-1]))
    plt.title('Три стратегии проплывания дистанции 200м плавание в ластах')
    plt.show()
    """


