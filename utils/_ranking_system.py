from datetime import datetime
from typing import Optional

import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup

#pd.options.mode.chained_assignment = None  # default='warn'


def compute_scores(B: int, T: int) -> int:
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

    P = int(1000 * ((B / T) ** 3))
    return P


def scrape_wr(url: str = 'https://www.cmas.org/world-records'):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup.get_text()[33:1330])

def time_to_sec(time: datetime.time) -> int:
    return 60 * time.minute + time.second


class RankingSystem:

    def __init__(self, FILE_PATH: Optional[str] = None, df: Optional[pd.DataFrame] = None):

        """
        FILE_PATH : str
            The path to an Excel file with a performance MxN matrix, where M is the number of athletes and N is the
            number of columns. The performance column must be the last one or have the name "Results".

        """
        if isinstance(df, type(None)):
            self.df = None
        else:
            self.df = df
        if isinstance(FILE_PATH, type(None)):
            self.FILE_PATH = None
        else:
            self.FILE_PATH=FILE_PATH

        self.performance_column = None
    """
    def _load_data(self):
        if not isinstance(self.FILE_PATH, type(None)):
            df = pd \
                .read_excel(self.FILE_PATH, sep=';', header=None) \
                .applymap(lambda x: str(x.replace(',', '.'))) \
                .astype('float32')  # str to float

            self.df = df
            return self
        else:
            print('the file path was not provided')
    """
    def _extract_performance(self):
        if isinstance(self.df, type(None)):
            self._load_data()
        if 'Results' in self.df.columns:
            performance_column = self.df['Results']
        elif 'Результат' in self.df.columns:
            performance_column = self.df['Результат']
        else:
            performance_column = self.df.columns[-1]

        self.performance_column = performance_column

        return self

    def _add_scores_column(self):
        if isinstance(self.performance_column, type(None)):
            self._extract_performance()
        self.df['Количество очков'] = self.performance_column

        return self

    def _compute_scores(self):
        self._add_scores_column()
        for idx, value in enumerate(self.df["Количество очков"]):
            self.df["Количество очков"].iloc[idx] = compute_scores(10, time_to_sec(value))
        return self

    def return_df_with_scores(self):
        self._compute_scores()
        return self.df


