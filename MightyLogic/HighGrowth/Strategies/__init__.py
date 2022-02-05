from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional
from typing import Tuple

from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.Hero import LevelingSteps
from MightyLogic.Heroes.OwnedHero import OwnedHero


@dataclass
class HighGrowthStrategy:
    original_collection: Collection = field(init=False)
    collection: Collection
    exclude: HeroSelector
    gold_discount: Optional[float]

    def __post_init__(self):
        self.original_collection = deepcopy(self.collection)

    def has_next(self, gold_remaining: Optional[float]) -> bool:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def process_next(self, gold_remaining: Optional[float]) -> Tuple[OwnedHero, LevelingSteps]:
        raise NotImplementedError("Method needs to be implemented by subclasses")
