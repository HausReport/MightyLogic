#
# Types of in-game currencies
#
from enum import Enum, auto


class Currency(Enum):
    COMMON_SOUL = auto()
    RARE_SOUL = auto()
    SOUL_DUST = auto()
    EPIC_SOUL = auto()
    GOLD = auto()
    KILO_SOUL = auto()
    LEGENDARY_SOUL = auto()
    CONTRIBUTION = auto()
    INFLUENCE = auto()
    SPARK = auto()
    GEM = auto()
