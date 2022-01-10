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
        if reborn == 0:
            if level > 11:
                return self.to_ordinal(0, 11)
            else:
                return level - 1
        elif reborn == 1:
            if level > 16:
                return self.to_ordinal(1, 16)
            else:
                return level - 1 + self.to_ordinal(0, 11)
        elif reborn == 2:
            if level > 21:
                return self.to_ordinal(2, 21)
            else:
                return level - 1 + self.to_ordinal(1, 11)
        elif reborn == 3:
            if level > 26:
                return self.to_ordinal(3, 26)
            else:
                return level - 1 + self.to_ordinal(2, 21)
        elif reborn == 4:
            if level > 26:
                return self.to_ordinal(4, 26)
            else:
                return level - 1 + self.to_ordinal(3, 26)
        elif reborn == 5:
            if level > 31:
                return self.to_ordinal(5, 31)
            else:
                return level - 1 + self.to_ordinal(4, 26)

    def to_ordinal2(self, reborn, level):
        if reborn == 0:
            return level - 1
        elif reborn == 1:
            return level - 1 + self.to_ordinal(0, 11)
        elif reborn == 2:
            return level - 1 + self.to_ordinal(1, 16)
        elif reborn == 3:
            return level - 1 + self.to_ordinal(2, 21)
        elif reborn == 4:
            return level - 1 + self.to_ordinal(3, 26)
        elif reborn == 5:
            return level - 1 + self.to_ordinal(4, 31)
