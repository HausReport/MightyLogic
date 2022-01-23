from unittest import TestCase

from MightyLogic.HighGrowth.Erlaed.Army import Army


class TestArmy(TestCase):

    def setUp(self):
        self.army = Army()
        self.army.fromFile("test.csv")
        self.coll = self.army.data_frame
        #self.leg = Legendary()
        #self.df = self.leg.get_moves_by_name(self.coll, "Villano Mad Genius")

    def test_load(self):
        assert len(self.army.getEpics()) > 0

    def test_souls_needed_to_reborn(self):
        assert self.army.souls_needed_to_reborn(1,10,3196,"Rare") == 354