from MightyLogic.TurfWar.Tiles.BuildingFactory import *
from MightyLogic.TurfWar.TurfWarMap import TurfWarMap


def getTestMap1():
    map2 = TurfWarMap()
    map2.setGuild("Nightterror")
    map2.setStartDate(year=2021, month=7, day=17)

    # Use convenience functions to build value array
    map2.addTile('A', 1, mountains(3000, 2000))
    map2.addTile('A', 2, forest(3000, 0, 2000))
    map2.addTile('A', 3, plains(3000, 2000))
    map2.addTile('A', 4, mountains(1600, 1000))
    map2.addTile('A', 5, forest(3000, 0, 2000))
    map2.addTile('A', 6, plains(3000, 2000))

    map2.addTile('B', 1, factory(1650, 500, 5000))
    map2.addTile('B', 2, mountains(5000, 5000))
    map2.addTile('B', 3, lighthouse(3500, 300, 7000))
    map2.addTile('B', 4, plains(5000, 5000))
    map2.addTile('B', 5, mountains(5000, 5000))
    map2.addTile('B', 6, gold_mine(90000, 500, 5000))

    map2.addTile('C', 1, forest(3000, 0, 2000))
    map2.addTile('C', 2, plains(5000, 5000))
    map2.addTile('C', 3, mountains(5000, 5000))
    map2.addTile('C', 4, forest(5000, 0, 5000))
    map2.addTile('C', 5, hells_gate(600, 800, 8500))
    map2.addTile('C', 6, mountains(3000, 2000))

    map2.addTile('D', 1, mountains(3000, 2000))
    map2.addTile('D', 2, witch_hut(3500, 600, 7000))
    map2.addTile('D', 3, plains(5000, 5000))
    map2.addTile('D', 4, altar(600, 800, 8500))
    map2.addTile('D', 5, forest(5000, 0, 5000))
    map2.addTile('D', 6, lighthouse(2000, 400, 5000))

    map2.addTile('E', 1, plains(3000, 2000))
    map2.addTile('E', 2, mountains(3000, 2000))
    map2.addTile('E', 3, forest(3000, 0, 2000))
    map2.addTile('E', 4, plains(3000, 2000))
    map2.addTile('E', 5, mountains(3000, 2000))
    map2.addTile('E', 6, forest(3000, 0, 2000))

    return map2

def getTestMap2():
    map2 = TurfWarMap()
    map2.setGuild("Nightterror")
    map2.setStartDate(year=2021, month=7, day=26)

    # Use convenience functions to build value array
    map2.addTile('A', 1, mountains(1600, 1000))
    map2.addTile('A', 2, forest(1600, 0, 1000))
    map2.addTile('A', 3, plains(1600, 1000))
    map2.addTile('A', 4, mountains(1600, 1000))
    map2.addTile('A', 5, forest(1600, 0, 1000))
    map2.addTile('A', 6, plains(1600, 1000))

    map2.addTile('B', 1, plains(1600, 1000))
    map2.addTile('B', 2, witch_hut(1700, 300, 3500))
    map2.addTile('B', 3, forest(2500, 0, 2500))
    map2.addTile('B', 4, altar(300, 400, 4250))
    map2.addTile('B', 5, mountains(2500, 2500))
    map2.addTile('B', 6, forest(1600, 0, 1000))

    map2.addTile('C', 1, forest(1600, 0, 1000))
    map2.addTile('C', 2, plains(2500, 2500))
    map2.addTile('C', 3, stronghold(300, 400, 4250))
    map2.addTile('C', 4, forest(2500, 0, 2500))
    map2.addTile('C', 5, hells_gate(300, 400, 4250))
    map2.addTile('C', 6, mountains(1600, 1000))

    map2.addTile('D', 1, gold_mine(45000, 250, 2500))
    map2.addTile('D', 2, forest(2500, 0, 2500))
    map2.addTile('D', 3, plains(2500, 2500))
    map2.addTile('D', 4, mountains(2500, 2500))
    map2.addTile('D', 5, forest(2500, 0, 2500))
    map2.addTile('D', 6, factory(900, 250, 2500))

    map2.addTile('E', 1, plains(1600, 1000))
    map2.addTile('E', 2, mountains(1600, 1000))
    map2.addTile('E', 3, forest(1600, 0, 1000))
    map2.addTile('E', 4, plains(1600, 1000))
    map2.addTile('E', 5, mountains(1600, 1000))
    map2.addTile('E', 6, forest(1600, 0, 1000))
    return map2