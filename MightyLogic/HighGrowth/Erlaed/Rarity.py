from abc import ABC

import pandas as pd

from MightyLogic.HighGrowth.Erlaed.Discounts import Discounts
from MightyLogic.HighGrowth.Erlaed.RarityBase import RarityBase


class Rarity(RarityBase, ABC):
    discounts = Discounts(guild=20, vip=12, crisis=18)
    # FIXME: move gold discount somewhere else
    # guild_discount = .8
    # vip_discount = .88
    # crisis_discount = .82
    # # gold_discount = .8
    # gold_discount = guild_discount * vip_discount  # * crisis_discount  # .66 # with crisis + guild
    FENCE = 10  # FIXME - change to average level for that rarity?

    COMMON = 0
    RARE = 1
    EPIC = 2
    LEGENDARY = 3

    TROOP_EFFICIENCY = 0
    GOLD_EFFICIENCY = 1
    MIXED = 2
    MIGHT_EFFICIENCY = 3
    REBORN_TO_ONE = 4
    EVENT_READY = 5

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
        :return: dataframe of moves
        """
        (curMight, curTroops) = self.getMightAndTroops(reborn, level)
        if straight_level:
            moves = self.straight_level(level, reborn, avail_souls)
        else:
            moves = self.fancy_level(level, reborn, avail_souls, total_souls)

        moves["Cur Level"] = level
        moves = moves.copy(deep=True)
        moves["Cur Reborn"] = reborn
        moves["Troop Gain"] = moves["Troops"] - curTroops
        moves["Might Gain"] = moves["Might"] - curMight
        moves = moves[moves['Troop Gain'] > 0]
        if score_mode == Rarity.REBORN_TO_ONE:
            moves = moves[moves['Level'] == 1]
        elif score_mode == Rarity.EVENT_READY:
            moves = moves[moves['Level'] >= 16]
        else:
            moves = moves[moves['Level'] > self.FENCE]
        moves['LevelUps'] = 0

        # fixed problem with lambda freaking out with 0 moves
        if len(moves) > 0:
            moves['LevelUps'] = moves.apply(
                lambda x: self.level_distance(x["Cur Reborn"], x["Cur Level"], x["Reborn"], x["Level"]),
                axis=1)
        if score_mode == Rarity.GOLD_EFFICIENCY:
            moves["Score"] = 10000000.0 * (moves["LevelUps"] / moves["Cum Gold"]) * (51.0 / 1291.0)
        elif score_mode == Rarity.REBORN_TO_ONE:
            moves["Score"] = 200.0
        elif score_mode == Rarity.MIXED:
            score_a = 10000000.0 * (moves["LevelUps"] / moves["Cum Gold"]) * (51.0 / 1291.0)
            score_b = 10000.0 * (moves["Troop Gain"] / moves["Cum Gold"])
            moves["Score"] = max(score_a, score_b)
        elif score_mode == Rarity.TROOP_EFFICIENCY or score_mode == Rarity.EVENT_READY:
            moves["Score"] = 10000.0 * (moves["Troop Gain"] / moves["Cum Gold"])
        elif score_mode == Rarity.MIGHT_EFFICIENCY:
            moves["Score"] = moves["Might Gain"]
        else:
            moves["Score"] = 10000.0 * (moves["Troop Gain"] / moves["Cum Gold"])  # FIXME: KLUDGE

        return moves

    def get_moves_by_name(self, collection_df: pd.DataFrame, name: str) -> pd.DataFrame:
        """
        Get dataframe of possible level-ups for the named hero

        :param collection_df: collection dataframe
        :param name: hero to work on
        :return: (Possibly empty) dataframe of possible moves if name exists, None otherwise.
        """
        if (collection_df['Name'] == name).any():
            loc = collection_df.loc[collection_df['Name'] == name]
            level = loc.Level.values[0]
            reborn = loc.Reborns.values[0]
            avail_souls = loc["Available Souls"].values[0]
            total_souls = loc["Total Souls"].values[0]
            strategy = loc["Strategy"].values[0]
            straight_level = False
            score_mode = Rarity.TROOP_EFFICIENCY
            if strategy == "Troops":
                score_mode = Rarity.TROOP_EFFICIENCY
            elif strategy == "HighGrowth":
                score_mode = Rarity.GOLD_EFFICIENCY
            elif strategy == "NoReborn":
                straight_level = True
            elif strategy == "RebornToLevel1":
                score_mode = Rarity.REBORN_TO_ONE
            elif strategy == "Might":
                score_mode = Rarity.MIGHT_EFFICIENCY
            else:
                return None

            return self.get_moves(level, reborn, avail_souls, total_souls, score_mode=score_mode,
                                  straight_level=straight_level)
        else:
            return None

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

    def get_most_efficient_move_by_name(self, collection_df: pd.DataFrame, heroName: str) -> pd.DataFrame:
        """
        Get level-up with highest score.  In case of tie, one with maximum level-ups wins.

        :param collection_df:
        :param heroName:
        :return: dataframe containing best move
        """
        possibleMoves = self.get_moves_by_name(collection_df, heroName)
        if possibleMoves is None:
            return None

        possibleMoves["Name"] = heroName
        possibleMoves = possibleMoves[possibleMoves.Score == possibleMoves.Score.max()]
        possibleMoves = possibleMoves[possibleMoves.LevelUps == possibleMoves.LevelUps.max()]
        # it's possible to have ties for max score
        # in case of a tie, return option with most level-ups
        return possibleMoves

    @staticmethod
    def get_rarity_by_name(aName: str):
        """
        Returns rarity with name closest to given string
        :param aName: name for rarity
        :return: A rarity if possible, None otherwise.
        """
        from MightyLogic.HighGrowth.Erlaed.Common import Common
        from MightyLogic.HighGrowth.Erlaed.Epic import Epic
        from MightyLogic.HighGrowth.Erlaed.Legendary import Legendary
        from MightyLogic.HighGrowth.Erlaed.Rare import Rare

        if aName is None or len(aName) == 0 or aName[0].lower() == 'l':
            return Legendary()
        elif aName[0].lower() == 'e':
            return Epic()
        elif aName[0].lower() == 'r':
            return Rare()
        elif aName[0].lower() == 'c':
            return Common()
        else:
            return None
