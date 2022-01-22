from unittest import TestCase

from MightyLogic.HighGrowth.Erlaed.Army import Army

class TestArmy(TestCase):

    def test_load(self):
        army = Army()
        army.fromFile("test.csv")
        assert len(army.getEpics()) > 0
