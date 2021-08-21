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


class HighGrowthStrategy:
    collection: Collection
    exclusions: FrozenSet[Hero]
    gold_discount: Optional[int]

    def __init__(self, collection: Collection, excluding: HeroSelector, gold_discount: Optional[int]):
        self.collection = collection
        self.exclusions = frozenset(collection.resolve(excluding))
        self.gold_discount = gold_discount

    def has_next(self, gold_remaining: Optional[int]) -> bool:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def process_next(self, gold_remaining: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        raise NotImplementedError("Method needs to be implemented by subclasses")
