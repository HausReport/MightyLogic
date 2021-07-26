from typing import Optional

from Heroes.OwnedHeroDirectory import OwnedHeroDirectory
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MinimizeGoldButNeverReborn(HighGrowthStrategy):
    """
    Always level up the cheapest hero, but never reborn - could also be called MaximizeLevelUpsButNeverReborn.
    """

    def __init__(self, oh_dir: OwnedHeroDirectory, gold_discount: Optional[int]):
        super(MinimizeGoldButNeverReborn, self).__init__(oh_dir, gold_discount)
