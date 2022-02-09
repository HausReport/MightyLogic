from __future__ import annotations

from dataclasses import dataclass, field, InitVar
from typing import Optional, List

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Leveling.LevelData import LevelData


@dataclass(order=True, frozen=True)
class LevelingCost:
    souls: int
    gold: int
    discount: Optional[float] = field(default=None, compare=False)
    allow_zero: InitVar[bool] = False

    def __post_init__(self, allow_zero: bool = False):
        min_cost = 0 if allow_zero else 1
        if self.souls < min_cost:
            raise RuntimeError(f"Souls must be greater than or equal to {min_cost} (was: {self.souls})")
        if self.gold < min_cost:
            raise RuntimeError(f"Gold must be greater than or equal to {min_cost} (was: {self.gold})")

    def __str__(self):
        return f"{self.souls:,} souls + {self.gold:,} gold"

    def with_discount(self, gold_discount: Optional[float] = None) -> LevelingCost:
        if gold_discount is None:
            gold_after_discount = self.gold
            combined_discount = self.discount
        else:
            gold_after_discount = round(float(self.gold) * (1.0 - gold_discount))
            combined_discount = gold_discount + (0 if self.discount is None else self.discount)
        return LevelingCost(souls=self.souls, gold=gold_after_discount, discount=combined_discount, allow_zero=True)

    @staticmethod
    def free() -> LevelingCost:
        return LevelingCost(0, 0, allow_zero=True)

    @staticmethod
    def to(to_level_count: int, rarity: Rarity) -> LevelingCost:
        if to_level_count == 1:
            return LevelingCost.free()
        else:
            datum = LevelData.for_rarity(rarity)[to_level_count]
            return LevelingCost(souls=datum.souls, gold=datum.gold)
