from MightyLogic.Rewards.Reward import Reward


class Tile:

    def __init__(self, name, row=0, column=0, value=0, common=0, rare=0, soul_dust=0, epic=0, gold=0, legendary=0,
                 contrib=0, influence=0, spark=0, gem=0):
        self.name = name
        self.row = row
        self.column = column
        #myName = "", value = 0, common = 0, rare = 0, soul_dust = 0, epic = 0, gold = 0, legendary = 0, contrib = 0, influence = 0,
        #spark = 0, gem = 0):
        self.reward = Reward(value, common, rare, soul_dust, epic, gold, legendary, contrib, influence, spark, gem)
        # print("world")

    def setRow(self,row):
        self.row = row

    def setColumn(self, column):
        self.column = column

    def share(self, percent):
        self.reward.share(percent)

    def getLocation(self):
        return str(self.row) + ":" + str(self.column)

    def getName(self):
        return self.name

    def payouts(self):
        ret = "```"
        ret += "Payouts for " + self.getLocation() + " " + self.name + "\n"
        ret += "Place               Reward" + "\n"
        ret += "First               " + self.reward.share(.07) + "\n"
        ret += "2nd                 " + self.reward.share(.06) + "\n"
        ret += "3rd                 " + self.reward.share(.05) + "\n"
        ret += "4-6                 " + self.reward.share(.04) + "\n"
        ret += "7-11                " + self.reward.share(.03) + "\n"
        ret += "12-25               " + self.reward.share(.02) + "\n"
        ret += "26-44               " + self.reward.share(.01) + "\n"
        ret += "```" + "\n"
        return ret

    def __str__(self):
        return f'Tile {self.name} at {self.row}:{self.column}'

    def __repr__(self):
        return f'Tile(name={self.name}, row={self.row}, column={self.column})'
