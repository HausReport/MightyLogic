

class HighestGrowth():

    def __init__(self, army):
        self.army = army
        self.locked = set()
        self.forced = set()
        self.rarities = [True, True, True, True]

    def lockHero(self, *heroes):
        for hero in heroes:
            self.locked.add(hero)

    def forceHero(self, *heroes):
        for hero in heroes:
            self.forced.add(hero)

    def toggleRarity(self, rarity):
        self.rarities[rarity] = not self.rarities[rarity]

    def setRarity(self, rarity):
        self.rarities[rarity] = True

    def unsetRarity(self, rarity):
        self.rarities[rarity] = False
