
import pandas as pd
import numpy as np

class ExcelTable:
    def __init__(self, table: pd.DataFrame):
        self.table = table

    def _add_index_column(self):
        self.table['Изначальный индекс'] = self.table.index + 12
        self.table = self.table.dropna(how='all')
        return self

    def _add_events(self):
        """ADD EVENTS"""
        for idx, value in enumerate(self.table['Место']):
            if not isinstance(value, str):
                self.table['Место'].iloc[idx] = np.NaN
            elif 'плавание' not in value:
                self.table['Место'].iloc[idx] = np.NaN

        return self

    def _add_first_event(self):
        """ADD FIRST EVENT"""

        self._add_events()

        self.table['Место'].iloc[0] = 'плавание в ластах - 50 м, девочки'
        return self

    def _filL_na_in_events(self):
        """FILL ALL Values with EVENTS"""

        self._add_first_event()

        self.table['Место'] = self.table['Место'].fillna(method='ffill')
        return self

    def _fill_na_in_times(self):
        """FILL NA In Times"""

        self._filL_na_in_events()

        for idx, value in enumerate(self.table['Результат']):
            if isinstance(value, str):
                self.table['Результат'].iloc[idx] = np.NaN
            elif not isinstance(value, type(self.table['Результат'].iloc[0])):
                self.table['Результат'].iloc[idx] = np.NaN

        self.table = self.table.dropna(how='any')
        return self

    def return_table(self, reformat: bool = True):

        if reformat:
            self._fill_na_in_times()
            return self.table
        else:
            return self.table

