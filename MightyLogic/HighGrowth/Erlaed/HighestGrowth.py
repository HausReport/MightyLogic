

class HighestGrowth():

    def __init__(self, army):
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
        ret = ret[['Name', 'Cur Reborn', 'Cur Level', 'Reborn', 'Level', 'LevelUps', 'Cum Gold', 'Troop Gain', 'Score']]
        ret = ret.rename(columns={"Cum Gold": "Gold"})
        ret["Total Gold"] = ret.Gold.cumsum()
        ret["Total Troop Gain"] = ret['Troop Gain'].cumsum()
        ret["Total LevelUps"] = ret['LevelUps'].cumsum()
        return ret

    def _filter(self, aList, aFilter=None):
        if aFilter is None:
            return aList
        elif aFilter is "Working":
            working = [item for item in aList if item not in self.forced]
            working = [item for item in working if item not in self.locked]
            return working
        elif aFilter is "Forced":
            forced = [item for item in aList if item in self.forced]
            return forced
        elif aFilter is "Locked":
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