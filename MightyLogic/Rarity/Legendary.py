import pandas
import pandas as pd

from Rarity.PurpleGold import PurpleGold


class Legendary(PurpleGold):

    def getName(self) -> str:
        return "Legendary"

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

        r0_tab['Gold'] = (r0_tab['Gold'] * self.discounts.get_gold_discount())
        return r0_tab

    def getMightBonus(self, reborn: int = 0):
        if reborn < 0:
            return 0
        elif reborn > 5:
            return 0
        tmp = [0, 200, 400, 600, 1200, 1700]
        return sum(tmp[:reborn + 1])

    def getTroopBonus(self, reborn: int = 0):
        if reborn < 0:
            return 0
        elif reborn > 5:
            return 0
        tmp = [0, 102, 268, 751, 1583, 2957]
        return sum(tmp[:reborn + 1])

    def souls_needed_to_reborn(self, reborn: int = 0):
        if reborn < 0:
            return 0
        elif reborn > 5:
            return 0
        tmp = [0, 90, 600, 2770, 7820, 27420]
        return sum(tmp[:reborn + 1])
