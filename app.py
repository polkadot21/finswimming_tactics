# -*- coding: utf-8 -*-
"""
tiny_example.py
:copyright: (c) 2015 by C. W.
:license: GPL v3 or BSD
"""
from datetime import datetime

import flask
from flask import Flask, request
import flask_excel as excel
import pandas as pd

from utils._add_wr_to_data import _add_wr_with_to_data
from utils._scrape_wr import WRScraper
from utils import _reformat_tables_xls
from utils import _ranking_system

app = Flask(__name__)


def compute_scores(B: float, T: float) -> int:
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


def time_to_sec(time: datetime.time) -> int:
    return 60 * time.minute + time.second


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f == "<FileStorage: '2022_04_15-16_PgYa.xlsx' ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')>":
            print(f)
        else:
            f = 'data/2022_04_15-16_PgYa.xlsx'
        data_xls = pd.read_excel(f, header=11)[['Место', 'Результат']]

        data_reformater = _reformat_tables_xls.ExcelTable(table=data_xls)
        data_xls = data_reformater.return_table(reformat=True)

        RS = _ranking_system.RankingSystem(df=data_xls)
        df_with_scores = RS.return_df_with_scores()

        url = 'https://www.cmas.org/world-records'
        file_path = 'data/005823-1-2022_03_01_CMAS_FS_WORLD.pdf'

        wrs = WRScraper(url=url, file_path=file_path)
        wr = wrs.return_df_with_wr()

        df_with_scores_and_wr = _add_wr_with_to_data(df=df_with_scores, wr=wr)

        #df_with_scores_and_wr['Результат'] = pd.to_datetime(df_with_scores_and_wr['Результат'])



        #df_with_scores_and_wr['Результат сек'] = df_with_scores_and_wr['Результат'].dt.hour * 60 \
        #                                         + df_with_scores_and_wr['Результат'].dt.minute \
        #                                         + df_with_scores_and_wr['Результат'].dt.second / 100

        for idx, value in enumerate(df_with_scores_and_wr['Количество очков']):
            df_with_scores_and_wr['Количество очков'].iloc[idx] \
                = compute_scores(B=df_with_scores_and_wr['Мировой рекорд'].iloc[idx],
                                 T=time_to_sec(df_with_scores_and_wr['Результат'].iloc[idx]))

        text_file = open("templates/table.html", "w")
        text_file.write(df_with_scores_and_wr.to_html())
        text_file.close()

        return flask.redirect(flask.url_for('show_table'))
    return flask.render_template('index.html')


@app.route("/table")
def show_table():
    return flask.render_template("table.html")


# insert database related code here
if __name__ == "__main__":
    excel.init_excel(app)
    app.run()
