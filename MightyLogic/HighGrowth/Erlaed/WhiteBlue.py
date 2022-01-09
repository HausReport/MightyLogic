from Rarity import Rarity

from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity

class WhiteBlue(Rarity):
    def la(self):
        return 1 + 1

    def reborn_level(self, rb=0):
            if rb == 0:
                return 0
            elif rb == 1:
                return 11
            elif rb == 2:
                return 16
            elif rb == 3:
                return 21
            elif rb == 4:
                return 26
            elif rb == 5:
                return 999

    def to_ordinal(self, reborn, level):
        ret = 0
        if reborn == 0:
            ret = level - 1
            if ret > 11:
                ret = 11
        elif reborn == 1:
            ret = 11 + level - 2
            if ret > 16 + 11:
                ret = 16 + 11
        elif reborn == 2:
            ret = 11 + 16 + level - 3
            if ret > 11 + 16 + 21:
                ret = 6 + 11 + 21
        elif reborn == 3:
            ret = 11 + 16 + 21 + level - 4
            if ret > 11 + 16 + 21 + 26:
                ret = 11 + 16 + 21 + 26
        elif reborn == 4:
            ret = 6 + 11 + 16 + 21 + level - 5
            if ret > 11 + 16 + 21 + 26 + 31:
                ret = 11 + 16 + 21 + 2 + 31
        elif reborn == 5:
            ret = 999
        return ret

    def to_ordinal2(self, reborn, level):
        ret = 0
        if reborn == 0:
            ret = level - 1
        elif reborn == 1:
            ret = 11 + level - 2
        elif reborn == 2:
            ret = 11 + 16 + level - 3
        elif reborn == 3:
            ret = 11 + 16 + 21 + level - 4
        elif reborn == 4:
            ret = 11 + 16 + 21 + 26 + level - 5
        elif reborn == 5:
            ret = 999
        return ret