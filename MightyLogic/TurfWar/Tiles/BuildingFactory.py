from MightyLogic.TurfWar.Tiles.Tile import Tile


def altar(epic, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Altar", row=row, column=column, epic=epic, influence=influence, contrib=contrib, building=True)


# ===============================================================================================================
def factory(soul_dust, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Factory", soul_dust=soul_dust, influence=influence, contrib=contrib, row=row, column=column,
                building=True)


def gold_mine(gold, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Gold Mine", gold=gold, influence=influence, contrib=contrib, row=row, column=column,
                building=True)


def hells_gate(epic, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Hell's Gate", epic=epic, influence=influence, contrib=contrib, row=row, column=column,
                building=True)

def stronghold(epic, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Stronghold", epic=epic, influence=influence, contrib=contrib, row=row, column=column,
                building=True)

def lighthouse(rare, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Lighthouse", rare=rare, influence=influence, contrib=contrib, row=row, column=column,
                building=True)


def tree_of_life(rare, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Tree of Life", rare=rare, influence=influence, contrib=contrib, row=row, column=column,
                building=True)


def witch_hut(rare, influence, contrib, row="?", column="?", building=True):
    return Tile(name="Witch Hut", rare=rare, influence=influence, contrib=contrib, row=row, column=column,
                building=True)


#
# Non-buildings
#
def forest(common, influence, contrib, row="?", column="?"):
    return Tile(name="Forest", common=common, influence=influence, contrib=contrib, row=row, column=column)


def mountains(common, contrib, row="?", column="?"):
    return Tile(name="Mountains", common=common, contrib=contrib, row=row, column=column)


def plains(common, contrib, row="?", column="?"):
    return Tile(name="Plains", common=common, contrib=contrib, row=row, column=column)
