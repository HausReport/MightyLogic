import pandas as pd


class TurfWarMap():
    row_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    rows = ['A', 'B', 'C', 'D', 'E']
    cols = [1, 2, 3, 4, 5, 6]
    arr = {}  # [[0]*6]*5

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

    def getDataFrame(self):
        image = self.getValues()
        payout = pd.DataFrame(image, index=["A", "B", "C", "D", "E"], columns=[1, 2, 3, 4, 5, 6])
        return payout

    def getStrategicDataFrame(self):
        frame = self.getDataFrame()
        res = self.oneMove(frame)
        return res

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
        return ret

# for r in rows:
#   for c in cols:
#     print(f"({r}-{c})",end='')
#   print("")
#
# for r in rows:
#   for c in cols:
#     print( "("+str(payout.iloc[row_dict[r]][c])+")",end='')
#   print("")