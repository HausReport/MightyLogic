from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

from MightyLogic.Heroes.Leveling.Level import Level
from MightyLogic.Heroes.Leveling.LevelingCost import LevelingCost


@dataclass
class LevelingSteps:
    steps: List[Tuple[Level, LevelingCost]]

    def __add__(self, other: LevelingSteps) -> LevelingSteps:
        return LevelingSteps(self.steps + other.steps)

    def aggregate_cost(self, gold_discount: Optional[float] = None) -> LevelingCost:
        souls = sum(cost.souls for __, cost in self.steps)
        gold = sum(cost.gold for __, cost in self.steps)
        return LevelingCost(souls, gold, allow_zero=True).with_discount(gold_discount)

    def final_level(self) -> Level:
        level, __ = self.steps[-1]
        return level

    def level_up_count(self) -> int:
        return len(list(level for level, __ in self.steps if level.level_count > 1))

    def with_discount(self, gold_discount: Optional[float] = None) -> LevelingSteps:
        return LevelingSteps([
            (level, cost.with_discount(gold_discount))
            for level, cost
            in self.steps
        ])
