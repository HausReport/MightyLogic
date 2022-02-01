import pandas as pd
import plotly.express as px

from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity


class Army:
    directory = HeroDirectory.default()  # from_csv_file(p)

    def __init__(self):
        self.data_frame: pd.DataFrame = None
        # p = pathlib.Path(hdPath)

    def icon_url(self, aName: str) -> str:
        return self.directory.icon_url(aName)

    def fromFile(self, file, strat_file="strategies.csv"):
        self.data_frame: pd.DataFrame = pd.read_csv(file)
        self.strat_file = strat_file
        if strat_file is None:
            self.data_frame['Strategy'] = "HighGrowth"
        else:
            try:
                self.strats: pd.DataFrame = pd.read_csv(strat_file)
                tmp = self.data_frame.join(self.strats.set_index('Name'), on='Name')
                self.data_frame = tmp
            except OSError as e:
                self.data_frame['Strategy'] = "HighGrowth"
                print(e.errno)

    def updateStrategy(self, aName, aStrat):
        if aStrat is None or len(aStrat) < 1:
            return
        # hero = self.lookup(aName)
        # update self.data_frame
        # FIXME: check if row exists, as below
        self.data_frame.loc[(self.data_frame['Name'] == aName), "Strategy"] = aStrat

        # load strats file
        # strat_file = IoGui.get_strategies_file()
        if self.strat_file is None:
            pass  # FIXME: what if strat_file isn't there
        else:
            strats: pd.DataFrame = pd.read_csv(self.strat_file)
            if (strats['Name'] == aName).any():
                strats.loc[(strats['Name'] == aName), "Strategy"] = aStrat
            else:
                df2 = {'Name': aName, 'Strategy': aStrat}
                strats = strats.append(df2, ignore_index=True)
            strats.to_csv(self.strat_file, encoding='utf-8', index=False)
        # if name exists, update entry
        # if name nexists, add entry
        # save strats file

    def fromDataframe(self, frame: pd.DataFrame):
        self.data_frame: pd.DataFrame = frame

    def getArmy(self) -> pd.DataFrame:
        return self.data_frame

    def getLegendaries(self) -> pd.DataFrame:
        return self.data_frame[self.data_frame['Rarity'] == 'Legendary']

    def getEpics(self) -> pd.DataFrame:
        # assert self.data_frame is not None, "DataFrame is None"
        # print(self.data_frame)
        return self.data_frame[self.data_frame['Rarity'] == 'Epic']

    def getRares(self) -> pd.DataFrame:
        return self.data_frame[self.data_frame['Rarity'] == 'Rare']

    def getCommons(self) -> pd.DataFrame:
        return self.data_frame[self.data_frame['Rarity'] == 'Common']

    def getGutterLegendaries(self) -> pd.DataFrame:
        legos = self.getLegendaries()
        return legos[(legos['Level'] > 1) & (legos['Level'] < 11)]

    def getGutterEpics(self) -> pd.DataFrame:
        legos = self.getEpics()
        return legos[(legos['Level'] > 1) & (legos['Level'] < 11)]

    def getGutterRares(self) -> pd.DataFrame:
        legos = self.getRares()
        return legos[(legos['Level'] > 1) & (legos['Level'] < 11)]

    def getLevelOneLegendaries(self) -> pd.DataFrame:
        legos = self.getLegendaries()
        return legos[(legos['Level'] == 1)]

    def getHistogram(self, rarity: str = "Legendary", nBins: int = 20):
        heroes = self.data_frame[self.data_frame['Rarity'] == rarity]
        fig = px.histogram(heroes, x="Level", nbins=nBins)
        return fig

    @staticmethod
    def findName(aName: str):
        return Army.directory.find(aName).name

    @staticmethod
    def get_evolve_froms(aName: str):
        ret = set()
        dude = Army.directory.find_by_name(Army.findName(aName))
        if dude is not None:
            for x in dude.evolves_from:
                ret.add(x.name)
                ret.update(Army.get_evolve_froms(x.name))
                # print(x.name)

        return ret

    @staticmethod
    def get_evolve_tos(aName: str):
        ret = set()
        dude = Army.directory.find_by_name(Army.findName(aName))
        if dude is not None:
            for x in dude.evolves_to:
                ret.add(x.name)
                ret.update(Army.get_evolve_tos(x.name))
                # print(x.name)

        return ret

    @staticmethod
    def reborn_level(reborn: int, rarity: str):
        from HighestGrowth import HighestGrowth
        ra = HighestGrowth.get_rarity_by_name(rarity)
        if ra is None:
            return 999
        return ra.reborn_level(reborn)

    #
    # Recently moved from notebook
    #
    @staticmethod
    def souls_needed_to_reborn(cur_reborn, level, avail_souls, rarity):
        target_reborn = cur_reborn + 1
        from HighestGrowth import HighestGrowth
        ra = HighestGrowth.get_rarity_by_name(rarity)
        # print("Rarity: ", ra.getName())

        df = ra.get_reborn_table(cur_reborn).copy(deep=True)
        target_level = ra.reborn_level(target_reborn)
        # print("Current reborn: ", cur_reborn)
        # print("Current level: ", level)
        # print("Target reborn: ", target_reborn)
        # print("Target level: ", target_level)
        if target_level <= level:
            return 0
        else:
            theSlice = df[(df['Level'] > level) & (df['Level'] <= target_level)]
            # print( slice)
            theSum = theSlice.Souls.sum()
            if theSum <= avail_souls:
                return 0
            else:
                # print("Required: ", theSum-avail_souls)
                return theSum - avail_souls

    def lookup(self, aName):
        return self.data_frame[self.data_frame['Name'] == aName]

    def patch(self, moves: pd.DataFrame):
        """Returns the resulting army after the level-ups in the moves dataframe are executed"""
        army = self.data_frame
        ret = army.copy(deep=True)
        for index, row in moves.iterrows():
            aName = row['Name']
            level = row['Level']
            reborn = row['Reborn']
            souls_spent = row['Cum Souls']
            avail_souls = ret.loc[ret.Name == aName, ['Available Souls']]
            ret.loc[ret.Name == aName, ['Level']] = level
            ret.loc[ret.Name == aName, ['Reborns']] = reborn
            #
            # FIXME: Want this to decrement souls by amount used
            # FIXME: returning negative numbers?!?
            ret.loc[ret.Name == aName, ['Available Souls']] = avail_souls - souls_spent

        # FIXME: carry filters from old to new army
        retA = Army()
        retA.data_frame = ret
        # retA.working = anArmy.working
        # retA.locked = anArmy.locked
        return retA
