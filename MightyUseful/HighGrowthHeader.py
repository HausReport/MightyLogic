from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide2.QtCore import Qt


class HighGrowthHeader(QWidget):

    def __init__(self):
        super().__init__()
        self.myLayout = QGridLayout()
        self.setLayout(self.myLayout)

        self.rerun = QPushButton("Run High Growth")
        self.myLayout.addWidget(self.rerun, 0, 0, 1, 1, alignment=Qt.AlignCenter)
