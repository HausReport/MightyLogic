from MightyUseful.PandaTables.AbstractFilter import AbstractFilter


class IntRangeFilter(AbstractFilter):

    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

    def matches(self, val):
        tmp = int(val)
        if tmp > self.hi:
            return False
        elif tmp < self.lo:
            return False
        else:
            return True
