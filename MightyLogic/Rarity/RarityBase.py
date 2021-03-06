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
        might = df.loc[(df.Level == level) & (df.Reborn == rb), 'Might'].values[0]
        troops = df.loc[(df.Level == level) & (df.Reborn == rb), 'Troops'].values[0]
        return might, troops

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
    def souls_needed_to_reborn(self, rb: int = 0) -> int:
        """souls needed for given reborn point"""
        pass

    def souls_needed(self, level: int = 0, reborn: int = 0):
        r = self.souls_needed_to_reborn(reborn)
        s2 = self._sn(level)
        return r + s2

    def souls_needed2(self, level1: int = 0, reborn1: int = 0, level2: int = 0, reborn2: int = 0):
        sn1 = self.souls_needed(level1, reborn1)
        sn2 = self.souls_needed(level2, reborn2)
        return sn2 - sn1

    def _sn(self, level):
        rbTable = self.get_reborn_table(0)
        soul_req = rbTable[rbTable.Level <= level].Souls.sum()
        return soul_req

    @abstractmethod
    def reborn_level(self, rb: int = 0) -> int:
        """level at which the given reborn can be done"""
        pass

    def meta_level(self, r0: int, l0: int) -> int:
        return r0*32 + l0

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
        tmp.loc[0, 'Souls'] = -1 * (total_souls - avail_souls - self.souls_needed_to_reborn(rb + 1))

        tmp['Cum Souls'] = tmp.Souls.cumsum()
        tmp['Cum Gold'] = tmp.Gold.cumsum()
        tmp = tmp[tmp['Cum Souls'] <= avail_souls]
        return tmp

    # FIXME: rework as list-based
    @staticmethod
    def _get_reborn_point(df: pd.DataFrame, rb: int = 1, a: int = 6, b: int = 11, c: int = 16, d: int = 21,
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

    @staticmethod
    def _has_reborn_1(df: pd.DataFrame, rb: int = 1, a: int = 6, b: int = 11, c: int = 16, d: int = 21,
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
