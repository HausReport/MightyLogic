from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def execute(self, df, rarity, name, avail_gold=-1):
        pass
