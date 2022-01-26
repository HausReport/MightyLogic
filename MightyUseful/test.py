import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QFormLayout, QVBoxLayout, QWidget, \
    QCheckBox, QGroupBox, QHBoxLayout, QFileDialog, QSplitter, QPushButton, QSizePolicy

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.Datafile import get_data_file
from MightyUseful.FileIo import getArmy
from MightyUseful.MultiFilterProxyModel import MultiFilterProxyModel
from MightyUseful.PandasModel import PandasModel
from TestHeroInfo import MplCanvas


class Window(QMainWindow):

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
        getArmy(self, self.army)
        hg = HighestGrowth(self.army)

        self.model = PandasModel(self.army.data_frame)
        self.proxy = MultiFilterProxyModel(self)
        # self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.clicked.connect(self.func_test)
        self.table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

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

        # form.setLayout(formLayout)
        leftWidget = QWidget()
        leftWidgetLayout = QVBoxLayout()

        horizontalFilterBox.setLayout(horizontalFilterBoxLayout)
        leftWidgetLayout.addWidget(horizontalFilterBox)
        leftWidgetLayout.addWidget(self.table)
        leftWidget.setLayout(leftWidgetLayout)
        # vbox.addWidget(form)

        self.splitter = QSplitter(self, Qt.Horizontal)
        self.splitter.addWidget(leftWidget)

        # self.btn = QPushButton("Hi")
        # self.btn.setMinimumHeight(1000)
        # splitter.addWidget(self.btn)
        self.heroInfo = MplCanvas()
        self.heroInfo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.splitter.addWidget(self.heroInfo)

        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        wholeUiWidgetLayout.addWidget(self.splitter)
        wholeUiWidget.setLayout(wholeUiWidgetLayout)
        self.setCentralWidget(wholeUiWidget)
        self.show()
        self.setHeroByName("Charon, Soul Catcher")

    def func_test(self, item):
        sf = "You clicked on {0}x{1}".format(item.column(), item.row())
        print(sf)
        print(type(item))
        # mod: QAbstractItemModel = item.model()
        foo = self.proxy.index(item.row(), 1, item)
        bar = self.proxy.data(foo, Qt.DisplayRole)
        self.setHeroByName(bar)
        # self.btn.setText(bar)

    def setHeroByName(self, aName):
        hero = self.army.lookup(aName)
        if hero is None:
            print("Bad hero name: " + aName)
        else:
            newHeroInfo = MplCanvas()
            newHeroInfo.setHero(hero, self.army)
            self.splitter.replaceWidget(1, newHeroInfo)
            self.heroInfo = newHeroInfo
            print(hero)
        hero = self.army.lookup(aName)
        if hero is None:
            print("Bad hero name: " + aName)
        else:
            newHeroInfo = MplCanvas()
            newHeroInfo.setHero(hero, self.army)
            self.splitter.replaceWidget(1, newHeroInfo)
            self.heroInfo = newHeroInfo
            print(hero)

    def checkBoxChange(self, state):
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

    def create_menu(self):
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
window = Window()
myApp.exec_()
sys.exit(0)


# TODO:
# 1) add tabs
# 3) add "can level up"
# 4) add "can reborn"
# 5) tab for army analysis
# 6) tab for high growth
# 8) gold discount ui
# 12) load discounts
# 13) Score - see Hanzo Sama case, lots of levels similar score to 1 level.  See also spreadsheet


# 10) ~~edit hg strategy~~
# 11B) ~~save hg strategy~~
# 10A) ~~edit widget for hg strategy~~
# 7) ~~gold discount class, refactor~~
# 9) ~~army column for hg strategy~~
# 2) ~~add available souls to hero info~~
# 11A) ~~load hg strategy~~
