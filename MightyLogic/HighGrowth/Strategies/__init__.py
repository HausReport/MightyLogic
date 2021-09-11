from dataclasses import dataclass, field
from typing import Any, Optional, FrozenSet
from typing import Tuple

from Heroes.Collection import Collection, HeroSelector
from Heroes.Hero import LevelingSteps, Hero
from Heroes.OwnedHero import OwnedHero


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


@dataclass
class HighGrowthStrategy:
    collection: Collection
    excluding: HeroSelector
    gold_discount: Optional[int]

    def has_next(self, gold_remaining: Optional[int]) -> bool:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def process_next(self, gold_remaining: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        raise NotImplementedError("Method needs to be implemented by subclasses")
