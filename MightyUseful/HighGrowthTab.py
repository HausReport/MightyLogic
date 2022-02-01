import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QPushButton
from jinja2 import Template, Environment, PackageLoader

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.IoGui import IoGui
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity

def add_comma(i):
    return '{:,}'.format(i)

class Window(QMainWindow):

        def __init__(self):
            super().__init__()
            GOLD_LIMIT = 2_750_000

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

            self.hg = HighestGrowth(army=self.army)
            gremory = self.army.lookup("Gremory Night Child")
            # leg: Rarity = Rarity.get_rarity_by_name("Legendary")
            #moves = hg.get_moves(gremory)

            hg_file = IoGui.get_high_growth_file()
            if hg_file is not None:
                ret: pd.DataFrame = pd.read_csv(hg_file)
            else:
                army2 = Army()
                army2.data_frame = self.army.data_frame.copy(deep=True)
                allMoves = pd.DataFrame()

                floor = 90
                while floor >= 50:
                    print("Floor is " + str(floor))
                    holder = pd.DataFrame()
                    for index, row in army2.data_frame.iterrows():
                        aMove = self.hg.get_most_efficient_move(row)     # HERE row is a series
                        if aMove is not None and len(aMove)> 0:
                            if (aMove.Score.values[0]) > floor:
                                holder = holder.append(aMove)
                    if len(holder) > 0:
                        allMoves = allMoves.append(holder)
                        print("\t # moves is " + str(len(holder)))
                        army2 = army2.patch(holder)
                        # finish with the current floor to look for better moves
                    else:
                        if allMoves['Cum Gold'].sum() > GOLD_LIMIT:
                            break
                        floor = floor -10 #* 0.8
                #moves = hg.get_most_efficient_move(gremory)
                #print(moves.to_string(max_cols=None))

                allMoves.sort_values(by='Score', ascending=False, inplace=True)
                allMoves = allMoves[allMoves['Score'] > 50.0].copy(deep=True)
                allMoves = allMoves.copy(deep=True)
                ret = self.hg._format_output(allMoves)
                #ret = allMoves

                hg_file = IoGui.get_high_growth_file(create=True)
                if hg_file is not None:
                    ret.to_csv(hg_file, encoding='utf-8', index=False)

            print(ret.to_string(max_cols=None))
            self.setCentralWidget(self.widget)
            # self.showMaximized()
            # self.showFullScreen()
            self.show()

            ret['GPT'] = ret['Gold'] / ret['Troop Gain']
            ret['GPL'] = ret['Gold'] / ret['LevelUps']
            ret['GPL'] = ret['GPL'].fillna(0)
            ret = ret.join(self.army.strats.set_index('Name'), on='Name')

            # ret['icon'] =

            ret[['LevelUps']] = ret[['LevelUps']].astype('int')
            ret[['Gold']] = ret[['Gold']].astype('int')
            ret[['Score']] = ret[['Score']].astype('int')
            ret[['Total Gold']] = ret[['Total Gold']].astype('int')
            ret[['Total LevelUps']] = ret[['Total LevelUps']].astype('int')
            ret[['Total Troop Gain']] = ret[['Total Troop Gain']].astype('int')
            ret[['GPT']] = ret[['GPT']].astype('int')
            ret[['GPL']] = ret[['GPL']].astype('int')

            env = Environment(loader=PackageLoader('MightyUseful', 'templates'))
            tmpl = env.get_template("table2.html")

            formatted_df = ret.assign(
                Gold=lambda x: x['Gold'].map(add_comma),
                GPL=lambda x: x['GPL'].map(add_comma),
                GPT=lambda x: x['GPT'].map(add_comma),
                **{"Total Gold": lambda x: x['Total Gold'].map(add_comma)},
                **{"Total LevelUps": lambda x: x['Total LevelUps'].map(add_comma)},
                **{"Total Troop Gain": lambda x: x['Total Troop Gain'].map(add_comma)},
                **{"Cum Souls": lambda x: x['Cum Souls'].map(add_comma)},
                **{"Icon": lambda x: x['Name'].map(self.army.icon_url)},
                #Total_Gold=lambda x: x['Total Gold'].map(add_comma),
            )
            formatted_df = formatted_df.reindex()
            formatted_df['no'] = formatted_df.index + 1
            html = tmpl.render(
                rows=formatted_df.to_dict(orient='records'),
                columns=formatted_df.columns.to_list()
            )
            print(html)
            with open("my_new_file.html", "w") as fh:
                fh.write(html)

myApp = QApplication(sys.argv)
window = Window()
myApp.exec_()
sys.exit(0)