import string

from MightyLogic.Rewards.Reward import Reward
from MightyLogic.TurfWar.Tiles.Tile import Tile


class TileList:

    # coordanates like [['A', 1], ['B', 1], ['C', 1]]
    def __init__(self, amap, coordList):
        self.amap = amap
        self.tiles = self.getTiles(coordList)
        self.value = self.getValue() # for sorting lists
        #print("In constructor")

    def getTiles(self, args):
        ret = []
        for arg in args:
            ret.append(self.amap.getTile(arg[0], arg[1]))
        return ret

    #
    # Informational output
    #
    def getCoordsString(self):
        ret = ""
        tile: Tile
        for tile in self.tiles:
            if ret != "":
                ret = ret + ", "
            ret = ret + tile.getLocation()
        return ret

    def getShortNameList(self):
        ret = []
        tile: Tile
        for tile in self.tiles:
            ret.append(tile.getLocation())
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

    def share(self, percent):
        rew = self.getRewards()
        return rew.share(percent)

    def getRewards(self):
        rew = Reward(myName="Combo")
        for tile in self.tiles:
            #print(tile.reward)
            rew = rew.combine(tile.reward)
        return rew

    def getTileLine(self):
        val = self.getValue()
        share = self.share(.07)
        loc = self.getCoordsString()
        rew = self.getRewards()
        #if self.name is None:
        #    self.name = "Unknown"
        return f"{loc}: {val:>8,.0f}  {share:>35s}, {rew.INFLUENCE:>4d} influence."

    def payouts(self, double=False):
        ret = ""
        ret += "Payouts for " + self.getName() + " "
        if double:
            ret += "(Sunday Double)"
        ret += "\n"
        #ret += "Payouts for " + self.getLocation() + " " + self.name + "\n"
        rewards = self.getRewards()
        if double:
            rewards = rewards.double()

        ret += rewards.payouts()
        return ret

    #
    # for removing redundant combos with sets
    #
    def __eq__(self, other):
        l1 = self.getShortNameList()
        l2 = other.getShortNameList()
        for aStr in l1:
            if aStr not in l2:
                return False
        for aStr in l2:
            if aStr not in l1:
                return False
        return True

    def __hash__(self):
        l1 = self.getShortNameList()
        l1.sort()
        srted = ""
        srted.join(l1)
        return hash(srted)