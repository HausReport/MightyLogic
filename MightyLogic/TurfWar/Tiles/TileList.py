from MightyLogic.Rewards.Reward import Reward
from MightyLogic.TurfWar.Tiles.Tile import Tile


class TileList:

    # coordanates like [['A', 1], ['B', 1], ['C', 1]]
    def __init__(self, amap, coordList):
        self.amap = amap
        self.tiles = self.getTiles(coordList)
        print("In constructor")

    def getTiles(self, args):
        ret = []
        for arg in args:
            ret.append(self.amap.getTile(arg[0], arg[1]))
        return ret

    def getName(self):
        ret = ""
        tile: Tile
        for tile in self.tiles:
            if tile is None:
                print("getName(): None tile")
                continue
            if len(ret) > 0:
                ret += ", "
            ret += tile.getMediumDescriptor()
        return ret

    def getValue(self):
        ret = 0
        for tile in self.tiles:
            ret += tile.getValue()
        return ret

    def getRewards(self):
        rew = Reward(myName="Combo")
        for tile in self.tiles:
            print(tile.reward)
            rew = rew.combine(tile.reward)
        return rew

    def payouts(self):
        ret = ""
        ret += "Payouts for " + self.getName() + "\n"
        #ret += "Payouts for " + self.getLocation() + " " + self.name + "\n"
        rewards = self.getRewards()
        ret += rewards.payouts()
        return ret
