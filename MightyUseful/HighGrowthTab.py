import pandas as pd
from PySide2.QtWidgets import QSplitter, QWidget, QVBoxLayout
from PySide2.QtCore import Qt

from MightyUseful.HighGrowthHeader import HighGrowthHeader
from MightyUseful.HighGrowthTable import HighGrowthTable


class HighGrowthTab(QWidget):

    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.splitter = QSplitter(self, Qt.Horizontal)
        self.hdr = HighGrowthHeader(self)
        self.splitter.addWidget(self.hdr)
        self.table = HighGrowthTable(self)
        self.splitter.addWidget(self.table)
        vbox.addWidget(self.splitter)

    def table_changed(self, frame: pd.DataFrame):
        self.hdr.table_changed(frame)

    def rerun_high_growth(self):
        self.table.rerun_high_growth()

    def percent_done(self, pct):
        print("Percent done: " + str(pct))