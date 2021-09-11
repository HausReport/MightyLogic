from MightyLogic.Rewards.Reward import Reward


class Tile:

    def __init__(self, name, row=0, column=0, value=0, common=0, rare=0, soul_dust=0, epic=0, gold=0, legendary=0,
                 contrib=0, influence=0, spark=0, gem=0, building=False):
        self.name = name
        self.row = row
        self.column = column
        self.building = building
        # myName = "", value = 0, common = 0, rare = 0, soul_dust = 0, epic = 0, gold = 0, legendary = 0, contrib = 0, influence = 0,
        # spark = 0, gem = 0):
        self.reward = Reward(value, common, rare, soul_dust, epic, gold, legendary, contrib, influence, spark, gem)
        # print("world")

    def combineRewards(self, o):
        return self.reward.combine(o.gems)

    def combine(self, o):
        name = self.name + ", " + o.name
        row = "Z"
        column = 99
        rew = self.combineRewards(o)
        ret = Tile(name, row, column, value=0, common=0, rare=0, soul_dust=0, epic=0, gold=0, legendary=0, contrib=0, influence=0, spark=0, gem=0, building=False)
        ret.reward = rew
        return ret

    def getValue(self):
        return self.reward.myValue

    def setRow(self, row):
        self.row = row

    def setColumn(self, column):
        self.column = column

    def share(self, percent):
        if self.reward is None:
            return "ERROR: Undefined reward"
        return self.reward.share(percent)

    def getLocation(self):
        return str(self.row) + ":" + str(self.column)

    def getMediumDescriptor(self):
        return self.getName() + " at " + self.getLocation()

    def getName(self):
        return self.name

    def payouts(self, ticks=False):
        ret = ""
        if ticks:
            ret = "```"
        ret += "Payouts for " + self.getLocation() + " " + self.name + "\n"
        ret += self.reward.payouts()
        ret += str(self.reward.INFLUENCE) + " guild influence"
        if ticks:
            ret += "```" + "\n"
        return ret

    def getTileLine(self):
        val = self.getValue()
        rew = self.share(.07)
        if self.name is None:
            self.name = "Unknown"
        if self.row is None:
            self.row = "?"
        if self.column is None:
            self.column = "?"
        return f"{self.row}-{self.column}: {self.name:11s} {val:>8,.0f}  {rew:>35s}, {self.reward.INFLUENCE:>4d} influence."

    def __str__(self):
        return f'Tile {self.name} at {self.row}:{self.column}'

    def __repr__(self):
        return f'Tile(name={self.name}, row={self.row}, column={self.column})'
