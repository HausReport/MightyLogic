import timeit
from collections import defaultdict

from MightyUseful.utilities.MightLookup import LevelRebornSoulbindMight

from Rarity.Legendary import Legendary

#
# Obvious implementation of putting all values in the dict and looking up took 18s to run
# This implementation takes ~1s
#

options = 0
start = timeit.default_timer()

mightDict = defaultdict(list)
lego = Legendary()
for reborn in range(1, 6):
    for level in range(1, 32):
        # for sb1 in [True, False]:
        #     for sb2 in [True, False]:
        #         for sb3 in [True, False]:
        #             for sb4 in [True, False]:
        sb1 = False
        sb2 = False
        sb3 = False
        sb4 = False
        options += 1
        baseMight, troops = lego.getMightAndTroops(reborn, level)
        foo = LevelRebornSoulbindMight(level, reborn, sb1, sb2, sb3, sb4)
        # print( str(foo.might) + " <-" + str(foo))
        mightDict[foo.might_for].append(foo)

baseMight = 4100
answers = []
for sb1 in [True, False]:
    for sb2 in [True, False]:
        for sb3 in [True, False]:
            for sb4 in [True, False]:
                tmpMight = baseMight
                if sb1: tmpMight -= 30
                if sb2: tmpMight -= 40
                if sb3: tmpMight -= 55
                if sb4: tmpMight -= 75
                aList = mightDict[tmpMight]
                for answer in aList:
                    answer.sb1 = sb1
                    answer.sb2 = sb2
                    answer.sb3 = sb3
                    answer.sb4 = sb4
                answers.extend(aList)

for item in answers:
    print(item)

print("Options: " + str(options))
# All the program statements
stop = timeit.default_timer()
execution_time = stop - start
print("Program executed in " + str(execution_time) + " seconds")

# print( mightDict[3455].__str__())
