import sys
import matplotlib

from MightyUseful.FileIo import getArmy

matplotlib.use('Qt5Agg')

from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel
from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth

class MplCanvas(QWidget):

    def getInt(self, field):
        return str(self.row[field].values[0])

    def getIntLabel(self, field):
        return QLabel(self.getInt(field))

    def getStringLabel(self, field):
        return str(self.row[field].values[0])

    def setHero(self, row):
        self.row = row
        self.btn = QLabel(row['Name'].values[0])
        vbox = QGridLayout()
        vbox.addWidget(self.btn, 0, 0, 1, 4)

        vbox.addWidget(QLabel("Level:"), 1,0,1,1)
        vbox.addWidget(self.getIntLabel('Level'), 1,1,1,1)

        vbox.addWidget(QLabel("Reborn:"), 2,0,1,1)
        vbox.addWidget(self.getIntLabel('Reborns'), 2,1,1,1)

        vbox.addWidget(QLabel("Rarity:"), 3,0,1,1)
        vbox.addWidget(self.getIntLabel('Rarity'), 3,1,1,1)

        vbox.addWidget(QLabel("Gender:"), 4,0,1,1)
        vbox.addWidget(self.getIntLabel('Gender'), 4,1,1,1)

        vbox.addWidget(QLabel("Alignment:"), 5,0,1,1)
        vbox.addWidget(self.getIntLabel('Alignment'), 5,1,1,1)

        vbox.addWidget(QLabel("Type:"), 6,0,1,1)
        vbox.addWidget(self.getIntLabel('Type'), 6,1,1,1)

        # TODO:
        # Evolves to
        # Evolves from
        # Possible Levelups

        self.setLayout(vbox)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.army = Army()
        getArmy(self, self.army)
        hg = HighestGrowth(self.army)

        row = self.army.lookup("Villano Mad Genius")
        sc = MplCanvas()
        sc.setHero(row) #width=5, height=4, dpi=100)
        self.setCentralWidget(sc)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()
