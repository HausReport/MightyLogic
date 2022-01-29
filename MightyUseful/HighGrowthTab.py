from PySide2.QtWidgets import QMainWindow

from MightyLogic.HighGrowth.Erlaed.Army import Army
from MightyLogic.HighGrowth.Erlaed.HighestGrowth import HighestGrowth
from MightyUseful.IoGui import IoGui
from MightyLogic.HighGrowth.Erlaed.Rarity import Rarity

class Window(QMainWindow):

        def __init__(self):
            super().__init__()
            self.army = Army()
            IoGui.getArmy(self, self.army)
            Rarity.getRarityByName("Legendary")