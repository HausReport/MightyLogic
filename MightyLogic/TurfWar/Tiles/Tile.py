from MightyLogic.Rewards.Reward import Reward


class Tile:

    def __init__(self, name, row=0, column=0, value=0, common=0, rare=0, soul_dust=0, epic=0, gold=0, legendary=0,
                 contrib=0, influence=0, spark=0, gem=0):
        self.name = name
        self.row = row
        self.column = column
        self.reward = Reward(value, common, rare, soul_dust, epic, gold, legendary, contrib, influence, spark, gem)
        # print("world")

    def setRow(self,row):
        self.row = row

    def setColumn(self, column):
        self.column = column

    def share(self, percent):
        self.reward.share(percent)

    def getLocation(self):
        return self.row + ":" + self.column

    def payouts(self):
        ret = "```"
        ret += "Payouts for " + self.getLocation() + " " + self.name
        ret += "Place               Reward"
        ret += "First               " + self.reward.share(.07)
        ret += "2nd                 " + self.reward.share(.06)
        ret += "3rd                 " + self.reward.share(.05)
        ret += "4-6                 " + self.reward.share(.04)
        ret += "7-11                " + self.reward.share(.03)
        ret += "12-25               " + self.reward.share(.02)
        ret += "26-44               " + self.reward.share(.01)
        ret += "```"
        return ret
