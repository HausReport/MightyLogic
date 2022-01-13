from abc import ABC, abstractmethod

import pandas as pd


class Rarity(ABC):
    guild_discount = .8
    vip_discount = .88
    crisis_discount = .82
    # gold_discount = .8
    gold_discount = guild_discount * vip_discount  # * crisis_discount  # .66 # with crisis + guild
    COMMON = 0
    RARE = 1
    EPIC = 2
    LEGENDARY = 3

    TROOP_EFFICIENCY = 0
    GOLD_EFFICIENCY = 1

    @abstractmethod
    def get_r0_tab(self) -> pd.DataFrame:
        pass

    def get_reborn_table(self, reborn: int) -> pd.DataFrame:
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

    def lookup(self, rb: int = 0, level: int = 1) -> (int, int):
        df = self.get_reborn_table(rb)
        valS = df.loc[(df.Level == level) & (df.Reborn == rb), 'Might'].values[0]
        valG = df.loc[(df.Level == level) & (df.Reborn == rb), 'Troops'].values[0]
        return valS, valG

    @abstractmethod
    def getMightBonus(self, reborn: int) -> int:
        pass

    @abstractmethod
    def getTroopBonus(self, reborn: int) -> int:
        pass

    @abstractmethod
    def to_ordinal(self, reborn: int, level: int) -> int:
        pass

    @abstractmethod
    def to_ordinal2(self, reborn: int, level: int) -> int:
        pass

    @abstractmethod
    def sn(self, rb: int = 0) -> int:
        pass

    @abstractmethod
    def reborn_level(self, rb: int = 0) -> int:
        pass

    def level_dist(self, r0: int, l0: int, r1: int, l1: int) -> int:
        if r0 == r1:
            return l1 - l0

        o0 = self.to_ordinal(r0, l0)
        o1 = self.to_ordinal2(r1, l1)
        return o1 - o0

    def straight_level(self, level: int, reborn: int, avail_souls: int, avail_gold: int = -1) -> pd.DataFrame:
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

    def get_tmp_table(self, total_souls: int, avail_souls: int, avail_gold: int, rb: int) -> pd.DataFrame:
        # print("Hi")
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

    def _get_reborn_point(self, df: pd.DataFrame, rb: int = 1, a: int = 6, b: int = 11, c: int = 16, d: int = 21,
                          e: int = 26) -> (int, int):
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
            return 0, 0

        valS = df.loc[(df.Level == alev) & (df.Reborn == rb - 1), 'Cum Souls'].values[0]
        valG = df.loc[(df.Level == alev) & (df.Reborn == rb - 1), 'Cum Gold'].values[0]
        return valS, valG

    def _has_reborn_1(self, df: pd.DataFrame, rb: int = 1, a: int = 6, b: int = 11, c: int = 16, d: int = 21,
                      e: int = 26) -> bool:
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
    def has_reborn_1(self, df: pd.DataFrame, rb: int = 1) -> bool:
        pass

    @abstractmethod
    def get_reborn_1_point(self, df: pd.DataFrame, rb: int = 1) -> int:
        pass

    def get_moves(self, level: int, reborn: int, avail_souls: int, total_souls: int = -1, avail_gold: int = -1,
                  score_mode: int = TROOP_EFFICIENCY) -> pd.DataFrame:
        (curMight, curTroops) = self.lookup(reborn, level)
        moves = self.fancy_level(level, reborn, avail_souls, total_souls, avail_gold)
        moves["Cur Level"] = level
        moves = moves.copy(deep=True)
        moves["Cur Reborn"] = reborn
        moves["Troop Gain"] = moves["Troops"] - curTroops
        moves = moves[moves['Troop Gain'] > 0]
        moves = moves[moves['Level'] > 10]
        moves['LevelUps'] = 0

        if len(moves) > 0:
            moves['LevelUps'] = moves.apply(
                lambda x: self.level_dist(x["Cur Reborn"], x["Cur Level"], x["Reborn"], x["Level"]),
                axis=1)  # (reborn, level, rb1, l1)
        # rb1 = moves['Reborn'].values[0]
        # l1 = moves['Level'].values[0]

        #
        #  YO!  Pretty sure lamba chokes when result has 0 rows
        #

        if score_mode == Rarity.GOLD_EFFICIENCY:
            moves["Score"] = 10000 * (moves["LevelUps"] / moves["Cum Gold"])
        else:
            moves["Score"] = 10000 * (moves["Troop Gain"] / moves["Cum Gold"])

        return moves

    def get_moves_by_name(self, collection_df: pd.DataFrame, name: str, avail_gold: int = -1,
                          score_mode: int = TROOP_EFFICIENCY) -> pd.DataFrame:
        if (collection_df['Name'] == name).any():
            loc = collection_df.loc[collection_df['Name'] == name]
            level = loc.Level.values[0]
            reborn = loc.Reborns.values[0]
            avail_souls = loc["Available Souls"].values[0]
            total_souls = loc["Total Souls"].values[0]
            return self.get_moves(level, reborn, avail_souls, total_souls, avail_gold, score_mode=score_mode)
        else:
            return None

    def fancy_level(self, level: int, reborn: int, avail_souls: int, total_souls: int = -1,
                    avail_gold: int = -1) -> pd.DataFrame:
        tab = self.straight_level(level, reborn, avail_souls, avail_gold)

        #
        # Have to add extra suppoort for over-levelled heroes
        # i.e. R 0 L 10
        # add a row for R 0 L 6
        #   add parm total_souls
        #   spent_souls = total_souls-avail_souls
        #   figure required_souls
        #
        #   set cum_souls to show "rebate" spent_souls-required_souls
        #   set cum_gold to 0
        #

        #
        # Table of possible levelups
        #
        for rb in range(reborn, 5):
            if self.has_reborn_1(tab, rb=rb):

                (cs, cg) = self.get_reborn_1_point(tab, rb=rb)
                tmp = self.get_reborn_table(rb).copy(deep=True)
                tmp.loc[0, 'Gold'] = cg
                tmp.loc[0, 'Souls'] = cs

                tmp['Cum Souls'] = tmp.Souls.cumsum()
                tmp['Cum Gold'] = tmp.Gold.cumsum()
                tmp = tmp[tmp['Cum Souls'] <= avail_souls]
                if avail_gold > 0:
                    tmp = tmp[tmp['Cum Gold'] <= avail_gold]
                tab = tab.append(tmp)
            elif reborn == rb:
                if level >= self.reborn_level(rb + 1):
                    tmp = self.get_tmp_table(total_souls, avail_souls, avail_gold, rb)
                    tab = tab.append(tmp)

        return tab

    def get_most_efficient_move_by_name(self, df: pd.DataFrame, name: str, avail_gold: int = -1,
                                        score_mode: int = TROOP_EFFICIENCY) -> pd.DataFrame:
        bleh = self.get_moves_by_name(df, name, avail_gold, score_mode=score_mode)
        bleh["Name"] = name
        bleh = bleh[bleh.Score == bleh.Score.max()]
        return bleh
