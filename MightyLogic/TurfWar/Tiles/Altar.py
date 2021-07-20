from MightyLogic.TurfWar.Tiles.Tile import Tile


class Altar(Tile):

    def __init__(self, epic, influence, contrib, row="?", column="?"):
        super().__init__(name="Altar", row=row, column=column, epic=epic, influence=influence, contrib=contrib)
