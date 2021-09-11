from datetime import datetime

import numpy as np
import pandas as pd
from scipy.signal import convolve2d
from sklearn.preprocessing import scale


#
# Scales all entries in the given map to values in [0,2]
#
def scaler(target):
    oldShape = target.shape
    foo = target.to_numpy()
    flat = foo.reshape([1, 30])
    X_scaled = scale(flat, axis=1)
    X_scaled -= X_scaled.min()

    # super_threshold_indices = scaled_payout < 0.5
    # scaled_payout[super_threshold_indices] = 0

    return np.reshape(X_scaled, oldShape)


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

    def setStartDate(self, year, month, day):
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
        if row is None:
            return None
        if col is None:
            return None
        if row not in self.rows:
            return None
        if col not in self.cols:
            return None
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

    #
    # Multi-tile support
    #
    def getTiles(self, args):
        ret = []
        for arg in args:
            ret.append(self.getTile(arg[0], arg[1]))
        return ret

    #
    # Neighboring tile functions
    #
    def upRow(self, row):
        up = chr(ord(row) - 1)
        if up in self.rows:
            return up
        return None

    def upTile(self, row, col):
        r = self.upRow(row)
        return self.getTile(r, col)

    def downTile(self, row, col):
        r = self.downRow(row)
        return self.getTile(r, col)

    def leftTile(self, row, col):
        c = self.leftCol(col)
        return self.getTile(row, c)

    def rightTile(self, row, col):
        c = self.rightCol(col)
        return self.getTile(row, c)

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

    def getNeighbors(self, row, col):
        ret = []
        tmp = self.leftTile(row, col)
        if tmp is not None:
            ret.append(tmp)
        tmp = self.rightTile(row, col)
        if tmp is not None:
            ret.append(tmp)
        tmp = self.upTile(row, col)
        if tmp is not None:
            ret.append(tmp)
        tmp = self.downTile(row, col)
        if tmp is not None:
            ret.append(tmp)
        return ret

    #
    # Useful representations
    #
    def getDataFrame(self):
        image = self.getValues()
        payout = pd.DataFrame(image, index=["A", "B", "C", "D", "E"], columns=[1, 2, 3, 4, 5, 6])
        return payout

    def getStrategicDataFrame(self):
        res = self.stagingScores()
        staging = pd.DataFrame(res, index=["A", "B", "C", "D", "E"], columns=[1, 2, 3, 4, 5, 6])
        return staging

    def stagingScores(self):
        # easier to do the summing with a convolve then
        # zero out buildings than both at the same time
        image = self.getValues()

        filter_kernel = [[0, 1, 0],
                         [1, 0, 1],
                         [0, 1, 0]]
        res = convolve2d(image,
                         filter_kernel,
                         mode='same',
                         boundary='fill',
                         fillvalue=0)
        row_num = 0
        for r in self.rows:
            col_num = 0
            for c in self.cols:
                score = 0
                if self.isBuilding(r, c):
                    res[row_num][col_num] = score
                # ...
                col_num += 1
            row_num += 1

        return res

    def getScaledPayout(self):
        return scaler(self.getDataFrame())

    def getScaledStaging(self):
        return scaler(self.getStrategicDataFrame()) / 3

    def getAdjustedMoves(self):
        adjusted_move = np.maximum(self.getScaledPayout(), self.getScaledStaging())
        adjusted_move -= adjusted_move.min()
        return adjusted_move

    def getRecommendedMovesArrays(self):
        flip = self.getAdjustedMoves() #moves
        #epsilon = 0.05
        rows = range(5)
        cols = range(6)
        retx = [[0 for i in cols] for j in rows]
        rety = [[0 for i in cols] for j in rows]

        for row in rows:
            for col in cols:
                up = row + 1
                down = row - 1
                left = col - 1
                right = col + 1

                me = flip[row][col]
                max = me
                z_up = -1000000
                z_dn = -1000000
                z_left = -1000000
                z_right = -1000000

                if up in rows:
                    tmp = flip[up][col]
                    z_up = tmp
                    if tmp > max:
                        max = tmp
                if down in rows:
                    tmp = flip[down][col]
                    z_dn = tmp
                    if tmp > max:
                        max = tmp
                if left in cols:
                    tmp = flip[row][left]
                    z_left = tmp
                    if tmp > max:
                        max = tmp
                if right in cols:
                    tmp = flip[row][right]
                    z_right = tmp
                    if tmp > max:
                        max = tmp

                drow = 4 - row
                if max == me:
                    retx[drow][col] = 0
                    rety[drow][col] = 0
                elif max == z_left:
                    retx[drow][col] = -1
                    rety[drow][col] = 0
                elif max == z_right:
                    retx[drow][col] = 1
                    rety[drow][col] = 0
                elif max == z_up:
                    retx[drow][col] = 0
                    rety[drow][col] = -1
                elif max == z_dn:
                    retx[drow][col] = 0
                    rety[drow][col] = 1

        return retx, rety

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

    def printTileListHeader(self):
        print("Building          Points      For 1st Place                      Guild Gets")
        print("===============================================================================")

    def printNeighborList(self, row, col):
        print(f"Neighbors of tile {row}:{col}")
        self.printTileListHeader()
        nbrs = self.getNeighbors(row, col)
        for nbr in nbrs:
            print(nbr.getTileLine())

    def printBuildingList(self, double=False):
        bl = self.buildingList()
        self.printTileListHeader()
        for build in bl:
            print(build.getTileLine())

    def printReport(self):
        print("Turf War Map Report")
        gn = self.getGuild()
        if gn != "":
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


# def stagingScoresOld(self):
#     ret = [[0 for x in range(0, 6)] for y in range(0, 5)]
#
#     row_num = 0
#     for r in self.rows:
#         col_num = 0
#         for c in self.cols:
#             score = 0
#             if self.isBuilding(r, c):
#                 pass  # print(f"{r}-{c} - Is a building")
#             else:
#                 # print(f"{r}-{c} - Not a building")
#                 #
#                 # this tile's score
#                 #
#                 score += self.getNonBuildingValue(r, c)
#
#                 #
#                 # Up & Down nbrs
#                 #
#                 tmp = self.upRow(r)
#                 if tmp is not None:
#                     score += self.getBuildingValue(tmp, c)
#                 tmp = self.downRow(r)
#                 if tmp is not None:
#                     score += self.getBuildingValue(tmp, c)
#                 #
#                 # Left & right nbrs
#                 #
#                 tmp = self.leftCol(c)
#                 if tmp is not None:
#                     score += self.getBuildingValue(r, tmp)
#                 tmp = self.rightCol(c)
#                 if tmp is not None:
#                     score += self.getBuildingValue(r, tmp)
#             # set score in array here
#             ret[row_num][col_num] = score
#             # ...
#             col_num += 1
#         row_num += 1
#     #X_train = np.array(ret)
#     # FIXME: should give results in [0-100], giving some >100
#     #scaler = preprocessing.StandardScaler().fit(X_train)
#     #X_scaled = scaler.transform(X_train)
#     #X_scaled = 50 * (X_scaled + 1)
#     #X_scaled = np.where(X_scaled < 10, 0, X_scaled)
#     # X_scaled = np.where(X_scaled >95,1,X_scaled)
#     #return X_scaled.tolist()
#     return ret

# def oneMove(self, frame):
#     ret = [[0 for x in range(0, 6)] for y in range(0, 5)]
#
#     row_num = 0
#     for r in self.rows:
#         col_num = 0
#         for c in self.cols:
#             max = 0
#
#             # scan nbr above
#             up = chr(ord(r) - 1)
#             if up in self.rows:
#                 tval = frame.iloc[self.row_dict[up]][c]
#                 if tval > max:
#                     max = tval
#
#                     # scan nbr below
#             dn = chr(ord(r) + 1)
#             if dn in self.rows:
#                 tval = frame.iloc[self.row_dict[dn]][c]
#                 if tval > max:
#                     max = tval
#
#                     # scan nbr left
#             left = c - 1
#             if left in self.cols:
#                 tval = frame.iloc[self.row_dict[r]][left]
#                 if tval > max:
#                     max = tval
#
#                     # scan nbr right
#             right = c + 1
#             if right in self.cols:
#                 tval = frame.iloc[self.row_dict[r]][right]
#                 if tval > max:
#                     max = tval
#
#                     # scan my val
#             tval = frame.iloc[self.row_dict[r]][c]
#             if tval > max:
#                 max = tval
#
#             ret[row_num][col_num] = max
#             col_num += 1
#             # print(f"({r}-{c})",end='')
#         row_num += 1
#
#     X_train = np.array(ret)
#     scaler = preprocessing.StandardScaler().fit(X_train)
#     X_scaled = scaler.transform(X_train)
#     return X_scaled.tolist()
#     # return ret
