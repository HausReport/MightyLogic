import pandas as pd
import plotly.express as px

from Epic import Epic
from Legendary import Legendary
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
import pathlib

from Rare import Rare


class Army:
    data_frame: pd.DataFrame

    def __init__(self):
        self.data_frame = None
        p = pathlib.Path("HeroDirectory.csv")
        self.directory = HeroDirectory.from_csv_file(p)

    def fromFile(self, file):
        self.data_frame = pd.read_csv(file)

    def fromDataframe(self, frame: pd.DataFrame):
        self.data_frame = frame

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

    def getHistogram(self, rarity="Legendary", nBins=20):
        heroes = self.data_frame[self.data_frame['Rarity'] == rarity]
        fig = px.histogram(heroes, x="Level", nbins=nBins)
        return fig

    def findName(self, aName):
        return self.directory.find(aName).name

    def get_evolve_froms(self, aName):
        ret = set()
        dude = self.directory.find_by_name(self.findName(aName))
        for x in dude.evolves_from:
            ret.add(x.name)
            ret.update(self.get_evolve_froms(x.name))
            # print(x.name)
        return ret

    def level_to_reborn(self, level, reborn, rarity):
        ra = None
        if rarity == "Legendary":
            ra = Legendary()
        elif rarity == "Epic":
            ra = Epic()
        elif rarity == "Rare":
            ra = Rare()
        if ra is None:
            return 999
        else:
            return ra.reborn_level(reborn)
        #elif rarity == "Common":
        #    ra = ()
