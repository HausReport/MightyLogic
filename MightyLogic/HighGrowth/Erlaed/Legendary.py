import pandas
import pandas as pd

from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity


class Legendary(Rarity):

    def la(self):
        return 1 + 1

    def get_r0_tab(self) -> pandas.DataFrame:
        r0_tab = pd.DataFrame([[1, 350, 100, 0, 0],
                               [2, 390, 118, 5, 600],
                               [3, 430, 136, 10, 900],
                               [4, 470, 154, 15, 1400],
                               [5, 510, 172, 20, 1900],
                               [6, 550, 190, 40, 2500],
                               [7, 620, 228, 60, 3500],
                               [8, 690, 266, 80, 5500],
                               [9, 760, 304, 100, 7000],
                               [10, 830, 342, 120, 9000],
                               [11, 900, 380, 150, 11000],
                               [12, 1010, 470, 200, 14000],
                               [13, 1120, 560, 250, 17000],
                               [14, 1230, 650, 320, 20000],
                               [15, 1340, 740, 400, 24000],
                               [16, 1450, 830, 500, 28000],
                               [17, 1630, 1064, 700, 32000],
                               [18, 1810, 1298, 850, 36000],
                               [19, 1990, 1532, 1000, 40000],
                               [20, 2170, 1766, 1300, 44000],
                               [21, 2350, 2000, 1700, 48000],
                               [22, 2630, 2300, 2200, 52000],
                               [23, 2910, 2600, 2900, 57000],
                               [24, 3190, 2900, 3700, 62000],
                               [25, 3470, 3200, 4800, 68000],
                               [26, 3750, 3500, 6000, 75000],
                               [27, 3998, 3731, 6150, 80000],
                               [28, 4246, 3962, 6300, 86000],
                               [29, 4494, 4193, 6450, 93000],
                               [30, 4742, 4424, 6650, 101000],
                               [31, 4990, 4655, 6900, 110000]], columns=['Level', 'Might', 'Troops', 'Souls', 'Gold'])

        r0_tab['Gold'] = (r0_tab['Gold'] * self.gold_discount)
        return r0_tab

    def getMightBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 200
        elif reborn == 2:
            return 200 + 350
        elif reborn == 3:
            return 200 + 350 + 600
        elif reborn == 4:
            return 200 + 350 + 600 + 1200
        elif reborn == 5:
            return 200 + 350 + 600 + 1200 + 1700

    def getTroopBonus(self, reborn):
        if reborn == 0:
            return 0
        elif reborn == 1:
            return 102
        elif reborn == 2:
            return 102 + 268
        elif reborn == 3:
            return 102 + 268 + 751
        elif reborn == 4:
            return 102 + 268 + 751 + 1583
        elif reborn == 5:
            return 102 + 268 + 751 + 1583 + 2957

    def sn(self, rb=0):
        if rb == 0:
            return 0
        elif rb == 1:
            return 90
        elif rb == 2:
            return 600 + 90
        elif rb == 3:
            return 2270 + 600 + 90
        elif rb == 4:
            return 7820 + 2270 + 600 + 90
        elif rb == 5:
            return 27420 + 7820 + 2270 + 600 + 90

    def reborn_level(self, rb=0):
            if rb == 0:
                return 0
            elif rb == 1:
                return 6
            elif rb == 2:
                return 11
            elif rb == 3:
                return 16
            elif rb == 4:
                return 21
            elif rb == 5:
                return 26

    def to_ordinal(self, reborn, level):
        ret = 0
        if reborn == 0:
            ret = level - 1
            if ret > 6:
                ret = 6
        elif reborn == 1:
            ret = 6 + level - 2
            if ret > 6 + 11:
                ret = 6 + 11
        elif reborn == 2:
            ret = 6 + 11 + level - 3
            if ret > 6 + 11 + 16:
                ret = 6 + 11 + 16
        elif reborn == 3:
            ret = 6 + 11 + 16 + level - 4
            if ret > 6 + 11 + 16 + 21:
                ret = 6 + 11 + 16 + 21
        elif reborn == 4:
            ret = 6 + 11 + 16 + 21 + level - 5
            if ret > 6 + 11 + 16 + 21 + 26:
                ret = 6 + 11 + 16 + 21 + 26
        elif reborn == 5:
            ret = 6 + 11 + 16 + 21 + 26 + level - 6
            if ret > 6 + 11 + 16 + 21 + 31:
                ret = 6 + 11 + 16 + 21 + 31
        return ret

    def to_ordinal2(self, reborn, level):
        ret = 0
        if reborn == 0:
            ret = level - 1
        elif reborn == 1:
            ret = 6 + level - 2
        elif reborn == 2:
            ret = 6 + 11 + level - 3
        elif reborn == 3:
            ret = 6 + 11 + 16 + level - 4
        elif reborn == 4:
            ret = 6 + 11 + 16 + 21 + level - 5
        elif reborn == 5:
            ret = 6 + 11 + 16 + 21 + 26 + level - 6
        return ret
