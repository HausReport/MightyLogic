import pandas
import pandas as pd

from MightyLogic.HighGrowth.Erlaed.PurpleGold import PurpleGold


class Epic(PurpleGold):

    def get_r0_tab(self) -> pandas.DataFrame:
        r0_tab_epic = pd.DataFrame([[1, 200, 60, 0, 0],
                                    [2, 230, 70, 15, 300],
                                    [3, 260, 80, 30, 600],
                                    [4, 290, 90, 45, 900],
                                    [5, 320, 100, 60, 1500],
                                    [6, 350, 110, 80, 1800],
                                    [7, 390, 128, 100, 2500],
                                    [8, 430, 146, 120, 4000],
                                    [9, 470, 164, 140, 5000],
                                    [10, 510, 182, 160, 6000],
                                    [11, 550, 200, 200, 7000],
                                    [12, 620, 242, 250, 9000],
                                    [13, 690, 284, 210, 11000],
                                    [14, 760, 326, 400, 13000],
                                    [15, 830, 368, 500, 16000],
                                    [16, 900, 410, 650, 19000],
                                    [17, 1020, 508, 900, 22000],
                                    [18, 1140, 606, 1100, 26000],
                                    [19, 1260, 704, 1350, 30000],
                                    [20, 1380, 802, 1800, 34000],
                                    [21, 1500, 900, 2300, 38000],
                                    [22, 1700, 1020, 3000, 42000],
                                    [23, 1900, 1140, 4000, 47000],
                                    [24, 2100, 1260, 5000, 52000],
                                    [25, 2300, 1380, 6300, 58000],
                                    [26, 2500, 1500, 8000, 65000],
                                    [27, 2665, 1599, 8200, 67000],
                                    [28, 2830, 1698, 8400, 70000],
                                    [29, 2995, 1997, 8650, 73000],
                                    [30, 3160, 1896, 8950, 77000],
                                    [31, 3325, 1995, 9300, 82000]],
                                   columns=['Level', 'Might', 'Troops', 'Souls', 'Gold'])

        r0_tab_epic['Gold'] = (r0_tab_epic['Gold'] * self.gold_discount)
        return r0_tab_epic

    def getMightBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 150
        elif reborn == 2:
            return 200 + 150
        elif reborn == 3:
            return 350 + 200 + 150
        elif reborn == 4:
            return 600 + 350 + 200 + 150
        elif reborn == 5:
            return 1000 + 600 + 350 + 200 + 150

    def getTroopBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 60
        elif reborn == 2:
            return 145 + 60
        elif reborn == 3:
            return 360 + 145 + 60
        elif reborn == 4:
            return 750 + 360 + 145 + 60
        elif reborn == 5:
            return 1350 + 750 + 360 + 145 + 60

    def sn(self, rb=0):
        if rb == 0:
            return 0
        elif rb == 1:
            return 230
        elif rb == 2:
            return 230 + 950
        elif rb == 3:
            return 230 + 950 + 3070
        elif rb == 4:
            return 230 + 950 + 3070 + 10520
        elif rb == 5:
            return 230 + 950 + 3070 + 10520 + 36820
