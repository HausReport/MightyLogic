from MightyLogic.Player.Player import Player
from MightyLogic.Player.PlayerGroup import PlayerGroup

def getNightTerrorPlayerGroup() -> PlayerGroup:
        players = PlayerGroup()
        players.append(Player("Rags", 64927))
        players.append(Player("BilBisqqit", 59909))
        players.append(Player("Malbad", 56436))
        players.append(Player("Hashem", 56118, cooldown=True))
        players.append(Player("Panda", 52514))
        players.append(Player("chingcheng", 50540))

        players.append(Player("LordOtto", 45669))
        players.append(Player("Flowbites", 41781, cooldown=True))
        players.append(Player("Erlaed", 40705))
        players.append(Player("Sente", 38083, cooldown=True))

        players.append(Player("negro", 32510))
        players.append(Player("FriarKen", 31473))
        players.append(Player("Stalguard", 31788))

        players.append(Player("OmniMan", 30975))
        players.append(Player("ThaBozz", 30542))
        players.append(Player("Wheeler", 29897))
        players.append(Player("Vasilich", 29125))

        players.append(Player("Eragon", 28602, 70))
        players.append(Player("Litch", 27547, awol=True))
        players.append(Player("iahobo", 27255))
        players.append(Player("RoMiC", 26482))
        players.append(Player("Ender", 26283))
        players.append(Player("PiXeL1K", 26017))
        players.append(Player("Tech34", 25753))
        players.append(Player("Hung", 25173))
        players.append(Player("Iceman", 24952))
        players.append(Player("Seph", 19118))
        players.append(Player("Beeznutz", 18649))
        players.append(Player("Ramzinator", 14318))
        players.append(Player("Holymight", 13941))
        players.append(Player("Nikki", 11759))
        return players
