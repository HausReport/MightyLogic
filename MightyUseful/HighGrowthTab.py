import sys

from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QPushButton

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.IoGui import IoGui
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity

class Window(QMainWindow):

        def __init__(self):
            super().__init__()

            #self.setLayout(QVBoxLayout())
            self.setWindowTitle("MightyUseful")
            self.setGeometry(300, 300, 500, 400)

            self.widget = QWidget()
            self.myLayout = QVBoxLayout()
            self.widget.setLayout(self.myLayout)
            btn = QPushButton("Hi")
            self.myLayout.addWidget(btn)

            self.army = Army()
            IoGui.getArmy(self, self.army)

            hg = HighestGrowth(army=self.army)
            gremory = self.army.lookup("Gremory Night Child")
            # leg: Rarity = Rarity.get_rarity_by_name("Legendary")
            #moves = hg.get_moves(gremory)
            moves = hg.get_most_efficient_move(gremory)
            print(moves.to_string(max_cols=None))

            self.setCentralWidget(self.widget)
            # self.showMaximized()
            # self.showFullScreen()
            self.show()



myApp = QApplication(sys.argv)
window = Window()
myApp.exec_()
sys.exit(0)