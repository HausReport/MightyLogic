import pandas as pd
import numpy as np
from sklearn import preprocessing
from datetime import datetime


class TurfWarMap():
    row_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    rows = ['A', 'B', 'C', 'D', 'E']
    cols = [1, 2, 3, 4, 5, 6]
    arr = {}  # [[0]*6]*5
    guild = ""

    def setGuild(self, gn):
        self.guild = gn

    def getGuild(self):
        return self.guild

    def setStartDate(self,year, month, day):
        self.date = datetime(year=year, month=month, day=day)

    def getStartDate(self):
        if self.date is None:
            return ""
        return self.date.strftime("%d %B %Y")

    def addTile(self, row, col, tile):
        r = row
        # if not isinstance(row, int):
        #  r = self.row_dict[row.upper()]

        # print(f"{r}-{col} = {tile.reward.myValue}")
        self.arr[r, col] = tile  # [r][col-1] = tile
        tile.setRow(r)
        tile.setColumn(col)

    def grid_distance(self, x0, y0, x1, y1):
        return abs(x0 - x1) + abs(y0 - y1)

    def getTile(self, row, col):
        # print(f"Getting {row}-{col}")
        return self.arr[row, col]

    def isBuilding(self, row, col):
        if row not in self.rows:
            return False
        if col not in self.cols:
            return False
        b = self.arr[row, col]
        return b.building

    def getValue(self, row, col):
        if row not in self.rows:
            return 0
        if col not in self.cols:
            return 0
        b = self.arr[row, col]
        return b.getValue()

    def getBuildingValue(self, row, col):
        if not self.isBuilding(row, col):
            return 0
        return self.getValue(row, col)

    def getNonBuildingValue(self, row, col):
        if self.isBuilding(row, col):
            return 0
        return self.getValue(row, col)

    def getValues(self):
        ret = [[0 for i in range(6)] for j in range(5)]
        r = 0
        for row in self.rows:
            for col in self.cols:
                val = self.arr[row, col].reward.myValue
                # print(f"{r}-{col} = {val}")
                ret[r][col - 1] = val
            r = r + 1
        return ret

    def getTotalValue(self):
        ret = 0
        for row in self.rows:
            for col in self.cols:
                val = self.arr[row, col].reward.myValue
                # print(f"{r}-{col} = {val}")
                ret += val
        return ret

    def upRow(self, row):
        up = chr(ord(row) - 1)
        if up in self.rows:
            return up
        return None

    def leftCol(self, col):
        up = col - 1
        if up in self.cols:
            return up
        return None

    def downRow(self, row):
        up = chr(ord(row) + 1)
        if up in self.rows:
            return up
        return None

    def rightCol(self, col):
        up = col + 1
        if up in self.cols:
            return up
        return None

    def getDataFrame(self):
        image = self.getValues()
        payout = pd.DataFrame(image, index=["A", "B", "C", "D", "E"], columns=[1, 2, 3, 4, 5, 6])
        return payout

    def getStrategicDataFrame(self):
        res = self.stagingScores()
        staging = pd.DataFrame(res, index=["A", "B", "C", "D", "E"], columns=[1, 2, 3, 4, 5, 6])
        return staging

    def stagingScores(self):
        ret = [[0 for x in range(0, 6)] for y in range(0, 5)]

        row_num = 0
        for r in self.rows:
            col_num = 0
            for c in self.cols:
                score = 0
                if self.isBuilding(r,c):
                    pass #print(f"{r}-{c} - Is a building")
                else:
                    #print(f"{r}-{c} - Not a building")
                    #
                    # this tile's score
                    #
                    score += self.getNonBuildingValue(r,c)

                    #
                    # Up & Down nbrs
                    #
                    tmp = self.upRow(r)
                    if tmp is not None:
                        score += self.getBuildingValue(tmp,c)
                    tmp = self.downRow(r)
                    if tmp is not None:
                        score += self.getBuildingValue(tmp,c)
                    #
                    # Left & right nbrs
                    #
                    tmp = self.leftCol(c)
                    if tmp is not None:
                        score += self.getBuildingValue(r,tmp)
                    tmp = self.rightCol(c)
                    if tmp is not None:
                        score += self.getBuildingValue(r,tmp)
                # set score in array here
                ret[row_num][col_num] = score
                #...
                col_num+=1
            row_num += 1
        X_train = np.array(ret)
        # FIXME: should give results in [0-100], giving some >100
        scaler = preprocessing.StandardScaler().fit(X_train)
        X_scaled = scaler.transform(X_train)
        X_scaled = 50 * (X_scaled +1)
        X_scaled = np.where(X_scaled <10,0,X_scaled)
        #X_scaled = np.where(X_scaled >95,1,X_scaled)
        return X_scaled.tolist()
        #return ret

    def oneMove(self, frame):
        ret = [[0 for x in range(0, 6)] for y in range(0, 5)]

        row_num = 0
        for r in self.rows:
            col_num = 0
            for c in self.cols:
                max = 0

                # scan nbr above
                up = chr(ord(r) - 1)
                if up in self.rows:
                    tval = frame.iloc[self.row_dict[up]][c]
                    if tval > max:
                        max = tval

                        # scan nbr below
                dn = chr(ord(r) + 1)
                if dn in self.rows:
                    tval = frame.iloc[self.row_dict[dn]][c]
                    if tval > max:
                        max = tval

                        # scan nbr left
                left = c - 1
                if left in self.cols:
                    tval = frame.iloc[self.row_dict[r]][left]
                    if tval > max:
                        max = tval

                        # scan nbr right
                right = c + 1
                if right in self.cols:
                    tval = frame.iloc[self.row_dict[r]][right]
                    if tval > max:
                        max = tval

                        # scan my val
                tval = frame.iloc[self.row_dict[r]][c]
                if tval > max:
                    max = tval

                ret[row_num][col_num] = max
                col_num += 1
                # print(f"({r}-{c})",end='')
            row_num += 1

        X_train = np.array(ret)
        scaler = preprocessing.StandardScaler().fit(X_train)
        X_scaled = scaler.transform(X_train)
        return X_scaled.tolist()
        #return ret

    def buildingList(self):
        ret = []

        for build in self.arr.values():
            if build.building:
                ret.append(build)

        # To sort the list in place...
        ret.sort(key=lambda x: x.getValue(), reverse=True)
        return ret

    def buildingDict(self):
        ret = {}

        for build in self.arr.values():
            if build.building:
                ret[build.row, build.col] = build

        return ret

    #
    # Human-readable reports
    #
    def buildingListText(self):
        ret = ""
        tmp = self.buildingList()

        for build in tmp:
            ret = ret + build.payouts(ticks=False) + "\n"

        return ret

    def getTotalValueString(self):
        val = self.getTotalValue()
        return f"Total Map Value: {val:,.0f} common souls"

    def printBuildingList(self):
        bl = self.buildingList()
        print("Building          Points      For 1st Place                      Guild Gets")
        print("===============================================================================")
        for build in bl:
            val = build.getValue()
            rew = build.reward.share(.07)
            print(f"{build.row}-{build.column}: {build.name:11s} {val:>8,.0f}  {rew:>35s}, {build.reward.INFLUENCE:>4d} influence.")

    def printReport(self):
        print("Turf War Map Report")
        gn = self.getGuild()
        if gn !="":
            print(f"Guild: {gn}")
        sd = self.getStartDate()
        if sd != "":
            print(f"For the Week of: {sd}")

        print(self.getTotalValueString())
        print("")
        self.printBuildingList()

    # 0 if i'm a building
    # sum of neighbor buildings + my score
    #
# for r in rows:
#   for c in cols:
#     print(f"({r}-{c})",end='')
#   print("")
#
# for r in rows:
#   for c in cols:
#     print( "("+str(payout.iloc[row_dict[r]][c])+")",end='')
#   print("")