from unittest import TestCase

from MightyLogic.HighGrowth.Erlaed.Army import Army
from Rarity.Legendary import Legendary
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth


class TestLegendary(TestCase):
    def setUp(self):
        self.army = Army()
        self.army.fromFile("test.csv")
        self.coll = self.army.data_frame
        self.leg = Legendary()
        self.df = HighestGrowth.get_moves_by_name("Villano Mad Genius", self.army)

    def test_sn(self):
        assert self.leg.souls_needed_to_reborn(1) == 90

    def test_reborn_level(self):
        assert self.leg.reborn_level(1) == 6

    def test_gold(self):
        valS = self.df.loc[(self.df.Level == 15) & (self.df.Reborn == 3), 'Cum Gold'].values[0]
        print(str(valS))
        assert abs(valS-177744) <2

    def test_souls(self):
        valS = self.df.loc[(self.df.Level == 15) & (self.df.Reborn == 3), 'Cum Souls'].values[0]
        print(str(valS))
        assert abs(valS-910) <2

    def test_troops(self):
        valS = self.df.loc[(self.df.Level == 19) & (self.df.Reborn == 0), 'Troops'].values[0]
        print(str(valS))
        assert abs(valS-1532) <2

    def test_might(self):
        valS = self.df.loc[(self.df.Level == 19) & (self.df.Reborn == 0), 'Might'].values[0]
        print(str(valS))
        assert abs(valS-1990) <2

    def test_levelups(self):
        valS = self.df.loc[(self.df.Level == 15) & (self.df.Reborn == 3), 'LevelUps'].values[0]
        print(str(valS))
        assert abs(valS-39) <1

    def test_max_level(self):
        assert self.df.Level.max()==19

    def test_min_level(self):
        assert self.df.Level.min()==11
