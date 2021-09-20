from enum import Enum


class Discount:
    NONE: float = 0
    CRISIS: float = 0.18
    NIGHTMARE: float = 0.18
    NIGHT_FALL: float = 0.14
    NIGHT_MOON: float = 0.0
    NIGHT_TERROR: float = 0.16

    @staticmethod
    def both(d1: float, d2: float) -> float:
        return round(1.0 - (1.0 - d1) * (1.0 - d2), 2)
