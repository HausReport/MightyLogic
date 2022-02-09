from __future__ import annotations

from enum import unique, Enum
from functools import total_ordering
from typing import Optional


@unique
@total_ordering
class Rarity(Enum):
    COMMON = 0
    RARE = 1
    EPIC = 2
    LEGENDARY = 3

    def __eq__(self, other: Rarity) -> bool:
        return other and self.name == other.name

    def __hash__(self) -> int:
        return self.name.__hash__()

    def __lt__(self, other: Rarity) -> bool:
        return self.value < other.value

    def __str__(self) -> str:
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Rarity]:
        try:
            return Rarity[s.upper()]
        except KeyError:
            return None
