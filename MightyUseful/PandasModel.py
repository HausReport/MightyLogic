import PySide2.QtCore as QtCore
from PySide2.QtGui import QIcon, QImage, QPixmap
from PySide2.QtWidgets import QPushButton
from natsort import natsorted, index_natsorted, order_by_index
from pathlib import Path

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
            elif index.column() == 0:
                if role == QtCore.Qt.DecorationRole: # or role == QtCore.Qt.ToolTipRole:
                    aName = self._data.iloc[index.row(),1]
                    aName = aName.replace(' ', '_')  # need to replace spaces with underline
                    aName = aName.replace('"', '')  # need to replace spaces with underline
                    if aName.endswith('rmun_Grand'):
                        aName = "J%3Frmun_Grand"
                    if aName.endswith('tunn'):
                        aName = "J%3Ftunn"
                    aName += '.png'
                    path = Path.cwd() / ".." / "MightyLogic" / "image" / aName
                    print(path)
                    print(path.exists())

                    print("role = " + str(role))
                    #icon = QIcon(str(path.absolute()))
                    image = QImage(str(path.absolute()))
                    pixmap = QPixmap.fromImage(image)
                    return pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
                    #return pixmap
                    #button = QPushButton(icon,"")
                    #button.setIconSize(QtCore.QSize(100, 100))
                    #return icon
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