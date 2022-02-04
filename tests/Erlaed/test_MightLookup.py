from MightyUseful.utilities.MightLookup import LevelRebornSoulbindMight

class test_MightLookup:

    def test_level_reborn_soulbind_might(self):
        ghosta = LevelRebornSoulbindMight(21,3,True,False,True,False)
        assert ghosta.might == 3635