class Player():
    def __init__(self, name, troops, elixirBoost=0, spent=0, cooldown=False, awol=False):
        self.name = name
        self.troops = troops
        self.spent = spent
        self.elixirBoost = elixirBoost
        self.cooldown = cooldown
        self.awol = awol

    def setElixirBoost(self, boost):
        self.elixirBoost = boost

    def getOrder(self, amt):
        return self.getTroops() / 3

    def getNature(self, amt):
        return self.getTroops() / 3

    def getChaos(self, amt):
        return self.getTroops() / 3

    def getTroops(self):
        if self.cooldown or self.awol:
            return 0
        avail = self.troops - self.spent
        if avail < 0:
            avail = 0
        return (avail) * ((100 + self.elixirBoost) / 100)

    def print(self):
        tr = self.getTroops()
        str = f"{tr:>8,.0f} {self.name}"
        if self.elixirBoost > 0:
            str += f" (elixir boost {self.elixirBoost}%)"
        if self.spent > 0:
            str += f" (spent:{self.spent:,.0f})"
        if self.awol:
            str += f" (AWOL)"
        elif self.cooldown:
            str += f" (Cooldown)"
        elif self.getTroops() < 1:
            str += f" (Spent)"
        print(str)

    def __eq__(self, other):
        return self.name == other.name  # and self.geT == other.suit

    def __lt__(self, other):
        return self.getTroops() < other.getTroops()

    # def assign(self, tileNum = 0, order=0, chaos=0, nature=0, elixirBoost=0):
    #  ret = [0 for i in range(3)]
    #  ret[tileNum] = (self.getOrder(1)+self.getChaos(1)+ self.getNature(1))*((100+elixirBoost)/100)
    #  return ret
