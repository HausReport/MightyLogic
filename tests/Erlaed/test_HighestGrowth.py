from unittest import TestCase

from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyLogic.HighGrowth.Erlaed.Army import Army


class TestHighestGrowth(TestCase):

    def setUp(self):
        self.army = Army()
        self.army.fromFile("test.csv")
        self.coll = self.army.data_frame
        #self.leg = Legendary()
        self.moves = HighestGrowth.get_moves_by_name("Ruthless Executioner", self.army)
        df = self.army.lookup("Ruthless Executioner")
        print(df.to_string(max_colwidth=None))

    def test_1(self):
        print(self.moves.to_string(max_colwidth=None))

    def test_2(self):
        self.move = HighestGrowth.get_most_efficient_move_by_name("Ruthless Executioner", self.army)
        print(self.move.to_string(max_colwidth=None))

    def test_3(self):
        self.move = HighestGrowth.get_most_efficient_move_by_name("Ruthless Executioner", self.army)
        print(self.move.to_string(max_colwidth=None))
        arm2 = self.army.patch(self.move)
        df = arm2.lookup("Ruthless Executioner")
        print(df.to_string(max_colwidth=None))
        assert df['Available Souls'].values[0] == 756
