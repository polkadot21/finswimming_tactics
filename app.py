# -*- coding: utf-8 -*-
"""
tiny_example.py
:copyright: (c) 2015 by C. W.
:license: GPL v3 or BSD
"""

import flask
from flask import Flask, request
import flask_excel as excel
import pandas as pd
from utils import _reformat_tables_xls
from finswimming_tactics.utils._ranking_system import RankingSystem

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        data_xls = pd.read_excel(f, header=11)[['Место', 'Результат']]

        data_reformater = _reformat_tables_xls.ExcelTable(table = data_xls)
        data_xls = data_reformater.return_table(reformat=True)

        RS = RankingSystem(df=data_xls)
        df_with_scores = RS.return_df_with_scores()

        text_file = open("templates/table.html", "w")
        text_file.write(df_with_scores.to_html())
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