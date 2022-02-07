from abc import ABC


class AbstractFilter(ABC):
    def matches(self, val) -> bool:
        pass