from __future__ import annotations

from enum import unique, Enum, auto
from typing import Optional


@unique
class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    SEXLESS = auto()

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Gender]:
        try:
            return Gender[s.upper()]
        except KeyError:
            return None
