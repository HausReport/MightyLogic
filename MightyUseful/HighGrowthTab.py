import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
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

            army2 = Army()
            army2.data_frame = self.army.data_frame.copy(deep=True)
            allMoves = pd.DataFrame()

            floor = 90
            while floor >= 50:
                print("Floor is " + str(floor))
                holder = pd.DataFrame()
                for index, row in army2.data_frame.iterrows():
                    aMove = hg.get_most_efficient_move(row)
                    if aMove is not None and len(aMove)> 0:
                        if (aMove.Score.values[0]) > floor:
                            holder = holder.append(aMove)
                if len(holder) > 0:
                    allMoves = allMoves.append(holder)
                    print("\t # moves is " + str(len(holder)))
                    army2 = army2.patch(holder)
                else:
                    floor = floor -10 #* 0.8
            #moves = hg.get_most_efficient_move(gremory)
            #print(moves.to_string(max_cols=None))

            allMoves.sort_values(by='Score', ascending=False, inplace=True)
            allMoves = allMoves[allMoves['Score'] > 50.0].copy(deep=True)
            allMoves = allMoves.copy(deep=True)
            ret = hg._format_output(allMoves)
            #ret = allMoves
            print(ret.to_string(max_cols=None))

            self.setCentralWidget(self.widget)
            # self.showMaximized()
            # self.showFullScreen()
            self.show()



myApp = QApplication(sys.argv)
window = Window()
myApp.exec_()
sys.exit(0)