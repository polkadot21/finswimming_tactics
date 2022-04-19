import pandas as pd
import numpy as np
from urllib.request import urlopen

def compute_scores(B: int, T:int) -> int:
    """
    the score is calculated as a cubic curve
    B : int
        The best time (WR approved by CMAS) on the 31th December of the previous years
    T : int
        The current time

    -----------------------
    P : int
        The computed score

    """

    P = int(1000*((B/T)**3))
    return P

def scrape_wr(url: str = 'https://www.cmas.org/world-records'):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    records_ = html.find("records_table")
    print(records_)

class RankingSystem:

    def __init__(self, FILE_PATH: str):

        """
        FILE_PATH : str
            The path to an Excel file with a performance MxN matrix, where M is the number of athletes and N is the
            number of columns. The performance column must be the last one or have the name "Results".

        """
        self.df = None
        self.FILE_PATH = FILE_PATH

    def _load_data(self):
        df = pd\
            .read_csv(self.FILE_PATH, sep = ';', header = None) \
            .applymap(lambda x: str(x.replace(',', '.')))\
            .astype('float32') #str to float

        self.df = df
        return self

    def _extract_performance(self):
        if isinstance(self.df, type(None)):
            self._load_data()
        if 'Results' in self.df.columns:
            performance_column = self.df['Results']
        elif 'Результаты' in self.df.columns:
            performance_column = self.df['Результаты']
        else:
            performance_column = self.df.columns[-1]

        return performance_column

if __name__ == '__main__':
    scrape_wr()


