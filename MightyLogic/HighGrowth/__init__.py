from functools import reduce


class Discount:
    NONE: float = 0
    CRISIS: float = 0.18

    NIGHTMARE: float = 0.20  # L6
    NIGHT_FALL: float = 0.20  # L6
    NIGHT_MOON: float = 0.16  # L4
    NIGHT_TERROR: float = 0.18  # L5
    NIGHT_SLEEPER: float = 0.10

    VIP8: float = 0.12
    VIP9: float = 0.15
    VIP10: float = 0.18
    VIP11: float = 0.20
    VIP12: float = 0.23
    VIP13: float = 0.25
    VIP14: float = 0.28
    VIP15: float = 0.30

    @staticmethod
    def combine(*discounts: float) -> float:
        effective_discount = reduce(lambda accumulated, new: accumulated * (1.0 - new), discounts, 1.0)
        return round(1.0 - effective_discount, 2)
