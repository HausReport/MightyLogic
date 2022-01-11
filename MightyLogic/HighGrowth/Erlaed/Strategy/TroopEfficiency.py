from MightyLogic.HighGrowth.Erlaed.Strategy.Strategy import Strategy


class TroopEfficiency(Strategy):

    def execute(self, df, rarity, name, avail_gold=-1):
        bleh = rarity.get_moves_by_name(df, name, avail_gold)
        bleh = bleh[bleh.Score == bleh.Score.max()]
        bleh["Name"] = name
        return bleh