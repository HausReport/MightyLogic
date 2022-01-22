from unittest import TestCase

from HeroDirectory import HeroDirectory


class TestHeroDirectory(TestCase):

    def test_strik(self):
        hd = HeroDirectory.default()
        strik = hd.find("Strik, the Fiery Heart")
        assert strik is not None
