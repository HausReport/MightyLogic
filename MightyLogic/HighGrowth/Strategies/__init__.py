from dataclasses import dataclass
from typing import Optional
from typing import Tuple

from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.Hero import LevelingSteps
from MightyLogic.Heroes.OwnedHero import OwnedHero


@dataclass
class HighGrowthStrategy:
    collection: Collection
    exclude: HeroSelector
    gold_discount: Optional[float]

    def has_next(self, gold_remaining: Optional[float]) -> bool:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def process_next(self, gold_remaining: Optional[float]) -> Tuple[OwnedHero, LevelingSteps]:
        raise NotImplementedError("Method needs to be implemented by subclasses")
