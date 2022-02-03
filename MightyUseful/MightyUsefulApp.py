import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QWidget, \
    QCheckBox, QGroupBox, QHBoxLayout, QSplitter, QSizePolicy, QLabel, QSpinBox, QTabWidget, QPushButton

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.HighGrowthTab import HighGrowthTab
from MightyUseful.HighGrowthTable import HighGrowthTable
from MightyUseful.IntRangeFilter import IntRangeFilter
from MightyUseful.RegExFilter import RegExFilter
from MightyUseful.IoGui import IoGui
from MightyUseful.MultiFilterProxyModel import MultiFilterProxyModel
from MightyUseful.PandasModel import PandasModel
from MightyUseful.HeroInfoPanel import HeroInfoPanel


class MightyUsefulApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.setWindowTitle("MightyUseful")
        self.setGeometry(300, 300, 500, 400)

        self.create_menu()
        self.table = QtWidgets.QTableView()
        vHead = self.table.verticalHeader()
        vHead.setIconSize(QSize(100, 100))
        self.army = Army()
        IoGui.getArmy(self, self.army)
        hg = HighestGrowth(self.army)

        self.model = PandasModel(self.army.data_frame)
        self.proxy = MultiFilterProxyModel(self)
        # self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.clicked.connect(self.set_hero_drilldown)
        self.table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        tabs = QTabWidget()
        wholeUiWidget = QWidget()
        wholeUiWidgetLayout = QVBoxLayout()
        horizontalFilterBoxLayout = QHBoxLayout()
        horizontalFilterBox = QWidget()
        # form = QWidget()
        # formLayout = QFormLayout()

        # nameLineEdit = QLineEdit()
        # emailLineEdit = QLineEdit()
        # ageSpinBox = QLineEdit()

        alignmentBox = QGroupBox("Alignment")
        box1 = QVBoxLayout()
        self.showChaos = QCheckBox("Chaos")
        self.showChaos.stateChanged.connect(self.checkBoxChange)
        box1.addWidget(self.showChaos)
        self.showOrder = QCheckBox("Order")
        self.showOrder.stateChanged.connect(self.checkBoxChange)
        box1.addWidget(self.showOrder)
        self.showNature = QCheckBox("Nature")
        self.showNature.stateChanged.connect(self.checkBoxChange)
        box1.addWidget(self.showNature)
        alignmentBox.setLayout(box1)
        horizontalFilterBoxLayout.addWidget(alignmentBox)

        genderBox = QGroupBox("Gender")
        box2 = QVBoxLayout()
        self.showMale = QCheckBox("Male")
        self.showMale.stateChanged.connect(self.checkBoxChange)
        box2.addWidget(self.showMale)
        self.showFemale = QCheckBox("Female")
        self.showFemale.stateChanged.connect(self.checkBoxChange)
        box2.addWidget(self.showFemale)
        self.showNeuter = QCheckBox("Neuter")
        self.showNeuter.stateChanged.connect(self.checkBoxChange)
        box2.addWidget(self.showNeuter)
        genderBox.setLayout(box2)
        horizontalFilterBoxLayout.addWidget(genderBox)

        typeBox = QGroupBox("Type")
        box3 = QVBoxLayout()
        self.showMelee = QCheckBox("Melee")
        self.showMelee.stateChanged.connect(self.checkBoxChange)
        box3.addWidget(self.showMelee)
        self.showRanged = QCheckBox("Ranged")
        self.showRanged.stateChanged.connect(self.checkBoxChange)
        box3.addWidget(self.showRanged)
        self.showBuilding = QCheckBox("Building")
        self.showBuilding.stateChanged.connect(self.checkBoxChange)
        box3.addWidget(self.showBuilding)
        typeBox.setLayout(box3)
        horizontalFilterBoxLayout.addWidget(typeBox)

        rarityBox = QGroupBox("Rarity")
        box4 = QVBoxLayout()
        self.showCommon = QCheckBox("Common")
        self.showCommon.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showCommon)
        self.showRare = QCheckBox("Rare")
        self.showRare.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showRare)
        self.showEpic = QCheckBox("Epic")
        self.showEpic.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showEpic)
        self.showLegendary = QCheckBox("Legendary")
        self.showLegendary.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showLegendary)
        rarityBox.setLayout(box4)
        horizontalFilterBoxLayout.addWidget(rarityBox)

        rebornBox = QGroupBox("Reborn")
        box4 = QVBoxLayout()
        self.showReborn0 = QCheckBox("Reborn 0")
        self.showReborn0.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showReborn0)
        self.showReborn1 = QCheckBox("Reborn 1")
        self.showReborn1.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showReborn1)
        self.showReborn2 = QCheckBox("Reborn 2")
        self.showReborn2.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showReborn2)
        self.showReborn3 = QCheckBox("Reborn 3")
        self.showReborn3.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showReborn3)
        self.showReborn4 = QCheckBox("Reborn 4")
        self.showReborn4.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showReborn4)
        self.showReborn5 = QCheckBox("Reborn 5")
        self.showReborn5.stateChanged.connect(self.checkBoxChange)
        box4.addWidget(self.showReborn5)
        rebornBox.setLayout(box4)
        horizontalFilterBoxLayout.addWidget(rebornBox)

        strategyBox = QGroupBox("Levelling Strategy")
        box5 = QVBoxLayout()

        self.showEventReady = QCheckBox("Event Ready")
        self.showEventReady.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showEventReady)
        self.showFreeze = QCheckBox("Freeze")
        self.showFreeze.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showFreeze)
        self.showHighGrowth = QCheckBox("HighGrowth")
        self.showHighGrowth.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showHighGrowth)
        self.showMight = QCheckBox("Might")
        self.showMight.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showMight)
        self.showNoReborn = QCheckBox("NoReborn")
        self.showNoReborn.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showNoReborn)
        self.showRebornToLevel1 = QCheckBox("RebornToLevel1")
        self.showRebornToLevel1.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showRebornToLevel1)
        self.showTroops = QCheckBox("Troops")
        self.showTroops.stateChanged.connect(self.checkBoxChange)
        box5.addWidget(self.showTroops)

        strategyBox.setLayout(box5)
        horizontalFilterBoxLayout.addWidget(strategyBox)

        horizontalFilterBox2 = QWidget()
        horizontalFilterBoxLayout2 = QHBoxLayout()
        self.fromSpin = QSpinBox()
        self.fromSpin.setRange(1, 31)
        self.fromSpin.setValue(1)
        # fromSpin.setReadOnly(True)
        self.toSpin = QSpinBox()
        self.toSpin.setRange(1, 31)
        self.toSpin.setValue(31)

        self.fromSpin.valueChanged.connect(self.spinChanged)
        self.toSpin.valueChanged.connect(self.spinChanged)
        horizontalFilterBoxLayout2.addWidget(QLabel("From level"))
        horizontalFilterBoxLayout2.addWidget(self.fromSpin)
        horizontalFilterBoxLayout2.addWidget(QLabel("to level"))
        horizontalFilterBoxLayout2.addWidget(self.toSpin)
        # form.setLayout(formLayout)
        leftWidget = QWidget()
        leftWidgetLayout = QVBoxLayout()

        horizontalFilterBox.setLayout(horizontalFilterBoxLayout)
        leftWidgetLayout.addWidget(horizontalFilterBox)
        horizontalFilterBox2.setLayout(horizontalFilterBoxLayout2)
        leftWidgetLayout.addWidget(horizontalFilterBox2)
        leftWidgetLayout.addWidget(self.table)
        leftWidget.setLayout(leftWidgetLayout)
        # vbox.addWidget(form)

        self.splitter = QSplitter(self, Qt.Horizontal)
        self.splitter.addWidget(leftWidget)

        # self.btn = QPushButton("Hi")
        # self.btn.setMinimumHeight(1000)
        # splitter.addWidget(self.btn)
        self.heroInfo = HeroInfoPanel()
        self.heroInfo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.splitter.addWidget(self.heroInfo)

        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        wholeUiWidgetLayout.addWidget(self.splitter)
        wholeUiWidget.setLayout(wholeUiWidgetLayout)

        tabs.addTab(wholeUiWidget, "Army Explorer")
        tabs.addTab(QPushButton("Hi"), "Army Analyzer")
        hgt = HighGrowthTab()
        tabs.addTab(hgt, "High Growth")
        self.setCentralWidget(tabs)
        # self.showMaximized()
        self.showFullScreen()
        self.show()
        self.setHeroByName("Charon, Soul Catcher")

    def set_hero_drilldown(self, item):
        """
        User clicked on a row, set drilldown display on right to display that hero.
        :param item:
        :return:
        """
        sf = "You clicked on {0}x{1}".format(item.column(), item.row())
        print(sf)
        print(type(item))
        # mod: QAbstractItemModel = item.model()
        foo = self.proxy.index(item.row(), 1, item)
        bar = self.proxy.data(foo, Qt.DisplayRole)
        self.setHeroByName(bar)
        # self.btn.setText(bar)

    def setHeroByName(self, aName):
        """
       Sets the current hero to the named hero.
        :param aName: name of hero
        :return:
        """
        hero = self.army.lookup(aName)
        if hero is None:
            print("Bad hero name: " + aName)
            # FIXME: handle case when hero is none
        else:
            newHeroInfo = HeroInfoPanel()
            newHeroInfo.setHero(hero, self.army)
            self.splitter.replaceWidget(1, newHeroInfo)
            self.heroInfo = newHeroInfo
            print(hero)
        hero = self.army.lookup(aName)
        if hero is None:
            print("Bad hero name: " + aName)
        else:
            newHeroInfo = HeroInfoPanel()
            newHeroInfo.setHero(hero, self.army)
            self.splitter.replaceWidget(1, newHeroInfo)
            self.heroInfo = newHeroInfo
            print(hero)

    def spinChanged(self, value):
        print(str(self.fromSpin.value()))
        print(str(self.toSpin.value()))
        reg = IntRangeFilter(self.fromSpin.value(), self.toSpin.value())
        self.proxy.setFilterByColumn(2, reg)

    def checkBoxChange(self, state):
        """
        Handle when user clicks a filter checkbox.
        :param state:
        :return:
        """
        aList = []
        if self.showChaos.isChecked():
            aList.append("Chaos")
        if self.showOrder.isChecked():
            aList.append("Order")
        if self.showNature.isChecked():
            aList.append("Nature")
        reg = '(' + '|'.join(aList) + ')'
        self.proxy.setFilterByColumn(7, reg)

        aList = []
        if self.showMale.isChecked():
            aList.append("Male")
        if self.showFemale.isChecked():
            aList.append("Female")
        if self.showNeuter.isChecked():
            aList.append("Middle_Gender")
        reg = '(' + '|'.join(aList) + ')'
        self.proxy.setFilterByColumn(6, reg)

        aList = []
        if self.showMelee.isChecked():
            aList.append("Melee")
        if self.showRanged.isChecked():
            aList.append("Ranged")
        if self.showBuilding.isChecked():
            aList.append("Building")
        reg = '(' + '|'.join(aList) + ')'
        self.proxy.setFilterByColumn(8, reg)

        aList = []
        if self.showCommon.isChecked():
            aList.append("Common")
        if self.showRare.isChecked():
            aList.append("Rare")
        if self.showEpic.isChecked():
            aList.append("Epic")
        if self.showLegendary.isChecked():
            aList.append("Legendary")
        reg = '(' + '|'.join(aList) + ')'
        self.proxy.setFilterByColumn(5, reg)

        aList = []
        if self.showReborn0.isChecked():
            aList.append("0")
        if self.showReborn1.isChecked():
            aList.append("1")
        if self.showReborn2.isChecked():
            aList.append("2")
        if self.showReborn3.isChecked():
            aList.append("3")
        if self.showReborn4.isChecked():
            aList.append("4")
        if self.showReborn5.isChecked():
            aList.append("5")
        reg = '(' + '|'.join(aList) + ')'
        self.proxy.setFilterByColumn(3, reg)

        aList = []
        if self.showEventReady.isChecked():
            aList.append("EventReady")
        if self.showFreeze.isChecked():
            aList.append("Freeze")
        if self.showHighGrowth.isChecked():
            aList.append("HighGrowth")
        if self.showMight.isChecked():
            aList.append("Might")
        if self.showNoReborn.isChecked():
            aList.append("NoReborn")
        if self.showRebornToLevel1.isChecked():
            aList.append("RebornToLevel1")
        if self.showTroops.isChecked():
            aList.append("Troops")
        reg = '(' + '|'.join(aList) + ')'
        self.proxy.setFilterByColumn(11, RegExFilter(reg))

        strategyList = ["EventReady", "Freeze", "HighGrowth", "Might", "NoReborn", "RebornToLevel1", "Troops"]

    def create_menu(self):
        """
        Creates the menuing system
        :return:
        """
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("Edit")
        searchMenu = mainMenu.addMenu("Font")
        helpMenu = mainMenu.addMenu("Help")

        openAction: QAction = QAction(QIcon('open.png'), "Open", self)
        openAction.setShortcut("Ctrl+O")

        saveAction = QAction(QIcon('save.png'), "Save", self)
        saveAction.setShortcut("Ctrl+S")

        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+X")

        exitAction.triggered.connect(self.exit_app)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

    def exit_app(self):
        self.close()


myApp = QApplication(sys.argv)
window = MightyUsefulApp()
myApp.exec_()
sys.exit(0)

# TODO:
# 3) add "can level up"
# 4) add "can reborn"/reborn level
# 8) gold discount ui
# 12) load discounts
# 13) Score - see Hanzo Sama case, lots of levels similar score to 1 level.  See also spreadsheet
# 17) Help system
# 23) Implement high-growth functionality
# 25) dialogue input might, click rarity, get level, reborn, soulbinds
# 25) dialogue input fame, get league and completion back
# 28) Limit table results by gold, HG stage, troops
# 29) Point out highest might lev/reb for reboosts
# 30) EventReady isn't getting the moves NoReborn gets
# 31) ~~Add top widget for HG tab~~


# 32) ~~Install NSIS installer system~~
# 26) ~~Show change in HG stage in table~~
# 29) ~~Show strategy in table, join with strats on Name~~
# 27) ~~Hero image in table~~
# 24) ~~Hide levelup table if empty~~
# 20) ~~Support for from level to level filter~~
# 18) ~~Show evolves to~~
# 19) ~~Show evolves from~~
# 22) ~~Refactor bulk of hg stuff from Rarity to HighestGrowth~~
# ~~21) Move default strategies from notebook to API~~
# 1) ~~add tabs~~
# 5) ~~tab for army analysis~~
# 6) ~~tab for high growth~~
# 21) ~~Start in full screen mode ~~
# 15) ~~Filters for strategy~~
# 16) Not necessary: ~~Add RebornLater strategy - is it the same as NoReborn?  Stop right at reborn point & save souls?~~
# 14) ~~RebornAndFreeze strategy~~
# 10) ~~edit hg strategy~~
# 11B) ~~save hg strategy~~
# 10A) ~~edit widget for hg strategy~~
# 7) ~~gold discount class, refactor~~
# 9) ~~army column for hg strategy~~
# 2) ~~add available souls to hero info~~
# 11A) ~~load hg strategy~~
