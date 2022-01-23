import os

from PySide2.QtCore import QRegExp, Qt, QSortFilterProxyModel
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QFormLayout, QLineEdit, QVBoxLayout
import sys
from PySide2.QtGui import QIcon
from PySide2 import QtWidgets


from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
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

        army = Army()
        print("BLABLA" + str(os.getcwd()))
        army.fromFile('../tests/Erlaed/test.csv')
        foo = army.getArmy()  # pd.read_csv('all.csv')
        hg = HighestGrowth(army)

        self.model = PandasModel(army.data_frame)
        self.proxy = MultiFilterProxyModel(self)
        #self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.table.setModel(self.proxy)
        self.table.setSortingEnabled(True)

        self.setCentralWidget(self.table)
        # flayout = QFormLayout()
        # self.layout().addChildLayout(flayout)   # addLayout(flayout)
        # for i in range(self.model.columnCount()):
        #     le = QLineEdit(self)
        #     flayout.addRow("column: {}".format(i), le)
        #     le.textChanged.connect(lambda text, col=i:
        #                            self.proxy.setFilterByColumn(QRegExp(text, Qt.CaseSensitive, QRegExp.FixedString),
        #                                                    col))
        #self.layout().addWidget(self.table)
        self.show()

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