from datetime import datetime


class PlayerGroup():
    def __init__(self):
        self.players = []

    def append(self, player):
        self.players.append(player)

    def strength(self):
        sum = 0
        for player in self.players:
            sum += player.getTroops()
        return sum

    def elixirize(self, desiredStrength):
        # make sure all zeroed
        for player in self.players:
            player.setElixirBoost(0)
        # self.sort
        if desiredStrength< self.strength():
            return
        for boost in [20, 30, 40, 60, 70, 90]:
            for player in self.players:
                player.setElixirBoost(boost)
                if self.strength()>= desiredStrength:
                    return

    def sort(self):
        # keyfun= operator.attrgetter("getTroops") # use operator since it's faster than lambda
        self.players.sort(reverse=True)  # sort in-place

    def print(self, title="", time=True):
        if time:
            print("Report Generated at " + datetime.datetime.utcnow().strftime("%H:%M GMT on %d %B %Y"))
        self.sort()
        sum = 0
        if title != "":
            print(title)
        for player in self.players:
            player.print()
            sum += player.getTroops()
        print("Team troops: " + str(sum))

    def splitDesired(self, strengths):
        # desired_strength = sum(strengths)
        desired_strength = 0
        for s in strengths:
            desired_strength += s
        self.elixirize (desired_strength)
        # check if desired_strength met
        gLen = len(strengths)
        groups = [PlayerGroup() for i in range(gLen)]
        self.sort()
        awol_cooldown = PlayerGroup()
        # print("Report Generated at " + datetime.datetime.utcnow().strftime("%H:%M GMT on %d %B %Y"))
        # spent = PlayerGroup()
        for x in self.players:
            if x.awol or x.cooldown:
                awol_cooldown.append(x)
            elif x.getTroops() < 1:
                awol_cooldown.append(x)
                # spent.append(x)
            else:
                mingroup = groups[0]
                minGroupNum = 0
                gNum = 0
                for g in groups:
                    if g.strength()/strengths[gNum] < mingroup.strength()/strengths[minGroupNum]:
                        mingroup = g
                        minGroupNum = gNum
                    gNum +=1
                mingroup.append(x)
        groups.append(awol_cooldown)
        # groups.append(spent)
        return groups
        pass
    # https://stackoverflow.com/questions/5248954/an-algorithm-to-sort-a-list-of-values-into-n-groups-so-that-the-sum-of-each-grou
    def split(self, nTeams):
        groups = [PlayerGroup() for i in range(nTeams)]
        self.sort()
        awol_cooldown = PlayerGroup()
        # print("Report Generated at " + datetime.datetime.utcnow().strftime("%H:%M GMT on %d %B %Y"))
        # spent = PlayerGroup()
        for x in self.players:
            if x.awol or x.cooldown:
                awol_cooldown.append(x)
            elif x.getTroops() < 1:
                awol_cooldown.append(x)
                # spent.append(x)
            else:
                mingroup = groups[0]
                for g in groups:
                    if g.strength() < mingroup.strength():
                        mingroup = g
                mingroup.append(x)
        groups.append(awol_cooldown)
        # groups.append(spent)
        return groups
