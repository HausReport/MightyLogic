from org.MightyLogic.TurfWar.Tiles.Tile import Tile


class Altar(Tile):

    def __init__(self, soul_dust, influence, contrib, row="?", column="?"):
        super().__init__(name="Factory", row=row, column=column, soul_dust=soul_dust, influence=influence,
                         contrib=contrib)
