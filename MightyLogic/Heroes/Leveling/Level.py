from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from functools import total_ordering
from typing import Dict, Any

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Leveling.LevelData import LevelData
from MightyLogic.Heroes.Leveling.RebornData import RebornData


@dataclass(frozen=True)
@total_ordering
class Level:
    level_count: int
    reborn_count: int

    def __post_init__(self):
        # FIXME: Figure out a better way to do this - leg's have the highest reborn/level count, so use them in interim
        self.require_valid_for(Rarity.LEGENDARY)

    def __lt__(self, other) -> bool:
        lower_reborn = self.reborn_count < other.reborn_count
        same_reborn_and_lower_level = self.reborn_count == other.reborn_count and self.level_count < other.level_count
        return lower_reborn or same_reborn_and_lower_level

    def __str__(self):
        return f"level {self.level_count} @ reborn {self.reborn_count}"

    def has_next_level(self, rarity: Rarity) -> bool:
        return self._leveling_data(rarity).is_valid_level_count(self.level_count + 1)

    def has_next_reborn(self, rarity: Rarity) -> bool:
        return self._reborn_data(rarity).is_valid_reborn_count(self.reborn_count + 1)

    def level_up(self) -> Level:
        return Level(self.level_count + 1, self.reborn_count)

    def might_for(self, rarity: Rarity) -> int:
        # Might is fixed per level
        for_level_count = self._leveling_data(rarity)[self.level_count].might

        # ... but stacks w/ each rebirth
        for_reborn_count = self._reborn_data(rarity).cumulative_might(self.reborn_count)

        return for_level_count + for_reborn_count

    def next_reborn_milestone_for(self, rarity: Rarity) -> int:
        return self._reborn_data(rarity)[self.reborn_count + 1].required_level

    def reborn(self) -> Level:
        return Level(1, self.reborn_count + 1)

    def require_valid_for(self, rarity: Rarity):
        self._leveling_data(rarity).require_valid_level_count(self.level_count)
        self._reborn_data(rarity).require_valid_reborn_count(self.reborn_count)

    def to_dict(self) -> Dict[str, Any]:
        return copy(self.__dict__)

    def troops_for(self, rarity: Rarity) -> int:
        # Troops are fixed per level
        for_level_count = self._leveling_data(rarity)[self.level_count].troops

        # ... but stack w/ each rebirth
        for_reborn_count = self._reborn_data(rarity).cumulative_troops(self.reborn_count)

        return for_level_count + for_reborn_count

    @staticmethod
    def _leveling_data(rarity: Rarity) -> LevelData:
        return LevelData.for_rarity(rarity)

    @staticmethod
    def _reborn_data(rarity: Rarity) -> RebornData:
        return RebornData.for_rarity(rarity)

    @staticmethod
    def max_for(rarity: Rarity) -> Level:
        return Level(
            level_count=LevelData.for_rarity(rarity).max_level_count(),
            reborn_count=RebornData.for_rarity(rarity).max_reborn_count(),
        )

    @staticmethod
    def min_for(rarity: Rarity) -> Level:
        return Level(
            level_count=LevelData.for_rarity(rarity).min_level_count(),
            reborn_count=RebornData.for_rarity(rarity).min_reborn_count(),
        )
