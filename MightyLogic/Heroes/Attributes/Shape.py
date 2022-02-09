from __future__ import annotations

from enum import unique, Enum, auto
from typing import Optional


@unique
class Shape(Enum):
    BUILDING = auto()
    MELEE = auto()
    RANGED = auto()

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Shape]:
        try:
            return Shape[s.upper()]
        except KeyError:
            return None
