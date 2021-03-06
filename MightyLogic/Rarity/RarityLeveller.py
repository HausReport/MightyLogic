from abc import ABC

import pandas as pd

from MightyLogic.HighGrowth.Erlaed.Discounts import Discounts
from Rarity.RarityBase import RarityBase


class RarityLeveller(RarityBase, ABC):
    discounts = Discounts(guild=20, vip=15, crisis=0)  # crisis 18
    # discounts = Discounts(guild=18, vip=12, crisis=0) # crisis 18
    # FIXME: move gold discount somewhere else
    FENCE = 10  # FIXME - change to average level for that rarity?

    # COMMON = 0
    # RARE = 1
    # EPIC = 2
    # LEGENDARY = 3

    TROOP_EFFICIENCY = 0
    GOLD_EFFICIENCY = 1
    MIXED = 2
    MIGHT_EFFICIENCY = 3
    REBORN_TO_ONE = 4
    EVENT_READY = 5
    REBOOST = 6

    def straight_level(self, level: int, reborn: int, avail_souls: int) -> pd.DataFrame:
        """
        Return dataframe of possible level-ups without any reborns
        :param level: hero's current level
        :param reborn: hero's current reborn
        :param avail_souls: how many souls are available
        :return: dataframe of moves in the current reborn
        """
        tab = self.get_reborn_table(reborn)
        tmp = tab.copy(deep=True)
        tmp['Reborn'] = reborn

        tmp = tmp[tmp.Level > level]
        tmp = tmp.copy(deep=True)
        tmp['Cum Souls'] = tmp.Souls.cumsum()  # is this right? sum on Level>level or >=?
        tmp['Cum Gold'] = tmp.Gold.cumsum()  # yes, level 2 shows requirements to go from level 1 to level 2...
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        return tmp

    def get_moves(self, level: int, reborn: int, avail_souls: int, total_souls: int = -1,
                  score_mode: int = TROOP_EFFICIENCY, straight_level: bool = False) -> pd.DataFrame:
        """
        Low-level function to provide possible moves
        :param level: hero's current level
        :param reborn: hero's current reborn
        :param avail_souls: available souls
        :param total_souls: total souls
        :param score_mode: how to reckon a good move
        :param straight_level: If True, don't consider reborns.
        :return: dataframe of moves or None
        """
        (curMight, curTroops) = self.getMightAndTroops(reborn, level)
        if straight_level: # or level < self.FENCE:
            moves = self.straight_level(level, reborn, avail_souls)
        else:
            moves = self.fancy_level(level, reborn, avail_souls, total_souls)

        # moves['Meta Level'] = moves.apply( lambda x: self.meta_level(x.Reborn, x.Level), axis=1)
        moves["Meta Level"] = (moves["Reborn"] * 32) + moves["Level"]
        moves["Cur Level"] = level
        moves = moves.copy(deep=True)
        moves["Cur Reborn"] = reborn
        moves["Troop Gain"] = moves["Troops"] - curTroops
        moves["Might Gain"] = moves["Might"] - curMight
        moves = moves[moves['Troop Gain'] > 0]
        if score_mode == RarityLeveller.REBORN_TO_ONE:
            moves = moves[moves['Level'] == 1]
        elif score_mode == RarityLeveller.REBOOST:
            maxLev = moves['Meta Level'].max()
            moves = moves[moves['Meta Level'] == maxLev]
        elif score_mode == RarityLeveller.EVENT_READY:
            tmp = moves[moves['Level'] > 15]
            if len(tmp) > 0:
                moves = tmp
            else:
                maxLev = moves['Level'].max()
                moves = moves[moves['Level'] == maxLev]
        elif level < self.FENCE:
            tmp = moves[moves['Level'] > self.FENCE]
            if len(tmp) > 0:
                moves = tmp
            else:
                maxLev = moves['Level'].max()
                moves = moves[moves['Level'] == maxLev]
        else:
            moves = moves[moves['Level'] > self.FENCE]
        moves['LevelUps'] = 0
        moves['Rarity'] = self.getName()

        # fixed problem with lambda freaking out with 0 moves
        if len(moves) < 1:
            # noinspection PyTypeChecker
            return None

        moves['LevelUps'] = moves.apply(
            lambda x: self.level_distance(x["Cur Reborn"], x["Cur Level"], x["Reborn"], x["Level"]),
            axis=1)

        SCALE = 225_000.0
        #  TROOP_SCALE = 700.0 / 14_000.0  # 0.21213203435 # 0.35355339059 # = sqrt(1.0/8.0)
        TROOP_SCALE = 700.0 / 15_000.0  # 0.21213203435 # 0.35355339059 # = sqrt(1.0/8.0)
        if score_mode == RarityLeveller.GOLD_EFFICIENCY:
            moves["Score"] = SCALE * (TROOP_SCALE * moves["Troop Gain"] + moves["LevelUps"]) / (moves["Cum Gold"])
        elif score_mode == RarityLeveller.REBOOST:
            moves["Score"] = 5000 + moves["Meta Level"]
        elif score_mode == RarityLeveller.REBORN_TO_ONE:
            moves["Score"] = 226.0 - moves['LevelUps']
        elif score_mode == RarityLeveller.MIXED:
            moves["Score"] = SCALE * (TROOP_SCALE * moves["Troop Gain"] + moves["LevelUps"]) / (moves["Cum Gold"])
        elif score_mode == RarityLeveller.TROOP_EFFICIENCY or score_mode == RarityLeveller.EVENT_READY:
            moves["Score"] = SCALE * (TROOP_SCALE * moves["Troop Gain"] + moves["LevelUps"]) / (moves["Cum Gold"])
        elif score_mode == RarityLeveller.MIGHT_EFFICIENCY:
            moves["Score"] = 32000 * moves["Might Gain"] / moves["Cum Gold"]
            # SCALE * (TROOP_SCALE * moves["Troop Gain"] + moves["LevelUps"]) / ( moves["Cum Gold"])
        else:
            moves["Score"] = SCALE * (TROOP_SCALE * moves["Troop Gain"] + moves["LevelUps"]) / (moves["Cum Gold"])

        # moves[moves['Level']==11].Score *= 1.1
        # moves[moves['Level']==16].Score *= 1.1
        # moves[moves['Level']==21].Score *= 1.1
        # moves[moves['Level']==26].Score *= 1.1
        # moves[moves['Level']==31].Score *= 1.1
        # if moves['Level'] in [11,16,21,26,31]:

        return moves

    def fancy_level(self, level: int, reborn: int, avail_souls: int, total_souls: int = -1) -> pd.DataFrame:
        """Get dataframe of possible level-ups including reborns
        :param level: hero's current level
        :param reborn: hero's current reborn
        :param avail_souls: hero's available souls
        :param total_souls:  hero's total souls (some may be refunded)
        :return:  dataframe of possible level-ups
        """
        tab = self.straight_level(level, reborn, avail_souls)
        #
        # Table of possible level-ups
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
                tab = tab.append(tmp)
            elif reborn == rb:
                if level >= self.reborn_level(rb + 1):
                    tmp = self.get_tmp_table(total_souls, avail_souls, rb)
                    tab = tab.append(tmp)

        return tab
