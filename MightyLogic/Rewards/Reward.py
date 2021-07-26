from MightyLogic.Values import Values


def append_value(ret, value, label):
    if value > 0:
        if ret != "":
            ret = ret + ", "
        ret = ret + f"{value:,.0f} {label}"
    return ret

# FIXME: name conflicts with name in Tile

class Reward:
    myValue = 0
    COMMON_SOUL = 0
    RARE_SOUL = 0
    SOUL_DUST = 0
    EPIC_SOUL = 0
    GOLD = 0
    LEGENDARY_SOUL = 0
    CONTRIBUTION = 0
    INFLUENCE = 0
    SPARK = 0
    GEM = 0

    def toDict(self):
        return {
            "value"         : self.myValue,
            "COMMON_SOUL"   : self.COMMON_SOUL,
            "RARE_SOUL"     : self.RARE_SOUL,
            "SOUL_DUST"     : self.SOUL_DUST,
            "EPIC_SOUL"     : self.EPIC_SOUL,
            "GOLD"          : self.GOLD,
            "LEGENDARY_SOUL": self.LEGENDARY_SOUL,
            "CONTRIBUTION"  : self.CONTRIBUTION,
            "INFLUENCE"     : self.INFLUENCE,
            "SPARK"         : self.SPARK,
            "GEM"           : self.GEM
        }

    def combine(self, o):
        common = self.COMMON_SOUL + o.COMMON_SOUL
        rare = self.RARE_SOUL + o.RARE_SOUL
        soul_dust = self.SOUL_DUST + o.SOUL_DUST
        epic = self.EPIC_SOUL + o.EPIC_SOUL
        gold = self.GOLD + o.GOLD
        legendary = self.LEGENDARY_SOUL + o.LEGENDARY_SOUL
        contrib = self.CONTRIBUTION + o.CONTRIBUTION
        influence = self.INFLUENCE + o.INFLUENCE
        spark = self.SPARK + o.SPARK
        gem = self.GEM + o.GEM
        myName = self.NAME + ", " + o.NAME
        return Reward(0, common, rare, soul_dust, epic, gold, legendary, contrib, influence, spark, gem, myName)

    def __init__(self, value=0, common=0, rare=0, soul_dust=0, epic=0, gold=0, legendary=0, contrib=0, influence=0,
                 spark=0, gem=0, myName=""):
        val = value
        if val == 0:
            val += Values.COMMON_SOUL * common
            val += Values.RARE_SOUL * rare
            val += Values.SOUL_DUST * soul_dust
            val += Values.EPIC_SOUL * epic
            val += Values.GOLD * gold
            val += Values.KILO_SOUL * 0
            val += Values.LEGENDARY_SOUL * legendary
            val += Values.CONTRIBUTION * contrib
            val += Values.INFLUENCE * influence
            val += Values.SPARK * spark
            val += Values.GEM * gem
        self.myValue = val

        self.NAME = myName
        self.COMMON_SOUL = common
        self.RARE_SOUL = rare
        self.SOUL_DUST = soul_dust
        self.EPIC_SOUL = epic
        self.GOLD = gold
        self.LEGENDARY_SOUL = legendary
        self.CONTRIBUTION = contrib
        self.INFLUENCE = influence
        self.SPARK = spark
        self.GEM = gem

    def payouts(self):
        ret = ""
        ret += "Place               Reward" + "\n"
        ret += "First               " + self.share(.07) + "\n"
        ret += "2nd                 " + self.share(.06) + "\n"
        ret += "3rd                 " + self.share(.05) + "\n"
        ret += "4-6                 " + self.share(.04) + "\n"
        ret += "7-11                " + self.share(.03) + "\n"
        ret += "12-25               " + self.share(.02) + "\n"
        ret += "26-44               " + self.share(.01) + "\n"
        return ret

    def share(self, percent, include_inf=False):
        ret = ""
        ret = append_value(ret, self.COMMON_SOUL * percent, "common souls")
        ret = append_value(ret, self.RARE_SOUL * percent, "rare souls")
        ret = append_value(ret, self.SOUL_DUST * percent, "soul dust")
        ret = append_value(ret, self.EPIC_SOUL * percent, "epic souls")
        ret = append_value(ret, self.GOLD * percent, "gold")
        ret = append_value(ret, self.LEGENDARY_SOUL * percent, "legendary souls")
        ret = append_value(ret, self.CONTRIBUTION * percent, "contribution")
        if include_inf:
            ret = append_value(ret,self.INFLUENCE * percent, "influence" )
        ret = append_value(ret, self.SPARK * percent, "sparks")
        ret = append_value(ret, self.GEM * percent, "gems")
        return ret

    def __str__(self):
        return self.share(1, True)

    def __repr__(self):
        return self.share(1, True)
