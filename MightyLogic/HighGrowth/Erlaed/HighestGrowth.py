import pandas as pd

from Rarity.Common import Common
from Rarity.Epic import Epic
from Rarity.Legendary import Legendary
from Rarity.Rare import Rare
from Rarity.RarityLeveller import RarityLeveller
from MightyLogic.HighGrowth.Erlaed.Army import Army


class HighestGrowth:
    legendary: Legendary = Legendary()
    epic: Epic = Epic()
    rare: Rare = Rare()
    common: Common = Common()

    def __init__(self, army: Army):
        self.army = army

    @staticmethod
    def _format_output(ret: pd.DataFrame):
        # Fixme, had to remove 'Rarity'
        ret = ret[['Name', 'Cur Reborn', 'Cur Level', 'Reborn', 'Level', 'LevelUps', 'Cum Souls', 'Cum Gold',
                   'Troop Gain', 'Score', 'Rarity']]
        ret = ret.rename(columns={"Cum Gold": "Gold"})
        ret["Total Gold"] = ret.Gold.cumsum()
        ret["Total Troop Gain"] = ret['Troop Gain'].cumsum()
        ret["Total LevelUps"] = ret['LevelUps'].cumsum()
        return ret

    def getLegendaries(self):
        return self.army.getLegendaries()

    def getEpics(self):
        return self.army.getEpics()

    def getRares(self):
        return self.army.getRares()

    def getCommons(self):
        return self.army.getCommons()

    @staticmethod
    def hg_level(level_ups: int) -> int:
        if level_ups < 0:
            return 0
        elif level_ups > 13150:
            return 15
        else:
            tmp = [0, 10, 25, 50, 90, 160, 275, 450, 700, 1050, 1550, 2350, 3650, 5650, 8650, 13150, 999999]
            for i in range(0, 15):
                if tmp[i] <= level_ups < tmp[i + 1]:
                    return i

    @staticmethod
    def hg_gems(level_ups: int):
        finished_round: int = HighestGrowth.hg_level(level_ups)
        tmp = [0, 50, 100, 200, 350, 650, 1100, 1800, 3000, 4500, 7500, 12000, 19500, 30000, 45000, 67500]
        return sum(tmp[0:finished_round + 1])

    @staticmethod
    def get_moves_by_name(aName: str, anArmy: Army) -> pd.DataFrame:
        aHero = anArmy.lookup(aName)
        if aHero is None or len(aHero) == 0:
            return None
        else:
            return HighestGrowth.get_moves(aHero)

    @staticmethod
    def get_moves_series(aHero: pd.Series) -> pd.DataFrame:
        """
        Get dataframe of possible level-ups for the given hero

        :param aHero: A dataframe containing the hero to consider
        :return: (Possibly empty) dataframe of possible moves.  None otherwise.
        """

        #print("get_moves Hero type:" + str(type(aHero)))


        # aName = aHero['Name']
        # collection_df = self.army.getArmy()
        level = aHero.Level
        reborn = aHero.Reborns
        avail_souls = aHero["Available Souls"]
        total_souls = aHero["Total Souls"]
        strategy = aHero["Strategy"]
        rarity = aHero['Rarity']
        #if strategy == 'Freeze':
        #    return None

        return HighestGrowth._get_moves(level, reborn, avail_souls, total_souls, strategy, rarity)
        #
        # straight_level = False
        # score_mode = Rarity.TROOP_EFFICIENCY
        #
        # if strategy == "Troops":
        #     score_mode = Rarity.TROOP_EFFICIENCY
        # elif strategy == "HighGrowth":
        #     score_mode = Rarity.GOLD_EFFICIENCY
        # elif strategy == "NoReborn":
        #     straight_level = True
        # elif strategy == "RebornToLevel1":
        #     score_mode = Rarity.REBORN_TO_ONE
        # elif strategy == "Might":
        #     score_mode = Rarity.MIGHT_EFFICIENCY
        # else:
        #     return None
        #
        # rarity_obj = HighestGrowth.get_rarity_by_name(rarity)
        # return rarity_obj.get_moves(level, reborn, avail_souls, total_souls, score_mode=score_mode,
        #                             straight_level=straight_level)

    @staticmethod
    def _get_moves(level:int, reborn:int, avail_souls:int, total_souls:int, strategy:str, rarity:str) -> pd.DataFrame:
        """
        Get dataframe of possible level-ups for the given hero

        :param aHero: A dataframe containing the hero to consider
        :return: (Possibly empty) dataframe of possible moves.  None otherwise.
        """

        straight_level = False
        score_mode = RarityLeveller.TROOP_EFFICIENCY

        if strategy == 'Freeze':
            return None
        elif strategy == "Troops":
            score_mode = RarityLeveller.TROOP_EFFICIENCY
        elif strategy == "HighGrowth":
            score_mode = RarityLeveller.GOLD_EFFICIENCY
        elif strategy == "NoReborn":
            straight_level = True
        elif strategy == "RebornToLevel1":
            score_mode = RarityLeveller.REBORN_TO_ONE
        elif strategy == "Reboost":
            score_mode = RarityLeveller.REBOOST
        elif strategy == "Might":
            score_mode = RarityLeveller.MIGHT_EFFICIENCY
        else:
            return None

        rarity_obj = HighestGrowth.get_rarity_by_name(rarity)
        return rarity_obj.get_moves(level, reborn, avail_souls, total_souls, score_mode=score_mode,
                                    straight_level=straight_level)

    @staticmethod
    def get_moves(aHero: pd.DataFrame) -> pd.DataFrame:
        """
        Get dataframe of possible level-ups for the given hero

        :param aHero: A dataframe containing the hero to consider
        :return: (Possibly empty) dataframe of possible moves.  None otherwise.
        """

        #print("get_moves Hero type:" + str(type(aHero)))


        # aName = aHero['Name'].values[0]
        # collection_df = self.army.getArmy()
        level = aHero.Level.values[0]
        reborn = aHero.Reborns.values[0]
        avail_souls = aHero["Available Souls"].values[0]
        total_souls = aHero["Total Souls"].values[0]
        strategy = aHero["Strategy"].values[0]
        rarity = aHero['Rarity'].values[0]

        return HighestGrowth._get_moves(level, reborn, avail_souls, total_souls, strategy, rarity)
        # straight_level = False
        # score_mode = Rarity.TROOP_EFFICIENCY
        #
        # if strategy == "Troops":
        #     score_mode = Rarity.TROOP_EFFICIENCY
        # elif strategy == "HighGrowth":
        #     score_mode = Rarity.GOLD_EFFICIENCY
        # elif strategy == "NoReborn":
        #     straight_level = True
        # elif strategy == "RebornToLevel1":
        #     score_mode = Rarity.REBORN_TO_ONE
        # elif strategy == "Might":
        #     score_mode = Rarity.MIGHT_EFFICIENCY
        # else:
        #     return None
        #
        # rarity_obj = HighestGrowth.get_rarity_by_name(rarity)
        # return rarity_obj.get_moves(level, reborn, avail_souls, total_souls, score_mode=score_mode,
        #                             straight_level=straight_level)

    def get_most_efficient_move(self, aHero: pd.DataFrame) -> pd.DataFrame:
        """
        Get level-up with highest score.  In case of tie, one with maximum level-ups wins.

        :param collection_df:
        :param heroName:
        :return: dataframe containing best move
        """

        #print("get_most_efficient_move Hero type:" + str(type(aHero)))
        possibleMoves = self.get_moves_series(aHero)
        if possibleMoves is None:
            return None

        possibleMoves["Name"] = aHero['Name']
        possibleMoves = possibleMoves[possibleMoves.Score == possibleMoves.Score.max()]
        possibleMoves = possibleMoves[possibleMoves.LevelUps == possibleMoves.LevelUps.max()]

        if len(possibleMoves)<1:
            return None
        # it's possible to have ties for max score
        # in case of a tie, return option with most level-ups
        return possibleMoves.iloc[[0]] # maximum 1 row

    @staticmethod
    def get_rarity_by_name(aName: str):
        """
        Returns rarity with name closest to given string
        :param aName: name for rarity
        :return: A rarity if possible, None otherwise.
        """
        if aName is None or len(aName) == 0:
            return None
        xName = aName.strip()
        if xName[0].lower() == 'l':
            return HighestGrowth.legendary
        elif xName[0].lower() == 'e':
            return HighestGrowth.epic
        elif xName[0].lower() == 'r':
            return HighestGrowth.rare
        elif xName[0].lower() == 'c':
            return HighestGrowth.common
        else:
            return None

    @staticmethod
    def get_most_efficient_move_by_name(heroName: str, army: Army):
        possibleMoves = HighestGrowth.get_moves_by_name(heroName, army)
        if possibleMoves is None:
            return None

        possibleMoves["Name"] = heroName
        possibleMoves = possibleMoves[possibleMoves.Score == possibleMoves.Score.max()]
        possibleMoves = possibleMoves[possibleMoves.LevelUps == possibleMoves.LevelUps.max()]
        # it's possible to have ties for max score
        # in case of a tie, return option with most level-ups
        return possibleMoves
