from __future__ import annotations

from enum import unique, Enum, auto
from typing import Optional


@unique
class Alignment(Enum):
    CHAOS = auto()
    NATURE = auto()
    ORDER = auto()

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Alignment]:
        try:
            return Alignment[s.upper()]
        except KeyError:
            return None
