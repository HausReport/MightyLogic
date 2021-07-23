from dataclasses import dataclass, field
from typing import Any, Optional
from typing import Tuple

from Heroes.Hero import LevelingSteps
from Heroes.OwnedHero import OwnedHero
from Heroes.OwnedHeroDirectory import OwnedHeroDirectory


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class HighGrowthStrategy:
    oh_dir: OwnedHeroDirectory
    gold_discount: Optional[int]

    def __init__(self, oh_dir: OwnedHeroDirectory, gold_discount: Optional[int]):
        self.oh_dir = oh_dir
        self.gold_discount = gold_discount

    def has_next(self, gold_remaining: Optional[int]) -> bool:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def process_next(self, gold_remaining: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        raise NotImplementedError("Method needs to be implemented by subclasses")
