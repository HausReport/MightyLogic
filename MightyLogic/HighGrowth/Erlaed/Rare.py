import pandas
import pandas as pd

from MightyLogic.HighGrowth.Erlaed.WhiteBlue import WhiteBlue

class Rare(WhiteBlue):

    def get_r0_tab(self) -> pandas.DataFrame:
        r0_tab_epic = pd.DataFrame([[1, 120, 25, 0, 0],
                                    [2, 135, 28, 25, 100],
                                    [3, 150, 31, 50, 300],
                                    [4, 170, 34, 75, 600],
                                    [5, 185, 37, 100, 900],
                                    [6, 200, 40, 130, 1400],
                                    [7, 230, 46, 160, 2000],
                                    [8, 260, 52, 190, 3500],
                                    [9, 290, 58, 220, 4000],
                                    [10, 320, 64, 250, 5000],
                                    [11, 350, 70, 330, 6000],
                                    [12, 400, 82, 420, 8000],
                                    [13, 450, 94, 500, 10000],
                                    [14, 500, 106, 600, 12000],
                                    [15, 550, 118, 750, 14000],
                                    [16, 600, 130, 950, 16000],
                                    [17, 680, 156, 1400, 19000],
                                    [18, 760, 182, 1900, 22000],
                                    [19, 840, 208, 2400, 25000],
                                    [20, 920, 234, 3000, 28000],
                                    [21, 1000, 260, 3700, 32000],
                                    [22, 1140, 288, 4500, 36000],
                                    [23, 1280, 316, 5500, 40000],
                                    [24, 1420, 344, 7000, 45000],
                                    [25, 1560, 372, 9000, 50000],
                                    [26, 1700, 400, 12000, 55000],
                                    [27, 1812, 426, 12150, 57000],
                                    [28, 1924, 452, 12350, 60000],
                                    [29, 2036, 478, 12550, 63000],
                                    [30, 2148, 504, 12800, 66000],
                                    [31, 2260, 530, 13100, 70000]],
                                   columns=['Level', 'Might', 'Troops', 'Souls', 'Gold'])

        r0_tab_epic['Gold'] = (r0_tab_epic['Gold'] * self.gold_discount)
        return r0_tab_epic

    def getMightBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 150
        elif reborn == 2:
            return 250 + 150
        elif reborn == 3:
            return 400 + 250 + 150
        elif reborn == 4:
            return 700 + 400 + 250 + 150
        elif reborn == 5:
            return -1000

    def getTroopBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 42
        elif reborn == 2:
            return 88 + 42
        elif reborn == 3:
            return 168 + 88 + 42
        elif reborn == 4:
            return 320 + 168 + 88 + 42
        elif reborn == 5:
            return -1000

    def sn(self, rb=0):
        if rb == 0:
            return 0
        elif rb == 1:
            return 1530
        elif rb == 2:
            return 4750 + 1530
        elif rb == 3:
            return 17150 + 4750 + 1530
        elif rb == 4:
            return 55150 + 17150 + 4750 + 1530
        elif rb == 5:
            return 99999999
