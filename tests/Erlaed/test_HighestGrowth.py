from unittest import TestCase
from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.Legendary import Legendary
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity

import pandas as pd

class TestHighestGrowth(TestCase):

    def setUp(self):
        self.army = Army()
        self.army.fromFile("test.csv")
        self.coll = self.army.data_frame
        self.leg = Legendary()
        self.moves = self.leg.get_moves_by_name(self.coll, "Ruthless Executioner")

    def test_1(self):
        print(self.moves.to_string(max_colwidth=None))

    def test_2(self):
        self.move = self.leg.get_most_efficient_move_by_name(self.army.getArmy(), "Ruthless Executioner", -1, score_mode=Rarity.TROOP_EFFICIENCY)
        print(self.move.to_string(max_colwidth=None))

    def test_3(self):
        self.move = self.leg.get_most_efficient_move_by_name(self.army.getArmy(), "Ruthless Executioner", -1, score_mode=Rarity.TROOP_EFFICIENCY)
        arm2 = self.army.patch(self.move)
        df = arm2.lookup("Ruthless Executioner")
        print(df.to_string(max_colwidth=None))
