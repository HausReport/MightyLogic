from MightyLogic.HighGrowth.Erlaed.Strategy.Strategy import Strategy


class AbsoluteMight(Strategy):

    def execute(self, df, rarity, name, avail_gold=-1):
        bleh = rarity.get_moves_by_name(df, name, avail_gold)
        bleh = bleh[bleh.Might == bleh.Might.max()]
        bleh["Name"] = name
        return bleh