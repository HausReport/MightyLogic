from PySide2.QtGui import QTextDocument
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QGroupBox, QLineEdit, QTextBrowser
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

        searchBox = QGroupBox("Search")
        searchBoxLayout = QGridLayout()
        self.textbox = QLineEdit(self)
        searchBoxLayout.addWidget(self.textbox,0,0,1,2)
        self.find = QPushButton("Find Forward")
        self.find.clicked.connect(self.find_in_table)
        searchBoxLayout.addWidget(self.find,1,0,1,1)
        self.find = QPushButton("Find Backward")
        self.find.clicked.connect(self.find_in_table_backwards)
        searchBoxLayout.addWidget(self.find,1,1,1,1)

        searchBox.setLayout(searchBoxLayout)
        self.myLayout.addWidget(searchBox)


        analysisBox = QGroupBox("Analysis")
        analysisBoxLayout = QVBoxLayout()

        self.text_browser = QTextBrowser()
        self.text_browser.setSearchPaths(["../MightyLogic/image/"])
        #self.text_browser.setText(html)
        analysisBoxLayout.addWidget(self.text_browser)

        analysisBox.setLayout(analysisBoxLayout)
        self.myLayout.addWidget(analysisBox)

    @Slot()
    def rerun_high_growth(self):
       self.hgt.rerun_high_growth()

    def do_analysis(self, frame: pd.DataFrame):
        html = ""
        nMoves = len(frame)
        html += f"Number of moves: {nMoves} <br>"
        nHeroes = frame.Name.nunique()
        html += f"Number of unique heroes: {nHeroes} <br>"
        totGold = frame['Total Gold'].max()
        html += f"Total Gold: {totGold:,} <br>"

        totLU = frame['Total LevelUps'].max()
        html += f"Total Level-Ups: {totLU:,} <br>"
        totTroopGain = frame['Total Troop Gain'].max()
        html += f"Total Troop Gain: {totTroopGain:,} <br>"

        GPL = int(totGold/totLU)
        html += f"Gold per Level-Up: {GPL:,} <br>"
        GPT = int(totGold/totTroopGain)
        html += f"Gold per Troop: {GPT:,} <br>"

        self.text_browser.setText(html)

    def table_changed(self, frame: pd.DataFrame):
        print("Header got table_changed")
        self.do_analysis(frame)
        #self.hdr.table_changed(frame)

    @Slot()
    def find_in_table(self): #, text):
        self.hgt.find_in_table(self.textbox.text())

    @Slot()
    def find_in_table_backwards(self, flag): #, text):
        flag = QTextDocument.FindBackward
        self.hgt.find_in_table(self.textbox.text(), flag)