from typing import Optional

from Heroes.Collection import Collection, HeroSelector
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MaximizeLevelUps(HighGrowthStrategy):
    """
    Reborn everything as late as possible.
    """

    def __init__(self, collection: Collection, excluding: HeroSelector, gold_discount: Optional[int]):
        super(MaximizeLevelUps, self).__init__(collection, excluding, gold_discount)
