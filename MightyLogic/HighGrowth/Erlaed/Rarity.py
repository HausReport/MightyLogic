from abc import ABC, abstractmethod


class Rarity(ABC):
    guild_discount = .8
    vip_discount = .88
    crisis_discount = .82
    # gold_discount = .8
    gold_discount = guild_discount * vip_discount # * crisis_discount  # .66 # with crisis + guild

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

    def lookup(self, rb=0, level=1):
        df = self.get_reborn_table(rb)
        valS = df.loc[(df.Level == level) & (df.Reborn == rb), 'Might'].values[0]
        valG = df.loc[(df.Level == level) & (df.Reborn == rb), 'Troops'].values[0]
        return (valS, valG)

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
        tmp.loc[0, 'Souls'] = -1 * (total_souls - avail_souls - self.sn(rb + 1))

        tmp['Cum Souls'] = tmp.Souls.cumsum()
        tmp['Cum Gold'] = tmp.Gold.cumsum()
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        if avail_gold > 0:
            tmp = tmp[tmp['Cum Gold'] <= avail_gold]
        return tmp

    def _get_reborn_point(self, df, rb=1, a=6, b=11, c=16, d=21, e=26):
        alev = a
        if rb == 1:
            alev = a
        elif rb == 2:
            alev = b
        elif rb == 3:
            alev = c
        elif rb == 4:
            alev = d
        elif rb == 5:
            alev = e
        else:
            return (0, 0)

        valS = df.loc[(df.Level == alev) & (df.Reborn == rb - 1), 'Cum Souls'].values[0]
        valG = df.loc[(df.Level == alev) & (df.Reborn == rb - 1), 'Cum Gold'].values[0]
        return (valS, valG)

    def _has_reborn_1(self, df, rb=1, a=6, b=11, c=16, d=21, e=26):
        if rb == 1:
            return ((df['Level'] == a) & (df['Reborn'] == 0)).any()
        elif rb == 2:
            return ((df['Level'] == b) & (df['Reborn'] == 1)).any()
        elif rb == 3:
            return ((df['Level'] == c) & (df['Reborn'] == 2)).any()
        elif rb == 4:
            return ((df['Level'] == d) & (df['Reborn'] == 3)).any()
        elif rb == 5:
            return ((df['Level'] == e) & (df['Reborn'] == 4)).any()

    @abstractmethod
    def has_reborn_1(self, df, rb=1):
        pass

    @abstractmethod
    def get_reborn_1_point(self, df, rb=1):
        pass

