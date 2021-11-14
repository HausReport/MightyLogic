from functools import reduce


class Discount:
    NONE: float = 0
    CRISIS: float = 0.18
    NIGHTMARE: float = 0.20
    NIGHT_FALL: float = 0.16
    NIGHT_MOON: float = 0.0
    NIGHT_TERROR: float = 0.16
    VIP8: float = 0.12

    @staticmethod
    def combine(*discounts: float) -> float:
        effective_discount = reduce(lambda accumulated, new: accumulated * (1.0 - new), discounts, 1.0)
        return round(1.0 - effective_discount, 2)
