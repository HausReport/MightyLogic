import re

from MightyUseful.PandaTables.AbstractFilter import AbstractFilter


class RegExFilter(AbstractFilter):

    def __init__(self, reg):
        self.regex = re.compile(reg)

    def matches(self, val):
        # if type(val) != str:
        # print("In filter, type is " + str(type(val)))
        return self.regex.match(str(val))
