import pandas as pd
import plotly.express as px


class Army:
    data_frame: pd.DataFrame

    def __init__(self):
        self.data_frame = None

    def fromFile(self, file):
        self.data_frame = pd.read_csv(file)

    def fromDataframe(self, frame: pd.DataFrame):
        self.data_frame = frame

    def getArmy(self) -> pd.DataFrame:
        return self.data_frame

    def getLegendaries(self) -> pd.DataFrame:
        return self.data_frame[self.data_frame['Rarity'] == 'Legendary']

    def getEpics(self) -> pd.DataFrame:
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
