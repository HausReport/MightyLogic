import pandas as pd
import plotly.express as px


class Army:

    def __init__(self):
        self.all = None

    def fromFile(self, file):
        self.all = pd.read_csv(file)

    def fromDataframe(self, frame):
        self.all = frame

    def getArmy(self):
        return self.all

    def getLegendaries(self):
        return self.all[self.all['Rarity'] == 'Legendary']

    def getEpics(self):
        return self.all[self.all['Rarity'] == 'Epic']

    def getRares(self):
        return self.all[self.all['Rarity'] == 'Rare']

    def getCommons(self):
        return self.all[self.all['Rarity'] == 'Common']

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
        heroes = self.all[self.all['Rarity'] == rarity]
        fig = px.histogram(heroes, x="Level", nbins=nBins)
        return fig
