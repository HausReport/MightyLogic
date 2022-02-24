from Rarity.Legendary import Legendary
from unittest import TestCase

class TestSoulsNeeded(TestCase):

    def setUp(self):
        self.leg = Legendary()

    def test_sn(self):
        assert self.leg.souls_needed(1,0) == 0
        assert self.leg.souls_needed(2,0) == 5
        assert self.leg.souls_needed(1,4) == 10780
        assert self.leg.souls_needed(31,5) == 98070

    def test_sn2(self):
        assert self.leg.souls_needed2(5,1, 17, 2) == 3520
        assert self.leg.souls_needed2(5, 1, 31, 5) == 97930
        assert self.leg.souls_needed2(21, 1, 31, 5) == 90160
        assert 1 == 2
        print("Hi")
        # assert self.leg.souls_needed(1,4) == 10780
        # assert self.leg.souls_needed(31,5) == 98070
