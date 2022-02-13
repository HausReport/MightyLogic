

class RebornLevel():

    def __init__(self, reborn, level):
        assert reborn >= 0
        assert reborn <= 5
        assert level >= 1
        assert level <= 31

        self.reborn = reborn
        self.level = level

    def pseudo_level(self):
        return self.reborn * 32 + self.level
