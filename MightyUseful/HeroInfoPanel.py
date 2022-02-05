import matplotlib
import pandas as pd
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, \
    QTextBrowser, QSizePolicy, QComboBox, QStyle, QGroupBox, QVBoxLayout

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.FileIo import FileIO
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity
from MightyUseful.IoGui import IoGui
#from MightyUseful.MightyUsefulApp import MightyUsefulApp

matplotlib.use('Qt5Agg')


class HeroInfoPanel(QWidget):
    strategyList = ["Freeze", "Troops", "HighGrowth", "Might", "NoReborn", "RebornToLevel1", "EventReady"]

    def __init__(self, aParent): # MightyUsefulApp):
        super().__init__()
        self.mua = aParent

    def getInt(self, field):
        return str(self.row[field].values[0])

    def getIntLabel(self, field) -> QLabel:
        lab = QLabel(self.getInt(field))
        lab.setMaximumHeight(24)
        lab.setStyleSheet("background-color: #ff0000;")
        return lab

    def getFieldStringLabel(self, field) -> QLabel:
        aStr = str(self.row[field].values[0])
        return self.getStringLabel(aStr)

    def getStringLabel(self, aStr) -> QLabel:
        lab = QLabel(str(aStr))
        lab.setMaximumHeight(24)
        lab.setStyleSheet("background-color: #ff0000;")
        return lab

    @staticmethod
    def nice_levelup_table(army, aName, rarity, might, troops):
        # ra = HighestGrowth.get_rarity_by_name(rarity)
        nice = HighestGrowth.get_moves_by_name(aName, army)
        if nice is None or len(nice) == 0:
            return None
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

        vbox = QVBoxLayout()
        #self.setLayout(vbox)

        typeBox = QGroupBox("Basic Info")
        panelLayour = QGridLayout()
        panelLayour.setContentsMargins(0, 0, 0, 0)
        panelLayour.setColumnStretch(0, 0)
        panelLayour.setRowStretch(0, 0)
        panelLayour.addWidget(self.btn, 0, 0, 1, 4, alignment=Qt.AlignCenter)

        pixmap = IoGui.nameToPixmap(aName, 300, 300)
        picLabel = QLabel()
        picLabel.setPixmap(pixmap)
        panelLayour.addWidget(picLabel, 1, 0, 1, 4, alignment=Qt.AlignCenter)

        rarity = row['Rarity'].values[0]

        panelLayour.addWidget(QLabel("Level:"), 2, 0, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.getIntLabel('Level'), 2, 1, 1, 1)

        panelLayour.addWidget(QLabel("Reborn:"), 2, 2, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.getIntLabel('Reborns'), 2, 3, 1, 1)

        panelLayour.addWidget(QLabel("Rarity:"), 3, 0, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.getFieldStringLabel('Rarity'), 3, 1, 1, 1)

        panelLayour.addWidget(QLabel("Gender:"), 3, 2, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.getFieldStringLabel('Gender'), 3, 3, 1, 1)

        panelLayour.addWidget(QLabel("Alignment:"), 4, 0, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.getFieldStringLabel('Alignment'), 4, 1, 1, 1)

        panelLayour.addWidget(QLabel("Type:"), 4, 2, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.getFieldStringLabel('Type'), 4, 3, 1, 1)

        ra = HighestGrowth.get_rarity_by_name(rarity)
        reborn = self.row['Reborns'].values[0]
        level = self.row['Level'].values[0]
        might, troops = ra.getMightAndTroops(reborn, level)

        panelLayour.addWidget(self.getStringLabel("Troops:"), 5, 0, 1, 1, Qt.AlignRight)
        tLabel = self.getStringLabel(str(troops))
        panelLayour.addWidget(tLabel, 5, 1, 1, 1)

        panelLayour.addWidget(self.getStringLabel("Might:"), 5, 2, 1, 1, Qt.AlignRight)
        mLabel = self.getStringLabel(str(might))
        panelLayour.addWidget(mLabel, 5, 3, 1, 1)

        avail_souls = self.row['Available Souls'].values[0]
        panelLayour.addWidget(self.getStringLabel("Available Souls:"), 6, 0, 1, 1, Qt.AlignRight)
        tLabel = self.getStringLabel(str(avail_souls))
        panelLayour.addWidget(tLabel, 6, 1, 1, 1)

        self.shapeCombo = QComboBox(self)
        optionList = sorted(HeroInfoPanel.strategyList)
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

        panelLayour.addWidget(self.getStringLabel("Strategy:"), 6, 2, 1, 1, Qt.AlignRight)
        panelLayour.addWidget(self.shapeCombo, 6, 3, 1, 1)

        box_row = 7
        evolves_from = self.army.get_evolve_froms(aName)
        evolves_to = self.army.get_evolve_tos(aName)
        if len(evolves_from) > 0:
            myLab = ",".join(evolves_from)
            panelLayour.addWidget(self.getStringLabel("Evolves from:"), box_row, 0, 1, 1, Qt.AlignRight)
            panelLayour.addWidget(self.getStringLabel(myLab), box_row, 1, 1, 3)
            box_row = box_row + 1

        if len(evolves_to) > 0:
            myLab = ",".join(evolves_to)
            panelLayour.addWidget(self.getStringLabel("Evolves to:"), box_row, 0, 1, 1, Qt.AlignRight)
            panelLayour.addWidget(self.getStringLabel(myLab), box_row, 1, 1, 3)
            box_row = box_row + 1

        typeBox.setLayout(panelLayour)
        vbox.addWidget(typeBox)

        some_html = self.nice_levelup_table(army, aName, rarity, might, troops)
        if some_html is not None:
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
            vbox.addWidget(self.text_browser) #, box_row, 0, 15, 4)
            box_row = box_row + 1
            # text_browser.show()
            # text_browser.raise_()

            #vbox.setRowStretch(99, 1)
            #vbox.setColumnStretch(99, 1)
        # vbox.addWidget(QLabel("Evolves from:" + str(evolves_from)))

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
        self.mua.invalidate_filters()
        # self.setHero(self.row, self.army) causes loop


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.army = Army()
        FileIO.getArmy(self, self.army)  # FIXME: bugged after moving shit around?
        hg = HighestGrowth(self.army)

        row = self.army.lookup("Villano Mad Genius")
        sc = HeroInfoPanel()
        sc.setHero(row, self.army)  # width=5, height=4, dpi=100)
        self.setCentralWidget(sc)
        self.show()

# app = QApplication(sys.argv)
# w = MainWindow()
# app.exec_()
