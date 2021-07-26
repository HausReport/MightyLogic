from MightyLogic.Rewards.Reward import Reward


class TileList():

    # coordanates like [['A', 1], ['B', 1], ['C', 1]]
    def __init__(self, map, coordList):
        self.map = map
        self.tiles = self.getTiles(coordList)

    def getTiles(self, args):
        ret = []
        for arg in args:
            ret.append(self.map.getTile(arg[0], arg[1]))
        return ret

    def getRewards(self):
        rew = Reward(myName="Combo")
        for tile in self.tiles:
            rew = rew.combine(tile.reward)
        return rew

    def payouts(self):
        ret = ""
        ret += "Payouts for " + self.getLocation() + " " + self.name + "\n"
        rewards = self.getRewards()
        ret += rewards.payouts()
        return ret