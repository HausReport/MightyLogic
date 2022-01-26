from abc import ABC, abstractmethod

import pandas as pd


class RarityBase(ABC):

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

    def getMightAndTroops(self, rb: int = 0, level: int = 1) -> (int, int):
        """Return might and troops for given level and reborn"""
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
        """Return (reborn, level) to ordinal, ignoring levels over reborn point"""
        pass

    @abstractmethod
    def to_ordinal2(self, reborn: int, level: int) -> int:
        """Return (reborn, level) to ordinal, including levels over reborn point"""
        pass

    @abstractmethod
    def sn(self, rb: int = 0) -> int:
        """souls needed for given reborn point"""
        pass

    @abstractmethod
    def reborn_level(self, rb: int = 0) -> int:
        """level at which the given reborn can be done"""
        pass

    def level_distance(self, r0: int, l0: int, r1: int, l1: int) -> int:
        """shortest distance between two levels"""
        if r0 == r1:
            return l1 - l0

        o0 = self.to_ordinal(r0, l0)
        o1 = self.to_ordinal2(r1, l1)
        return o1 - o0

    def get_tmp_table(self, total_souls: int, avail_souls: int, rb: int) -> pd.DataFrame:
        """Return level-up dataframe for reborn with souls rebated from the reborn"""
        # print("Hi")
        (cs, cg) = (0, 0)  # do rebate here
        tmp = self.get_reborn_table(rb + 1).copy(deep=True)
        tmp.loc[0, 'Gold'] = cg
        tmp.loc[0, 'Souls'] = -1 * (total_souls - avail_souls - self.sn(rb + 1))

        tmp['Cum Souls'] = tmp.Souls.cumsum()
        tmp['Cum Gold'] = tmp.Gold.cumsum()
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        return tmp

    def _get_reborn_point(self, df: pd.DataFrame, rb: int = 1, a: int = 6, b: int = 11, c: int = 16, d: int = 21,
                          e: int = 26) -> (int, int):
        """get the gold and souls needed for the given reborn for the given rarity"""
        if rb == 1:
            theLevel = a
        elif rb == 2:
            theLevel = b
        elif rb == 3:
            theLevel = c
        elif rb == 4:
            theLevel = d
        elif rb == 5:
            theLevel = e
        else:
            return 0, 0

        valS = df.loc[(df.Level == theLevel) & (df.Reborn == rb - 1), 'Cum Souls'].values[0]
        valG = df.loc[(df.Level == theLevel) & (df.Reborn == rb - 1), 'Cum Gold'].values[0]
        return valS, valG

    def _has_reborn_1(self, df: pd.DataFrame, rb: int = 1, a: int = 6, b: int = 11, c: int = 16, d: int = 21,
                      e: int = 26) -> bool:
        """is it possible to do the given reborn?"""
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

    @abstractmethod
    def getName(self) -> str:
        pass
