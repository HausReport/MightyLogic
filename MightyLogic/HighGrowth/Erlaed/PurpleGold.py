from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity


class PurpleGold(Rarity):
    def la(self):
        return 1 + 1

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
        if reborn == 0:
            if level > 6:
                return self.to_ordinal(0, 6)
            else:
                return level - 1
        elif reborn == 1:
            if level > 11:
                return self.to_ordinal(1, 11)
            else:
                return level - 1 + self.to_ordinal(0, 6)
        elif reborn == 2:
            if level > 16:
                return self.to_ordinal(2, 16)
            else:
                return level - 1 + self.to_ordinal(1, 11)
        elif reborn == 3:
            if level > 21:
                return self.to_ordinal(3, 21)
            else:
                return level - 1 + self.to_ordinal(2, 16)
        elif reborn == 4:
            if level > 26:
                return self.to_ordinal(4, 26)
            else:
                return level - 1 + self.to_ordinal(3, 21)
        elif reborn == 5:
            if level > 31:
                return self.to_ordinal(5, 31)
            else:
                return level - 1 + self.to_ordinal(4, 26)

    def to_ordinal2(self, reborn, level):
        if reborn == 0:
            return level - 1
        elif reborn == 1:
            return level - 1 + self.to_ordinal(0, 6)
        elif reborn == 2:
            return level - 1 + self.to_ordinal(1, 11)
        elif reborn == 3:
            return level - 1 + self.to_ordinal(2, 16)
        elif reborn == 4:
            return level - 1 + self.to_ordinal(3, 21)
        elif reborn == 5:
            return level - 1 + self.to_ordinal(4, 26)

    def get_reborn_1_point(self, df, rb=1):
        return self._get_reborn_point(df, rb, 6, 11, 16, 21, 26)

    def has_reborn_1(self, df, rb=1):
        return self._has_reborn_1(df, rb, 6, 11, 16, 21, 26)
