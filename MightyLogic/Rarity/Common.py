import pandas
import pandas as pd

from Rarity.WhiteBlue import WhiteBlue


class Common(WhiteBlue):

    def getName(self) -> str:
        return "Common"

    def get_r0_tab(self) -> pandas.DataFrame:
        r0_tab_epic = pd.DataFrame([[1, 100, 20, 0, 0],
                                    [2, 110, 22, 25, 50],
                                    [3, 120, 24, 50, 80],
                                    [4, 130, 26, 75, 120],
                                    [5, 140, 28, 100, 200],
                                    [6, 150, 30, 150, 300],
                                    [7, 170, 34, 200, 500],
                                    [8, 190, 38, 250, 1000],
                                    [9, 210, 42, 300, 1500],
                                    [10, 230, 46, 350, 2000],
                                    [11, 250, 50, 450, 3000],
                                    [12, 280, 58, 600, 4000],
                                    [13, 310, 66, 750, 6000],
                                    [14, 340, 74, 900, 8000],
                                    [15, 370, 82, 1100, 10000],
                                    [16, 400, 90, 1400, 13000],
                                    [17, 450, 106, 2000, 16000],
                                    [18, 500, 122, 2700, 19000],
                                    [19, 550, 138, 3500, 22000],
                                    [20, 600, 154, 4500, 25000],
                                    [21, 650, 170, 6000, 28000],
                                    [22, 750, 186, 7500, 32000],
                                    [23, 850, 202, 9500, 36000],
                                    [24, 950, 218, 12000, 40000],
                                    [25, 1050, 234, 15000, 45000],
                                    [26, 1150, 250, 18000, 50000]],
                                   columns=['Level', 'Might', 'Troops', 'Souls', 'Gold'])

        r0_tab_epic['Gold'] = (r0_tab_epic['Gold'] * self.discounts.get_gold_discount())
        return r0_tab_epic

    def getMightBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 100
        elif reborn == 2:
            return 150 + 100
        elif reborn == 3:
            return 250 + 150 + 100
        elif reborn == 4:
            return 500 + 250 + 150 + 100
        elif reborn == 5:
            return -1000

    def getTroopBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 24
        elif reborn == 2:
            return 48 + 24
        elif reborn == 3:
            return 85 + 48 + 24
        elif reborn == 4:
            return 150 + 85 + 48 + 24
        elif reborn == 5:
            return -1000

    def souls_needed_to_reborn(self, rb=0):
        if rb == 0:
            return 0
        elif rb == 1:
            return 1950
        elif rb == 2:
            return 6700 + 1950
        elif rb == 3:
            return 24500 + 6700 + 1950
        elif rb == 4:
            return 87400 + 24500 + 6700 + 1950
        elif rb == 5:
            return 99999999
