from MightyLogic.HighGrowth.Erlaed.Strategy.Strategy import Strategy


class AbsoluteMight(Strategy):

    def execute(self, df, rarity, name, avail_gold=-1):
        ret = rarity.get_moves_by_name(df, name, avail_gold)
        ret = ret[ret.Might == ret.Might.max()]
        ret["Name"] = name
        return ret
