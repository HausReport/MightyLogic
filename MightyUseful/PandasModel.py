import PySide2.QtCore as QtCore
from natsort import natsorted, index_natsorted, order_by_index

import pandas as pd
class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data_int(self, index, role):
       if role == QtCore.Qt.DisplayRole:
           val: int = self._data.iloc[index.row(), index.column()]
           numbers = "{:,}".format(val)
           return numbers
       elif role == QtCore.Qt.TextAlignmentRole:
           return QtCore.Qt.AlignRight

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if index.column() in [2, 3, 4, 9, 10]:
                return self.data_int(index, role)
            elif role == QtCore.Qt.DisplayRole:
                return self._data.iloc[index.row(), index.column()]
        return None

    def headerData(self, col, orientation, role):

        #print(str(orientation))
        #print(str(role))
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def sort(self, column, order):
        if order == 0:
            self._dataframe = self._dataframe.reindex(
                index=order_by_index(self._dataframe.index, index_natsorted(self._dataframe[column])))
        else:
            self._dataframe = self._dataframe.reindex(
                index=order_by_index(self._dataframe.index, reversed(index_natsorted(self._dataframe[column]))))

        self._dataframe.reset_index(inplace=True, drop=True)
        self.setDataFrame(self._dataframe)