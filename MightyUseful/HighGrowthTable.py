import sys
import warnings

from PySide2.QtCore import Slot
from PySide2.QtGui import QTextDocument

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QPushButton, QTextBrowser
from jinja2 import Template, Environment, PackageLoader

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.IoGui import IoGui
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity


def add_comma(i):
    return '{:,}'.format(i)


def meta_score_to_letter_grade(meta_score):
    if meta_score > 158:
        return "A+"
    elif meta_score > 100:
        return "A"
    elif meta_score > 90:
        return "A-"
    elif meta_score > 80:
        return "B"
    elif meta_score > 70:
        return "C"
    elif meta_score > 60:
        return "D"
    elif meta_score > 50:
        return "D-"
    else:
        return "F"


class HighGrowthTable(QWidget):

    def __init__(self, aParent):
        #
        # UI stuff
        #
        super().__init__()
        self.myLayout = QVBoxLayout()
        self.setLayout(self.myLayout)
        self.hgt = aParent

        #
        # Get Army/HG Classes
        #
        self.army = Army()
        IoGui.getArmy(self, self.army)
        self.hg = HighestGrowth(army=self.army)

        self.TROOP_LIMIT =  14_050
        self.GOLD_LIMIT  =  2_700_000
        self.SCORE_LIMIT = -1 # 50
        self.STOP_HG_AT  = -1 # 950
        self.LEVELUP_LIMIT = -1 # 1300

        #
        # Get base HG dataframe
        #
        hg_file = IoGui.get_high_growth_file()
        if hg_file is not None:
            ret: pd.DataFrame = pd.read_csv(hg_file)
        else:
            ret: pd.DataFrame = self.run_high_growth()

        ret = self.bells_and_whistles(ret)
        html = self.df_to_html(ret)

        #
        self.text_browser = QTextBrowser()
        self.text_browser.setSearchPaths(["../MightyLogic/image/"])
        self.text_browser.setText(html)
        self.myLayout.addWidget(self.text_browser)
        # print(ret.to_string(max_cols=None))

    def find(self, text, flag):
        #flag = QTextDocument.FindBackward
        #print(self.text_browser.toHtml(), self.text_browser.find(text, flag))
        self.text_browser.find(text, flag)

    def rerun_high_growth(self):
        ret: pd.DataFrame = self.run_high_growth()  # note: saves to file also
        ret = self.bells_and_whistles(ret)
        html = self.df_to_html(ret)
        self.text_browser.setText(html)

    def run_high_growth(self):
        army2 = Army()
        army2.data_frame = self.army.data_frame.copy(deep=True)
        allMoves = pd.DataFrame()

        self.hgt.percent_done(0)
        floor = 90
        while floor >= 50:
            print("Floor is " + str(floor))
            holder = pd.DataFrame()
            for index, row in army2.data_frame.iterrows():
                aMove = self.hg.get_most_efficient_move(row)  # HERE row is a series
                if aMove is not None and len(aMove) > 0:
                    if (aMove.Score.values[0]) > floor:
                        holder = holder.append(aMove)
            if len(holder) > 0:
                allMoves = allMoves.append(holder)
                print("\t # moves is " + str(len(holder)))
                army2 = army2.patch(holder)
                # finish with the current floor to look for better moves
            else:
                if 0 < self.GOLD_LIMIT < allMoves['Cum Gold'].sum():
                    break
                floor = floor - 10  # * 0.8
                self.hgt.percent_done(90 - ((9.0/4.0) * (floor - 50)) )

        allMoves.sort_values(by='Score', ascending=False, inplace=True)
        if self.SCORE_LIMIT > 0:
            allMoves = allMoves[allMoves['Score'] > self.SCORE_LIMIT]
        allMoves = allMoves.copy(deep=True)
        allMoves = allMoves.reset_index()
        #
        # FIXME: THIS IS IN THE BALLPARK OF WORKING, BUT...
        # 1) 'Strategy' isn't available without a join
        # 2) You're dropping rows after the stop criteria has been met, meaning there might not be sufficient rows
        #
        # if self.STOP_HG_AT > 0:
        #     #allMoves = allMoves.reset_index()
        #     allMoves["Total LevelUps"] = allMoves['LevelUps'].cumsum()
        #     allMoves.drop( (  (allMoves['Total LevelUps'] > 600) & (allMoves['Strategy']=="HighGrowth")).index , inplace=True)
        #
        #
        #
        ret = self.hg._format_output(allMoves)

        hg_file = IoGui.get_high_growth_file(create=True)
        if hg_file is not None:
            ret.to_csv(hg_file, encoding='utf-8', index=False)
        return ret

    def bells_and_whistles(self, ret) -> pd.DataFrame:
        #
        # Add bells-n-whistles to dataframe
        #
        ret['GPT'] = ret['Gold'] / ret['Troop Gain']
        ret['GPL'] = ret['Gold'] / ret['LevelUps']
        ret['GPL'] = ret['GPL'].fillna(0)
        ret = ret.join(self.army.strats.set_index('Name'), on='Name')

        ret[['LevelUps']] = ret[['LevelUps']].astype('int')
        ret[['Gold']] = ret[['Gold']].astype('int')
        ret[['Score']] = ret[['Score']].astype('int')
        ret[['Total Gold']] = ret[['Total Gold']].astype('int')
        ret[['Total LevelUps']] = ret[['Total LevelUps']].astype('int')
        ret[['Total Troop Gain']] = ret[['Total Troop Gain']].astype('int')
        ret[['GPT']] = ret[['GPT']].astype('int')
        ret[['GPL']] = ret[['GPL']].astype('int')
        if self.TROOP_LIMIT > 0:
            firstHit =ret[ret['Total Troop Gain']> self.TROOP_LIMIT]
            firstHit = firstHit['Total Troop Gain'].min()
            ret = ret[ret['Total Troop Gain']<= firstHit]
        if self.LEVELUP_LIMIT > 0:
            firstHit =ret[ret['Total LevelUps']> self.LEVELUP_LIMIT]
            firstHit = firstHit['Total LevelUps'].min()
            ret = ret[ret['Total LevelUps']<= firstHit]
        if self.GOLD_LIMIT > 0:
            ret = ret[ret['Total Gold']< self.GOLD_LIMIT]
        self.hgt.table_changed(ret)
        return ret

    def df_to_html(self, ret) -> str:
        #
        # Convert dataframe to HTML
        #
        env = Environment(loader=PackageLoader('MightyUseful', 'templates'))
        tmpl = env.get_template("table2.html")

        formatted_df = ret.assign(
            Gold=lambda x: x['Gold'].map(add_comma),
            GPL=lambda x: x['GPL'].map(add_comma),
            GPT=lambda x: x['GPT'].map(add_comma),
            **{"Total Gold": lambda x: x['Total Gold'].map(add_comma)},
            **{"HighGrowthStage": lambda x: x['Total LevelUps'].map(HighestGrowth.hg_level)},
            **{"HighGrowthGems": lambda x: x['Total LevelUps'].map(HighestGrowth.hg_gems)},
            **{"Total LevelUps": lambda x: x['Total LevelUps'].map(add_comma)},
            **{"Total Troop Gain": lambda x: x['Total Troop Gain'].map(add_comma)},
            **{"Cum Souls": lambda x: x['Cum Souls'].map(add_comma)},
            **{"Icon": lambda x: x['Name'].map(self.army.local_icon_url)},
            **{"Letter Grade": lambda x: x['Score'].map(meta_score_to_letter_grade)},
            # Total_Gold=lambda x: x['Total Gold'].map(add_comma),
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
        return html

        # self.setCentralWidget(self.widget)
        # self.show()


