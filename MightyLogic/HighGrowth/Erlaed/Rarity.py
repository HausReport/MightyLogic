from abc import ABC

import pandas as pd

from MightyLogic.HighGrowth.Erlaed.RarityBase import RarityBase
from MightyLogic.HighGrowth.Erlaed.Discounts import Discounts

class Rarity(RarityBase, ABC):
    discounts = Discounts(guild=20, vip=12, crisis=18)
    # FIXME: move gold discount somewhere else
    # guild_discount = .8
    # vip_discount = .88
    # crisis_discount = .82
    # # gold_discount = .8
    # gold_discount = guild_discount * vip_discount  # * crisis_discount  # .66 # with crisis + guild

    COMMON = 0
    RARE = 1
    EPIC = 2
    LEGENDARY = 3

    TROOP_EFFICIENCY = 0
    GOLD_EFFICIENCY = 1
    MIXED = 2

    def straight_level(self, level: int, reborn: int, avail_souls: int, avail_gold: int = -1) -> pd.DataFrame:
        """Return dataframe of possible level-ups without any reborns"""
        tab = self.get_reborn_table(reborn)
        tmp = tab.copy(deep=True)
        tmp['Reborn'] = reborn

        tmp = tmp[tmp.Level > level]
        tmp = tmp.copy(deep=True)
        tmp['Cum Souls'] = tmp.Souls.cumsum()  # is this right? sum on Level>level or >=?
        tmp['Cum Gold'] = tmp.Gold.cumsum()  # yes, level 2 shows requirements to go from level 1 to level 2...
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        if avail_gold > 0:
            tmp = tmp[tmp['Cum Gold'] <= avail_gold]
        return tmp

    def get_moves(self, level: int, reborn: int, avail_souls: int, total_souls: int = -1, avail_gold: int = -1,
                  score_mode: int = TROOP_EFFICIENCY) -> pd.DataFrame:
        (curMight, curTroops) = self.getMightAndTroops(reborn, level)
        moves = self.fancy_level(level, reborn, avail_souls, total_souls, avail_gold)
        moves["Cur Level"] = level
        moves = moves.copy(deep=True)
        moves["Cur Reborn"] = reborn
        moves["Troop Gain"] = moves["Troops"] - curTroops
        moves = moves[moves['Troop Gain'] > 0]
        moves = moves[moves['Level'] > 10]
        moves['LevelUps'] = 0

        # fixed problem with lambda freaking out with 0 moves
        if len(moves) > 0:
            moves['LevelUps'] = moves.apply(
                lambda x: self.level_distance(x["Cur Reborn"], x["Cur Level"], x["Reborn"], x["Level"]),
                axis=1)

        if score_mode == Rarity.GOLD_EFFICIENCY:
            moves["Score"] = 10000000.0 * (moves["LevelUps"] / moves["Cum Gold"]) * (51.0 / 1291.0)
        elif score_mode == Rarity.MIXED:
            score_a = 10000000.0 * (moves["LevelUps"] / moves["Cum Gold"]) * (51.0 / 1291.0)
            score_b = 10000.0 * (moves["Troop Gain"] / moves["Cum Gold"])
            moves["Score"] = max(score_a, score_b)
        else:
            moves["Score"] = 10000.0 * (moves["Troop Gain"] / moves["Cum Gold"])

        return moves

    def get_moves_by_name(self, collection_df: pd.DataFrame, name: str, avail_gold: int = -1,
                          score_mode: int = TROOP_EFFICIENCY) -> pd.DataFrame:
        """Get dataframe of possible level-ups for the named hero"""
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
        """Get dataframe of possible level-ups including reborns"""
        tab = self.straight_level(level, reborn, avail_souls, avail_gold)
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
        """Get level-up with highest score.  In case of tie, one with maximum level-ups wins."""
        possibleMoves = self.get_moves_by_name(df, name, avail_gold, score_mode=score_mode)
        possibleMoves["Name"] = name
        possibleMoves = possibleMoves[possibleMoves.Score == possibleMoves.Score.max()]
        possibleMoves = possibleMoves[possibleMoves.LevelUps == possibleMoves.LevelUps.max()]
        # it's possible to have ties for max score
        # in case of a tie, return option with most level-ups
        return possibleMoves

    @staticmethod
    def get_rarity_by_name(aName: str):
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
