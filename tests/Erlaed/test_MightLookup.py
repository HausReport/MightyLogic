from unittest import TestCase

from MightyUseful.utilities.MightLookup import LevelRebornSoulbindMight

class TestMightLookup(TestCase):

    def test_r3l1(self):
        ghosta = LevelRebornSoulbindMight(1,3,False,False,False,False)
        assert ghosta.might_for == 1550 # from bot

    def test_r4l1(self):
        ghosta = LevelRebornSoulbindMight(1,4,False,False,False,False)
        assert ghosta.might_for == 2750 # from bot

    def test_ghosta0(self):
        ghosta = LevelRebornSoulbindMight(21,3,False,False,False,False)
        assert ghosta.might_for == 2350 + 200 + 400 + 600 # = 3500

    def test_ghosta(self):
        ghosta = LevelRebornSoulbindMight(21,3,True,False,True,False)
        assert ghosta.might_for == 3635

    def test_eostre(self):
        eostre = LevelRebornSoulbindMight(1,0,False,False,False,False)
        assert eostre.might_for == 350

    def test_villano(self):
        villano = LevelRebornSoulbindMight(18,0,True,True,True,True)
        assert villano.might_for == 2010

    def test_tani(self):
        tani = LevelRebornSoulbindMight(12,1,False,False,True,False)
        assert tani.might_for == 1265
