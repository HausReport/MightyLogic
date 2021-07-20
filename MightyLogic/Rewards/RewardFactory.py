#
# Various types of event chest.  Values for tier 2, chapter 3
# See https://mightyparty.fandom.com/wiki/Global_Events#Event_Chest_Contents
#
from random import randrange

from MightyLogic.Rewards.Reward import Reward


def rare_chest(verbose=False):
  branch = randrange(0,99)
  if branch<75:
    souls = randrange(80,220)
    if verbose:
      print(f"{souls} rare souls")
    return Reward(name="Rare Chest", rare=souls)
  elif branch<77:
    souls = 20
    if verbose:
      print(f"{souls} epic souls")
    return Reward(name="Rare Chest", epic=souls)
  elif branch<97:
    souls = randrange(175,300)
    if verbose:
      print(f"{souls} sparks")
    return Reward(name="Rare Chest", spark=souls)
  else:
    souls = randrange(50,100)
    if verbose:
      print(f"{souls} gems")
    return Reward(name="Rare Chest", gem=souls)

def epic_chest(verbose=False):
  branch = randrange(0,99)
  if branch<75:
    souls = randrange(80,500)
    if verbose:
      print(f"{souls} epic souls")
    return Reward(name="Epic Chest", epic=souls)
  elif branch<77:
    souls = 20
    if verbose:
      print(f"{souls} legendary souls")
    return Reward(name="Epic Chest", legendary=souls)
  elif branch<97:
    souls = randrange(750,2000)
    if verbose:
      print(f"{souls} sparks")
    return Reward(name="Epic Chest", spark=souls)
  else:
    souls = randrange(150,300)
    if verbose:
      print(f"{souls} gems")
    return Reward(name="Epic Chest", gem=souls)

  def legendary_chest(verbose=False):
    branch = randrange(0, 99)
    if branch < 62:
      souls = randrange(40, 160)
      if verbose:
        print(f"{souls} legendary souls")
      return Reward(name="Legendary Chest", legendary=souls)
    elif branch < 97:
      souls = randrange(3500, 10000)
      if verbose:
        print(f"{souls} sparks")
      return Reward(name="Legendary Chest", spark=souls)
    else:
      souls = 1000
      if verbose:
        print(f"{souls} gems")
      return Reward(name="Legendary Chest", gem=souls)