from dataclasses import dataclass
from typing import Optional
from typing import Tuple

from Heroes.Collection import Collection, HeroSelector
from Heroes.Hero import LevelingSteps
from Heroes.OwnedHero import OwnedHero


@dataclass
class HighGrowthStrategy:
    collection: Collection
    exclude: HeroSelector
    gold_discount: Optional[int]

    def has_next(self, gold_remaining: Optional[int]) -> bool:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def process_next(self, gold_remaining: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        raise NotImplementedError("Method needs to be implemented by subclasses")
