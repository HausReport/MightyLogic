from typing import Optional

from Heroes.Collection import Collection, HeroSelector
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MinimizeGoldButNeverReborn(HighGrowthStrategy):
    """
    Always level up the cheapest hero, but never reborn - could also be called MaximizeLevelUpsButNeverReborn.
    """

    def __init__(self, collection: Collection, exclude: HeroSelector, gold_discount: Optional[int]):
        super(MinimizeGoldButNeverReborn, self).__init__(collection, exclude, gold_discount)
