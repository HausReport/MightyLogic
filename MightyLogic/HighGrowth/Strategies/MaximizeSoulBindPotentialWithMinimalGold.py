from typing import Optional

from Heroes.Collection import Collection, HeroSelector
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MaximizeSoulBindPotentialWithMinimalGold(HighGrowthStrategy):
    """
    Get everything to >= required soulbind level without spending too much gold.
    """

    def __init__(self, collection: Collection, exclude: HeroSelector, gold_discount: Optional[int]):
        super(MaximizeSoulBindPotentialWithMinimalGold, self).__init__(collection, exclude, gold_discount)
