from typing import Optional

from Heroes.OwnedHeroDirectory import OwnedHeroDirectory
from HighGrowth.Strategies import HighGrowthStrategy


# TODO: Implement this strategy
class MaximizeSoulBindPotentialWithMinimalGold(HighGrowthStrategy):
    """
    Get everything to >= required soulbind level without spending too much gold.
    """

    def __init__(self, oh_dir: OwnedHeroDirectory, gold_discount: Optional[int]):
        super(MaximizeSoulBindPotentialWithMinimalGold, self).__init__(oh_dir, gold_discount)
