from MightyUseful.utilities.MightLookup import LevelRebornSoulbindMight
from collections import defaultdict

from MightyLogic.HighGrowth.Erlaed.Legendary import Legendary


mightDict = defaultdict(list)
lego = Legendary()
for reborn in range(1, 6):
    for level in range(1, 32):
        for sb1 in [True, False]:
            for sb2 in [True, False]:
                for sb3 in [True, False]:
                    for sb4 in [True, False]:
                        baseMight, troops = lego.getMightAndTroops(reborn, level)
                        foo = LevelRebornSoulbindMight(level, reborn, sb1, sb2, sb3, sb4)
                        #print( str(foo.might) + " <-" + str(foo))
                        mightDict[foo.might].append(foo)

aList = mightDict[2795]
for item in aList:
    print(item)
#print( mightDict[3455].__str__())