from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity
from MightyLogic.HighGrowth.Erlaed.Strategy.Strategy import Strategy


class GoldEfficiency(Strategy):

    def execute(self, df, rarity, name, avail_gold=-1):
        bleh = rarity.get_moves_by_name(df, name, avail_gold, score_mode=Rarity.GOLD_EFFICIENCY)
        bleh = bleh[bleh.Score == bleh.Score.max()]
        bleh["Name"] = name
        return bleh
