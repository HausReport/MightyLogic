from collections import defaultdict

from MightyLogic.HighGrowth.Erlaed.Legendary import Legendary


class LevelRebornSoulbindMight:

    def __init__(self, level, reborn, sb1, sb2, sb3, sb4):
        self.lego = Legendary()
        self.level = level
        self.reborn = reborn
        self.sb1 = sb1
        self.sb2 = sb2
        self.sb3 = sb3
        self.sb4 = sb4
        self.might, troops = self.lego.getMightAndTroops(reborn, level)
        if sb1: self.might += 30
        if sb2: self.might += 40
        if sb3: self.might += 55
        if sb4: self.might += 75

    def __str__(self):
        aStr = "Level " + str(self.level)
        aStr += " Reborn " + str(self.reborn)
        aList = []
        if self.sb1:
            aList.append("1")
        if self.sb2:
            aList.append("2")
        if self.sb3:
            aList.append("3")
        if self.sb4:
            aList.append("4")
        if len(aList) > 0:
            if len(aList) > 1:
                aStr += " Soulbind"
            if len(aList) > 2:
                aStr += "s"
            aStr += ": "
            aStr += ",".join(aList)
        print(aStr)
        return aStr


x = LevelRebornSoulbindMight(20,3,True, False, True, False)
print(x)
print( str(x.might))
mightDict = defaultdict(list)
lego = Legendary()
for reborn in range(1, 6):
    for level in range(1, 32):
        for sb in range(0, 16):
            baseMight, troops = lego.getMightAndTroops(reborn, level)
            soulbits = "{0:b}".format(sb)
            soulbits = soulbits.zfill(4)
            sb1: bool = soulbits[0] == '1'
            sb2: bool = soulbits[1] == '1'
            sb3: bool = soulbits[2] == '1'
            sb4: bool = soulbits[3] == '1'
            foo = LevelRebornSoulbindMight(level, reborn, sb1, sb2, sb3, sb4)
            #print( str(foo.might) + " <-" + str(foo))
            mightDict[foo.might].append(foo)

aList = mightDict[2390]
for item in aList:
    print(item)
#print( mightDict[3455].__str__())
