from urllib.request import urlopen
from bs4 import BeautifulSoup

from tabula.io import read_pdf


def scrape_wr(url: str = 'https://www.cmas.org/world-records'):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    line = soup.find_all("a", "extension pdf even")[0]
    # TODO: extract the link from the line


file_path = '/Users/evgenysaurov/PycharmProjects/finswimming_tactics/finswimming_tactics/data/005823-1-2022_03_01_' \
            'CMAS_FS_WORLD.pdf'


def extract_wr(file_path: str):
    df = read_pdf(file_path, stream=True)[0][['MEN/HOMMES']]
    # print(df)
    df[['Дистанция', 'Мировой рекорд']] = df['MEN/HOMMES'].str.split(" ", 1, expand=True)
    print(df)
