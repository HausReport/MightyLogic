from typing import Optional

from Heroes.OwnedHeroDirectory import OwnedHeroDirectory
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MaximizeLevelUps(HighGrowthStrategy):
    """
    Reborn everything as late as possible.
    """

    def __init__(self, oh_dir: OwnedHeroDirectory, gold_discount: Optional[int]):
        super(MaximizeLevelUps, self).__init__(oh_dir, gold_discount)
