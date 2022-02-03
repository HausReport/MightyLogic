from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QGroupBox
from PySide2.QtCore import Qt


class HighGrowthHeader(QWidget):

    def __init__(self):
        super().__init__()
        self.myLayout = QVBoxLayout()
        self.setLayout(self.myLayout)

        limitsBox = QGroupBox("Your High Growth Limits")
        limitsBoxLayout = QVBoxLayout()
        self.rerun = QPushButton("Run High Growth")
        limitsBoxLayout.addWidget(self.rerun)

        limitsBox.setLayout(limitsBoxLayout)

        self.myLayout.addWidget(limitsBox)

