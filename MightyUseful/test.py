import sys

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QFormLayout, QVBoxLayout, QWidget, \
    QCheckBox, QGroupBox, QHBoxLayout, QFileDialog, QSplitter, QPushButton

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.Datafile import get_data_file
from MightyUseful.FileIo import getArmy
from MightyUseful.MultiFilterProxyModel import MultiFilterProxyModel
from MightyUseful.PandasModel import PandasModel




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
#'../tests/Erlaed/test.csv')
        # foo = army.getArmy()  # pd.read_csv('all.csv')
        hg = HighestGrowth(self.army)

        self.model = PandasModel(self.army.data_frame)
        self.proxy = MultiFilterProxyModel(self)
        # self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)
        self.table.clicked.connect(self.func_test)

        thang = QWidget()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        horiz = QWidget()
        form = QWidget()
        formLayout = QFormLayout()

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
        hbox.addWidget(alignmentBox)

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
        hbox.addWidget(genderBox)

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
        hbox.addWidget(typeBox)

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
        hbox.addWidget(rarityBox)

        form.setLayout(formLayout)

        horiz.setLayout(hbox)
        vbox.addWidget(horiz)
        vbox.addWidget(form)

        splitter = QSplitter(self, Qt.Horizontal)
        splitter.addWidget(self.table)
        self.btn = QPushButton("Hi")
        self.btn.setMinimumHeight(1000)
        splitter.addWidget(self.btn)
        vbox.addWidget(splitter)
        thang.setLayout(vbox)
        self.setCentralWidget(thang)
        self.show()

    def func_test(self, item):
        sf = "You clicked on {0}x{1}".format(item.column(), item.row())
        print(sf)
        print(type(item))
        # mod: QAbstractItemModel = item.model()
        foo = self.proxy.index(item.row(), 1, item)
        bar = self.proxy.data(foo, Qt.DisplayRole)
        self.btn.setText(bar)
        print(self.army.lookup(bar))
        # idx = QModelIndex(1, item.row())
        # print(idx)
        # print(mod.data())I
        # print(mod.data(1, item.row()))

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
