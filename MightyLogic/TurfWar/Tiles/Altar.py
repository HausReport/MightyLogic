from MightyLogic.TurfWar.Tiles.Tile import Tile

from MightyLogic.Rewards.RewardFactory import legendary_chest

class Altar(Tile):

    def __init__(self, epic, influence, contrib, row="?", column="?"):
        super().__init__(name="Altar", row=row, column=column, epic=epic, influence=influence, contrib=contrib)
