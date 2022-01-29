import matplotlib
import pandas as pd

from MightyLogic.HighGrowth.Erlaed.FileIo import FileIO
from MightyUseful.IoGui import IoGui
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, \
    QTextBrowser, QSizePolicy, QComboBox
from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from PySide2.QtCore import Qt
matplotlib.use('Qt5Agg')


class MplCanvas(QWidget):
    strategyList = ["Freeze", "Troops", "HighGrowth", "Might", "NoReborn", "RebornToLevel1", "EventReady"]

    def getInt(self, field):
        return str(self.row[field].values[0])

    def getIntLabel(self, field) -> QLabel:
        return QLabel(self.getInt(field))

    def getStringLabel(self, field) -> QLabel:
        return QLabel(str(self.row[field].values[0]))

    @staticmethod
    def nice_levelup_table(army, aName, rarity, might, troops):
        ra = Rarity.get_rarity_by_name(rarity)
        nice = ra.get_moves_by_name(army.data_frame, aName)
        if nice is None or len(nice) == 0:
            return "<i>None available.</i>"
        nice = nice.copy(deep=True)
        nice = nice[['Reborn', 'Level', 'Cum Souls', 'Cum Gold', 'Troops', 'Might', 'LevelUps', 'Score']]
        nice = nice.reindex()
        for i in nice.columns:
            try:
                nice[[i]] = nice[[i]].astype(float)
            except:
                pass
        pd.options.display.float_format = '{:,.0f}'.format
        nice.rename(columns={'Cum Souls': 'Souls', 'Cum Gold': 'Gold'}, inplace=True)

        if troops > 0:
            nice['Troops'] -= troops
            nice.rename(columns={'Troops': 'Troop ∆'}, inplace=True)
        if might > 0:
            nice['Might'] -= might
            nice.rename(columns={'Might': 'Might ∆'}, inplace=True)
        return nice.to_html(index=False, classes="mystyle")

    def setHero(self, row, army):
        self.row = row
        self.army = army
        aName = row['Name'].values[0]
        self.btn = QLabel(aName)
        self.btn.setStyleSheet("color: white; background-color: black; font-size: 24pt; text-align: center;")
        self.btn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.btn.setMaximumWidth(375)
        self.btn.setMinimumWidth(375)
        self.setMaximumWidth(375)
        self.setMinimumWidth(375)
        vbox = QGridLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.btn, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        pixmap = IoGui.nameToPixmap(aName, 300, 300)
        picLabel = QLabel()
        picLabel.setPixmap(pixmap)
        vbox.addWidget(picLabel, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        rarity = row['Rarity'].values[0]

        vbox.addWidget(QLabel("Level:"), 2, 0, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.getIntLabel('Level'), 2, 1, 1, 1)

        vbox.addWidget(QLabel("Reborn:"), 2, 2, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.getIntLabel('Reborns'), 2, 3, 1, 1)

        vbox.addWidget(QLabel("Rarity:"), 3, 0, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.getStringLabel('Rarity'), 3, 1, 1, 1)

        vbox.addWidget(QLabel("Gender:"), 3, 2, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.getStringLabel('Gender'), 3, 3, 1, 1)

        vbox.addWidget(QLabel("Alignment:"), 4, 0, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.getStringLabel('Alignment'), 4, 1, 1, 1)

        vbox.addWidget(QLabel("Type:"), 4, 2, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.getStringLabel('Type'), 4, 3, 1, 1)

        ra = Rarity.get_rarity_by_name(rarity)
        reborn = self.row['Reborns'].values[0]
        level = self.row['Level'].values[0]
        might, troops = ra.getMightAndTroops(reborn, level)

        vbox.addWidget(QLabel("Troops:"), 5, 0, 1, 1, Qt.AlignRight)
        tLabel = QLabel(str(troops))
        vbox.addWidget(tLabel, 5, 1, 1, 1)

        vbox.addWidget(QLabel("Might:"), 5, 2, 1, 1, Qt.AlignRight)
        mLabel = QLabel(str(might))
        vbox.addWidget(mLabel, 5, 3, 1, 1)

        avail_souls = self.row['Available Souls'].values[0]
        vbox.addWidget(QLabel("Available Souls:"), 6, 0, 1, 1, Qt.AlignRight)
        tLabel = QLabel(str(avail_souls))
        vbox.addWidget(tLabel, 6, 1, 1, 1)

        self.shapeCombo = QComboBox(self)
        optionList = sorted(MplCanvas.strategyList)
        self.shapeCombo.addItems(optionList)
        self.shapeCombo.currentTextChanged.connect(self.stratChanged)
        # self.shapeCombo.setEditable(False)

        strat = str(self.row['Strategy'].values[0])
        index = self.shapeCombo.findText(strat)
        if index != -1:  # -1 for not found
            print("Found: " + strat)
            self.shapeCombo.setCurrentIndex(index)
        else:
            print("Couldn't find: [" + strat + "]")
            index = self.shapeCombo.findText("Freeze")
            if index != -1:  # -1 for not found
                print("Found: " + strat)
                self.shapeCombo.setCurrentIndex(index)

        self.army.updateStrategy(aName, strat)

        vbox.addWidget(QLabel("Strategy:"), 6, 2, 1, 1, Qt.AlignRight)
        vbox.addWidget(self.shapeCombo, 6, 3, 1, 1)

        some_html = self.nice_levelup_table(army, aName, rarity, might, troops)
        self.text_browser = QTextBrowser()
        css = """
<html>
<head>
<style>     
/* includes alternating gray and white with on-hover color */

.mystyle {
    font-size: 12pt; 
    font-family: Arial Narrow;
    border-collapse: collapse; 
    border: 0px solid silver;
    font-variant-numeric: tabular-nums;
    text-align: right;
}

.mystyle td, th {
    padding: 0px;
    font-size: 12pt; 
    text-align: right;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}</style></head><body>
        """
        self.text_browser.setText("<h2>Recommended Level-Ups</h2>" + css + some_html)
        vbox.addWidget(self.text_browser, 7, 0, 15, 4)
        # text_browser.show()
        # text_browser.raise_()

        # TODO:
        # Evolves to
        # Evolves from
        # ~~Image~~
        # ~~Possible Levelups~~

        self.setLayout(vbox)

    def stratChanged(self):
        newStrat = self.shapeCombo.currentText()
        aName = self.row['Name'].values[0]
        print("Name = " + aName)
        self.army.updateStrategy(aName, newStrat)
        # self.setHero(self.row, self.army) causes loop


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.army = Army()
        FileIO.getArmy(self, self.army)
        hg = HighestGrowth(self.army)

        row = self.army.lookup("Villano Mad Genius")
        sc = MplCanvas()
        sc.setHero(row, self.army)  # width=5, height=4, dpi=100)
        self.setCentralWidget(sc)
        self.show()

# app = QApplication(sys.argv)
# w = MainWindow()
# app.exec_()
