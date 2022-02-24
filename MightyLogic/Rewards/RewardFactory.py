#
# Various types of event chest.  Values for tier 2, chapter 3
# See https://mightyparty.fandom.com/wiki/Global_Events#Event_Chest_Contents
#
from random import randrange

from MightyLogic.Rewards.Reward import Reward


def rare_chest(verbose=False):
    branch = randrange(0, 99)
    if branch < 75:
        tmp = randrange(80, 220)
        if verbose:
            print(f"{tmp} rare souls")
        return Reward(myName="Rare Chest", rare=tmp)
    elif branch < 77:
        tmp = 20
        if verbose:
            print(f"{tmp} epic souls")
        return Reward(myName="Rare Chest", epic=tmp)
    elif branch < 97:
        tmp = randrange(175, 300)
        if verbose:
            print(f"{tmp} sparks")
        return Reward(myName="Rare Chest", spark=tmp)
    else:
        tmp = randrange(50, 100)
        if verbose:
            print(f"{tmp} gems")
        return Reward(myName="Rare Chest", gem=tmp)


def epic_chest(verbose=False):
    branch = randrange(0, 99)
    if branch < 75:
        tmp = randrange(80, 500)
        if verbose:
            print(f"{tmp} epic souls")
        return Reward(myName="Epic Chest", epic=tmp)
    elif branch < 77:
        tmp = 20
        if verbose:
            print(f"{tmp} legendary souls")
        return Reward(myName="Epic Chest", legendary=tmp)
    elif branch < 97:
        tmp = randrange(750, 2000)
        if verbose:
            print(f"{tmp} sparks")
        return Reward(myName="Epic Chest", spark=tmp)
    else:
        tmp = randrange(150, 300)
        if verbose:
            print(f"{tmp} gems")
        return Reward(myName="Epic Chest", gem=tmp)


def legendary_chest(verbose=False):
    branch = randrange(0, 99)
    if branch < 62:
        tmp = randrange(40, 160)
        if verbose:
            print(f"{tmp} legendary souls")
        return Reward(myName="Legendary Chest", legendary=tmp)
    elif branch < 97:
        tmp = randrange(3500, 10000)
        if verbose:
            print(f"{tmp} sparks")
        return Reward(myName="Legendary Chest", spark=tmp)
    else:
        tmp = 1000
        if verbose:
            print(f"{tmp} gems")
        return Reward(myName="Legendary Chest", gem=tmp)
