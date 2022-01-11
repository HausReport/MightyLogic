

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