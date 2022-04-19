# -*- coding: utf-8 -*-
"""
tiny_example.py
:copyright: (c) 2015 by C. W.
:license: GPL v3 or BSD
"""
from datetime import datetime

from flask import Flask, request, jsonify
from tablib import Dataset
import flask_excel as excel
import pandas as pd
import numpy as np

app=Flask(__name__)

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        data_xls = pd.read_excel(f, header=11)[['Место', 'Результат']]
        data_xls['Изначальный индекс'] = data_xls.index+12

        data_xls = data_xls.dropna(how='all')

        print(data_xls)

        #### ADD EVENTS
        for idx, value in enumerate(data_xls['Место']):
            if not isinstance(value, str):
                data_xls['Место'].iloc[idx] = np.NaN
            elif 'плавание' not in value:
                data_xls['Место'].iloc[idx] = np.NaN

        #### ADD FIRST EVENT
        data_xls['Место'].iloc[0] = 'плавание в ластах - 50 м, девочки'

        ###FILL ALL Values with EVENTS
        data_xls['Место'] = data_xls['Место'].fillna(method='ffill')

        #### FILL NA In Times
        for idx, value in enumerate(data_xls['Результат']):
            if isinstance(value, str):
                data_xls['Результат'].iloc[idx] = np.NaN
            elif not isinstance(value, type(data_xls['Результат'].iloc[0])):
                data_xls['Результат'].iloc[idx] = np.NaN

        data_xls = data_xls.dropna(how='any')

        return data_xls.to_html()
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
   </form>
    '''

@app.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name="export_data")


@app.route("/download_file_named_in_unicode", methods=['GET'])
def download_file_named_in_unicode():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name=u"中文文件名")


# insert database related code here
if __name__ == "__main__":
    excel.init_excel(app)
    app.run()