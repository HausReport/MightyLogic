from MightyLogic.Values import Values


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

    def __init__(self, name="", value=0, common=0, rare=0, soul_dust=0, epic=0, gold=0, legendary=0, contrib=0, influence=0,
                 spark=0, gem=0):
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

        self.NAME = name
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

    def append_value(self, ret, value, label):
        if value > 0:
            if ret is not "":
                ret = ret + ", "
            ret = ret + f"{value:,.0f} {label}"
        return ret

    def share(self, percent):
        ret = ""
        ret = self.append_value(ret, self.COMMON_SOUL * percent, "common souls")
        ret = self.append_value(ret, self.RARE_SOUL * percent, "rare souls")
        ret = self.append_value(ret, self.SOUL_DUST * percent, "soul dust")
        ret = self.append_value(ret, self.EPIC_SOUL * percent, "epic souls")
        ret = self.append_value(ret, self.GOLD * percent, "gold")
        ret = self.append_value(ret, self.LEGENDARY_SOUL * percent, "legendary souls")
        ret = self.append_value(ret, self.CONTRIBUTION * percent, "contribution")
        # ret = self.append_value(ret,self.INFLUENCE * percent, "gold" )
        ret = self.append_value(ret, self.SPARK * percent, "sparks")
        ret = self.append_value(ret, self.GEM * percent, "gems")
        return ret
