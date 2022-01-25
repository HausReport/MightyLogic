from MightyLogic.HighGrowth.Erlaed.Army import Army


class HighestGrowth:

    def __init__(self, army: Army):
        self.army = army
        self.locked = set()
        self.forced = set()
        self.rarities = [True, True, True, True]

    def lockHeroes(self, heroes):
        for hero in heroes:
            self.locked.add(hero)

    def forceHeroes(self, heroes):
        for hero in heroes:
            self.forced.add(hero)

    def toggleRarity(self, rarity):
        self.rarities[rarity] = not self.rarities[rarity]

    def setRarity(self, rarity):
        self.rarities[rarity] = True

    def unsetRarity(self, rarity):
        self.rarities[rarity] = False

    def _format_output(self, ret):
        ret = ret[['Name', 'Rarity', 'Cur Reborn', 'Cur Level', 'Reborn', 'Level', 'LevelUps', 'Cum Souls', 'Cum Gold',
                   'Troop Gain',
                   'Score']]
        ret = ret.rename(columns={"Cum Gold": "Gold"})
        ret["Total Gold"] = ret.Gold.cumsum()
        ret["Total Troop Gain"] = ret['Troop Gain'].cumsum()
        ret["Total LevelUps"] = ret['LevelUps'].cumsum()
        return ret

    def _filter(self, df, aFilter=None):

        aList = df.Name.tolist()
        if aFilter is None:
            return aList
        elif aFilter == "Working":
            working = [item for item in aList if item not in self.forced]
            working = [item for item in working if item not in self.locked]
            return working
        elif aFilter == "Forced":
            forced = [item for item in aList if item in self.forced]
            return forced
        elif aFilter == "Locked":
            locked = [item for item in aList if item in self.locked]
            return locked

    def getLegendaries(self, aFilter=None):
        tmp = self.army.getLegendaries()
        return self._filter(tmp, aFilter)

    def getEpics(self, aFilter=None):
        tmp = self.army.getEpics()
        return self._filter(tmp, aFilter)

    def getRares(self, aFilter=None):
        tmp = self.army.getRares()
        return self._filter(tmp, aFilter)

    def getCommons(self, aFilter=None):
        tmp = self.army.getCommons()
        return self._filter(tmp, aFilter)

    def hg_level(self, level_ups) -> int:
        if level_ups < 0:
            return 0
        elif level_ups > 13150:
            return 15
        else:
            tmp = [0, 10, 25, 50, 90, 160, 275, 450, 700, 1050, 1550, 2350, 3650, 5650, 8650, 13150, 999999]
            for i in range(0, 15):
                if tmp[i] <= level_ups < tmp[i + 1]:
                    return i

    def hg_gems(self, level_ups: int):
        finished_round = self.hg_level(level_ups)
        tmp = [0, 50, 100, 200, 350, 650, 1100, 1800, 3000, 4500, 7500, 12000, 19500, 30000, 45000, 67500]
        return sum(tmp[0:finished_round + 1])
