class Discounts:

    def __init__(self, guild: int = 0, vip: int = 0, crisis: int = 0):
        self.set_guild_discount(guild)
        self.set_vip_discount(vip)
        self.set_crisis_discount(crisis)

    def get_gold_discount(self) -> float:
        a = 1 - self.guild_discount
        b = 1 - self.vip_discount
        c = 1 - self.crisis_discount
        return a * b * c

    @staticmethod
    def _to_percentage(percent: int) -> float:
        if percent < 0:
            percent = 0
        if percent > 100:
            percent = 100
        return 1.0 * percent / 100.0

    def set_guild_discount(self, percent: int):
        self.guild_discount = self._to_percentage(percent)

    def set_vip_discount(self, percent: int):
        self.vip_discount = self._to_percentage(percent)

    def set_crisis_discount(self, percent: int):
        self.crisis_discount = self._to_percentage(percent)
