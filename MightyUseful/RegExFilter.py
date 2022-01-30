import re

from MightyUseful.AbstractFilter import AbstractFilter


class RegExFilter(AbstractFilter):

    def __init__(self, reg):
        self.regex = re.compile(reg)

    def matches(self, val):
        return self.regex.match(val)