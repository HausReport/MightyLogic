from datetime import datetime
from pprint import pprint

from MightyLogic.Player.NightTerror import getNightTerrorPlayerGroup
from MightyLogic.Rewards.Reward import Reward
from MightyLogic.TurfWar.Tiles.BuildingFactory import *
from MightyLogic.TurfWar.Tiles.TileList import TileList
from MightyLogic.TurfWar.TurfWarMap import TurfWarMap
from MightyLogic.Player import *

playerGroup = getNightTerrorPlayerGroup()
#nt: NightTerror = NightTerror()
#playerGroup = nt.getPlayerGroup()
print(playerGroup.strength())
playerGroup.elixirize(1200000)
print(playerGroup.strength())

# print("Report Generated at " + datetime.utcnow().strftime("%H:%M GMT on %d %B %Y"))
# four_groups= playerGroup.split(4)
# i=0
# for group in four_groups:
#   group.print(title="Team " + str(i), time=False)
#   i +=1

print("Report Generated at " + datetime.utcnow().strftime("%H:%M GMT on %d %B %Y"))
four_groups= playerGroup.splitDesired([250000,250000,350000,125000])
i=0
for group in four_groups:
  group.print(title="Team " + str(i), time=False)
  i +=1











# #
# # A Turf War Map
# #
#
# map2 =TurfWarMap()
#
# # Use convenience functions to build value array
# map2.addTile('A',1, mountains(3000,2000))
# map2.addTile('A',2, forest(3000,0,2000))
# map2.addTile('A',3, plains(3000, 2000))
# map2.addTile('A',4, mountains(1600,1000))
# map2.addTile('A',5, forest(3000,0,2000))
# map2.addTile('A',6, plains(3000, 2000))
#
# map2.addTile('B',1, factory(1650,500,5000))
# map2.addTile('B',2, mountains(5000,5000))
# map2.addTile('B',3, lighthouse(3500,300,7000))
# map2.addTile('B',4, plains(5000,5000))
# map2.addTile('B',5, mountains(5000,5000))
# map2.addTile('B',6, gold_mine(90000,500,5000))
#
# map2.addTile('C',1, forest(3000,0,2000))
# map2.addTile('C',2, plains(5000,5000))
# map2.addTile('C',3, mountains(5000,5000))
# map2.addTile('C',4, forest(5000,0,5000))
# map2.addTile('C',5, hells_gate(600,800,8500))
# map2.addTile('C',6, mountains(3000,2000))
#
# map2.addTile('D',1, mountains(3000,2000))
# map2.addTile('D',2, witch_hut(3500,600, 7000))
# map2.addTile('D',3, plains(5000,5000))
# map2.addTile('D',4, altar(600,800,8500))
# map2.addTile('D',5, forest(5000,0,5000))
# map2.addTile('D',6, lighthouse(2000, 400, 5000))
#
# map2.addTile('E',1, plains(3000, 2000))
# map2.addTile('E',2, mountains(3000,2000))
# map2.addTile('E',3, forest(3000,0,2000))
# map2.addTile('E',4, plains(3000, 2000))
# map2.addTile('E',5, mountains(3000,2000))
# map2.addTile('E',6, forest(3000,0,2000))
#
#
# # Payout array
# #image = map2.getValues()
# #pprint(image)
#
# #print("STAGING SCORES")
# #pprint(map2.stagingScores())
# map2.setGuild("Nightterror")
# map2.setStartDate(year=2021, month=7, day=17)
# map2.printReport()
#
# print("")
# map2.printNeighborList('B',2)
#
# pprint(map2.getScaledStaging())
#
#
# def getTiles(args):
#   ret = []
#   for arg in args:
#     ret.append(map2.getTile(arg[0], arg[1]))
#   return ret
#
# ts = getTiles([ ['A',1], ['B',3]])
# for t in ts:
#   print( str(t))
#
# rew1 = ts[0].reward
# rew2 = ts[1].reward
#
# rew3 = rew1.combine(rew2)
# print(rew1.share(.07))
# print(rew2.share(.07))
# print(rew3.share(.07))
#
# rewiv = ts[0].combineRewards(ts[1])
# print(rewiv.share(.07))
#
# print("combined")
# t4 = ts[0].combine(ts[1])
# print( t4 )
# print(t4.share(.07))
#
# print("New")
#
# rew = Reward(myName="Combo")
# rew = rew.combine(rew1)
# rew = rew.combine(rew2)
# rew = rew.combine(rew3)
# print(rew.share(.07))
# print(rew)
# print("End")
#
# print("Here")
# ret =  [['A', 1], ['B', 1], ['C', 1]]
# tarr = map2.getTiles(ret)
# pprint(tarr)
# #tlist = TileList(map=map2,coords=tarr)
# tlist = TileList(map2,ret)
# print(type(tlist))
# print(tlist.getName())
# print(tlist.payouts()) #share(0.20))
#
# print("WTF")