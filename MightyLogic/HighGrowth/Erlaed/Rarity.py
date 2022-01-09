from abc import ABC, abstractmethod


class Rarity(ABC):
    guild_discount = .8
    vip_discount = .88
    crisis_discount = .82
    # gold_discount = .8
    gold_discount = guild_discount * vip_discount * crisis_discount  # .66 # with crisis + guild

    @abstractmethod
    def sn(self, rb=0):
        pass

    @abstractmethod
    def get_r0_tab(self):
        pass

    def get_reborn_table(self, reborn):
        r0_tab = self.get_r0_tab()
        r0_tab["Reborn"] = 0

        if reborn == 0:
            return r0_tab

        tmp = r0_tab
        tmp = tmp.copy(deep=True)
        tmp["Reborn"] = reborn
        tmp["Might"] += self.getMightBonus(reborn)
        tmp["Troops"] += self.getTroopBonus(reborn)
        return tmp  # .copy(deep=True)

    @abstractmethod
    def getMightBonus(self, reborn):
        pass

    @abstractmethod
    def getTroopBonus(self, reborn):
        pass

    @abstractmethod
    def to_ordinal(self, reborn, level):
        pass

    @abstractmethod
    def to_ordinal2(self, reborn, level):
        pass

    @abstractmethod
    def sn(self, rb=0):
        pass

    @abstractmethod
    def reborn_level(self, rb=0):
        pass



    @abstractmethod
    def to_ordinal2(self, reborn, level):
        pass

    def level_dist(self, r0, l0, r1, l1):
        if r0 == r1:
            return l1 - l0

        o0 = self.to_ordinal(r0, l0)
        o1 = self.to_ordinal2(r1, l1)
        return o1 - o0

    def straight_level(self, level, reborn, avail_souls, avail_gold=-1):
        tab = self.get_reborn_table(reborn)
        tmp = tab.copy(deep=True)
        tmp['Reborn'] = reborn

        tmp = tmp[tmp.Level > level]
        tmp = tmp.copy(deep=True)
        tmp['Cum Souls'] = tmp.Souls.cumsum()
        tmp['Cum Gold'] = tmp.Gold.cumsum()
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        if avail_gold > 0:
            tmp = tmp[tmp['Cum Gold'] <= avail_gold]
        return tmp

    def get_tmp_table(self, total_souls, avail_souls, avail_gold, rb):
        print("Hi")
        (cs, cg) = (0, 0)  # do rebate here
        tmp = self.get_reborn_table(rb + 1).copy(deep=True)
        tmp.loc[0, 'Gold'] = cg
        tmp.loc[0, 'Souls'] = -1 * (total_souls - avail_souls - sn(rb + 1))

        tmp['Cum Souls'] = tmp.Souls.cumsum()
        tmp['Cum Gold'] = tmp.Gold.cumsum()
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        if avail_gold > 0:
            tmp = tmp[tmp['Cum Gold'] <= avail_gold]
        return tmp