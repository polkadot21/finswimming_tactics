from urllib.request import urlopen
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from tabula.io import read_pdf


def english_events_to_russian(value: str) -> str:
    return {
        'SURFACE 50 MEN/HOMMES': 'плавание в ластах - 50 м, мужчины',
        'SURFACE 100 MEN/HOMMES': 'плавание в ластах - 100 м, мужчины',
        'SURFACE 200 MEN/HOMMES': 'плавание в ластах - 200 м, мужчины',
        'SURFACE 400 MEN/HOMMES': 'плавание в ластах - 400 м, мужчины',
        'SURFACE 800 MEN/HOMMES': 'плавание в ластах - 800 м, мужчины',
        'SURFACE 1500 MEN/HOMMES': 'плавание в ластах - 1500 м, мужчины',
        'IMMERSION 50 MEN/HOMMES': 'ныряние в ластах - 50 м, мужчины',
        'IMMERSION 100 MEN/HOMMES': 'ныряние в ластах - 100 м, мужчины',
        'IMMERSION 400 MEN/HOMMES': 'ныряние в ластах - 400 м, мужчины',
        'IMMERSION 800 MEN/HOMMES': 'ныряние в ластах - 800 м, мужчины',
        'BI 50 MEN/HOMMES': 'плавание в классических ластах - 50 м, мужчины',
        'BI 100 MEN/HOMMES': 'плавание в классических ластах - 100 м, мужчины',
        'BI 200 MEN/HOMMES': 'плавание в классических ластах - 200 м, мужчины',
        'BI 400 MEN/HOMMES': 'плавание в классических ластах - 400 м, мужчины',
        "RELAY 4 MEN/HOMMES": 'эстафетное плавание 4х100 м, мужчины',
        'SURFACE 50 WOMEN/DAMES': 'плавание в ластах - 50 м, женщины',
        'SURFACE 100 WOMEN/DAMES': 'плавание в ластах - 100 м, женщины',
        'SURFACE 200 WOMEN/DAMES': 'плавание в ластах - 200 м, женщины',
        'SURFACE 400 WOMEN/DAMES': 'плавание в ластах - 400 м, женщины',
        'SURFACE 800 WOMEN/DAMES': 'плавание в ластах - 800 м, женщины',
        'SURFACE 1500 WOMEN/DAMES': 'плавание в ластах - 1500 м, женщины',
        'IMMERSION 50 WOMEN/DAMES': 'ныряние в ластах - 50 м, женщины',
        'IMMERSION 100 WOMEN/DAMES': 'ныряние в ластах - 100 м, женщины',
        'IMMERSION 400 WOMEN/DAMES': 'ныряние в ластах - 400 м, женщины',
        'IMMERSION 800 WOMEN/DAMES': 'ныряние в ластах - 800 м, женщины',
        'BI 50 WOMEN/DAMES': 'плавание в классических ластах - 50 м, женщины',
        'BI 100 WOMEN/DAMES': 'плавание в классических ластах - 100 м, женщины',
        'BI 200 WOMEN/DAMES': 'плавание в классических ластах - 200 м, женщины',
        'BI 400 WOMEN/DAMES': 'плавание в классических ластах - 400 м, женщины',
        "RELAY 4 WOMEN/DAMES": 'эстафетное плавание 4х100 м, женщины',
    }[value]


class WRScraper:
    def __init__(self, url: str, file_path: str):
        self.file_path = file_path
        self.url = url
        self.df = None

    def scrape_wr(self):
        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        line = soup.find_all("a", "extension pdf even")[0]
        # TODO: extract the link from the line

    def extract_wr(self) -> 'WRScraper':
        df = read_pdf(self.file_path, stream=True)[0][['MEN/HOMMES']]
        # print(df)
        df[['Дистанция', 'Мировой рекорд']] = df['MEN/HOMMES'].str.split(" ", 1, expand=True)

        list_of_events = ["SURFACE", "RELAY", "IMMERSION", "BI"]
        event = None
        sex = "MEN/HOMMES"
        for idx, value in enumerate(df["Дистанция"]):
            if value in list_of_events:
                event = value

            if "WOMEN/DAMES" in value:
                sex = "WOMEN/DAMES"

            if idx + 1 <= len(df) - 1:
                if not df["Дистанция"].iloc[idx + 1] in list_of_events:
                    df["Дистанция"].iloc[idx + 1] = event + ' ' + df["Дистанция"].iloc[idx + 1] + ' ' + sex
                else:
                    pass
            else:
                break
        self.df = df.drop(columns='MEN/HOMMES')

        return self

    def drop_none_results(self) -> 'WRScraper':
        if isinstance(self.df, type(None)):
            self.extract_wr()
        for idx, value in enumerate(self.df['Мировой рекорд']):
            if isinstance(value, type(None)) or value == 'FINS':
                self.df['Мировой рекорд'].iloc[idx] = np.NAN
        self.df = self.df.dropna()

        return self

    def translate_events(self) -> 'WRScraper':
        self.drop_none_results()
        for idx, value in enumerate(self.df['Дистанция']):
            self.df['Дистанция'].iloc[idx] = english_events_to_russian(value)
        return self

    def remove_spaces(self) -> "WRScraper":
        self.translate_events()
        if "Мировой рекорд" in self.df.columns:
            for idx, value in enumerate(self.df["Мировой рекорд"]):
                if 'x ' in value:
                    self.df["Мировой рекорд"].iloc[idx] = value.split(' ')[-1]
        return self

    def wr_to_datetime(self) -> "WRScraper":
        self.remove_spaces()
        self.df["Мировой рекорд"] = pd.to_datetime(self.df["Мировой рекорд"])
        return self

    def wr_to_sec(self) -> "WRScraper":
        self.wr_to_datetime()

        self.df['Мировой рекорд в сек'] = self.df["Мировой рекорд"].dt.hour * 60 \
                                          + self.df["Мировой рекорд"].dt.minute \
                                          + self.df["Мировой рекорд"].dt.second / 100
        return self

    def return_df_with_wr(self):
        self.wr_to_sec()
        return self.df


if __name__ == "__main__":
    url = 'https://www.cmas.org/world-records'
    file_path = '/Users/evgenysaurov/PycharmProjects/finswimming_tactics/finswimming_tactics/data/005823-1-2022_03_01_' \
                'CMAS_FS_WORLD.pdf'
    # path_to_save = '/finswimming_tactics/utils/wr.csv'

    wrs = WRScraper(url=url, file_path=file_path)
    df = wrs.return_df_with_wr()
    # df.to_csv(path_to_save)
