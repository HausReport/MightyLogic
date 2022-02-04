from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QGroupBox
from PySide2.QtCore import Qt, Slot
import pandas as pd

class HighGrowthHeader(QWidget):

    def __init__(self, aParent):
        super().__init__()
        self.hgt = aParent
        self.myLayout = QVBoxLayout()
        self.setLayout(self.myLayout)

        limitsBox = QGroupBox("Your High Growth Limits")
        limitsBoxLayout = QVBoxLayout()
        self.rerun = QPushButton("Run High Growth")
        self.rerun.clicked.connect(self.rerun_high_growth)
        limitsBoxLayout.addWidget(self.rerun)

        limitsBox.setLayout(limitsBoxLayout)

        self.myLayout.addWidget(limitsBox)

    @Slot()
    def rerun_high_growth(self):
       self.hgt.rerun_high_growth()

    def table_changed(self, frame: pd.DataFrame):
        print("Header got table_changed")
        #self.hdr.table_changed(frame)