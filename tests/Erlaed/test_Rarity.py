from unittest import TestCase

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.Legendary import Legendary
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
import pandas as pd

class TestRarity(TestCase):
    def setUp(self):
        self.army = Army()
        self.army.fromFile("test.csv")
        self.coll = self.army.data_frame
        self.leg = Legendary()
        self.df = HighestGrowth.get_moves_by_name("Villano Mad Genius", self.army)

    def test_level_dist(self):
        assert self.leg.level_distance(0, 6, 1, 1) == 0
        assert self.leg.level_distance(0, 6, 1, 2) == 1
