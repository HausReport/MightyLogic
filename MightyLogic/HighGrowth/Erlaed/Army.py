import pandas as pd
import plotly.express as px


class Army:

    def __init__(self):
        self.data_frame = None

    def fromFile(self, file):
        self.data_frame = pd.read_csv(file)

    def fromDataframe(self, frame):
        self.data_frame = frame

    def getArmy(self):
        return self.data_frame

    def getLegendaries(self):
        return self.data_frame[self.data_frame['Rarity'] == 'Legendary']

    def getEpics(self):
        return self.data_frame[self.data_frame['Rarity'] == 'Epic']

    def getRares(self):
        return self.data_frame[self.data_frame['Rarity'] == 'Rare']

    def getCommons(self):
        return self.data_frame[self.data_frame['Rarity'] == 'Common']

    def getGutterLegendaries(self):
        legos = self.getLegendaries()
        return legos[(legos['Level'] > 1) & (legos['Level'] < 11)]

    def getGutterEpics(self):
        legos = self.getEpics()
        return legos[(legos['Level'] > 1) & (legos['Level'] < 11)]

    def getGutterRares(self):
        legos = self.getRares()
        return legos[(legos['Level'] > 1) & (legos['Level'] < 11)]

    def getLevelOneLegendaries(self):
        legos = self.getLegendaries()
        return legos[(legos['Level'] == 1)]

    def getHistogram(self, rarity="Legendary", nBins=20):
        heroes = self.data_frame[self.data_frame['Rarity'] == rarity]
        fig = px.histogram(heroes, x="Level", nbins=nBins)
        return fig
