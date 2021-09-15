from typing import Optional

from Heroes.Collection import Collection, HeroSelector
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MaximizeLevelUps(HighGrowthStrategy):
    """
    Reborn everything as late as possible.
    """

    def __init__(self, collection: Collection, exclude: HeroSelector, gold_discount: Optional[int]):
        super(MaximizeLevelUps, self).__init__(collection, exclude, gold_discount)
