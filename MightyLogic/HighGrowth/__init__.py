from enum import Enum


class Discount:
    NONE: int = 0
    CRISIS: int = 18
    NIGHTMARE: int = 18
    NIGHT_FALL: int = 0
    NIGHT_MOON: int = 0
    NIGHT_TERROR: int = 16


class Tier(Enum):
    NONE = 0  # FIXME
