import logging
import sys
from pathlib import Path
from typing import Any

from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.HighGrowth import Discount
from MightyLogic.HighGrowth.Calculator import HighGrowthCalculation
from MightyLogic.HighGrowth.Strategies.MinimizeGold import MinimizeGold

logging.basicConfig(stream=sys.stdout, format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

all_evolutions_to = HeroSelector.all_evolutions_to
exactly = HeroSelector.exactly
has_rarity = HeroSelector.has_rarity
none = HeroSelector.none


def pretty_format(thing: Any, indent: int = 0):
    def do_indent(s, i=indent):
        return ("  " * i) + s + "\n"

    formatted = ""
    if isinstance(thing, dict):
        formatted += do_indent("{")
        for k, v in thing.items():
            formatted += do_indent(f"{k}: {pretty_format(v, indent + 1).strip()}", indent + 1)
        formatted += do_indent("}")
    elif isinstance(thing, list) or isinstance(thing, set) or isinstance(thing, frozenset):
        formatted += do_indent("[")
        for v in thing:
            formatted += pretty_format(v, indent + 1)
        formatted += do_indent("]")
    else:
        formatted += do_indent(str(thing))
    return formatted


collection = Collection.from_squad_export_file(
    Path("tests/HighGrowth/2021-09-14-1523_JoeDaddy_squad_export.txt"),
    HeroDirectory.default()
)

logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary: {collection.summarize()}")

logger.info("-" * 120)

bobo_squad = {  # minimize evolutions to these heroes
    # melee
    "charon",
    "groot",
    "shaa",

    # ranged
    "blair",
    "eostre",
    "grace",
    "strik",
    "yuri",
}
bobo_to_farm = {  # minimize these heroes + their evolutions
    # melee
    "angelia",  # 10/11
    "arioch",  # 15/16
    "chuba",  # 11/16
    "fury",  # 11/11
    "legion",  # 11/11
    "mi",  # 8/11
    "shao lin",  # 13/16

    # ranged
    "agony",  # 11/11
    "alex",  # 13/16
    "aphro",  # 12/16
    "draggara",  # 11/11
    "melia",  # 11/11
    "mina",  # 2/16
    "red woman",  # 11/11
    "trix",  # 1/16
}
bobo_farming = {  # exclude these heroes + minimize evolutions to them
    # melee
    "dead lord",  # locked
    "diana",  # 1/6
    "dominus",  # locked
    "flap",  # 1/6
    "mosura",  # 1/6
    "super mary",  # locked

    # ranged
    "flos",  # 1/11
    "frost",  # 1/6
    "ghosta",  # locked
    "justia",  # locked
    "vixen",  # locked
}

seph_farming = {
    "alexandria",
    "dominus"
}

# TODO: Support "minimizing"
calc = HighGrowthCalculation.from_strategy(
    strategy=MinimizeGold(
        collection=collection,
        # Bobo:
        #exclude=all_evolutions_to(bobo_squad, inclusive=False) + all_evolutions_to(bobo_to_farm, inclusive=True) + all_evolutions_to(bobo_farming, inclusive=True),
        #exclude=exactly(bobo_farming),
        #minimize=all_evolutions_to(bobo_squad, inclusive=False) +
                 #all_evolutions_to(bobo_to_farm, inclusive=True) +
                 #all_evolutions_to(bobo_farming, inclusive=False),
        #never_reborn=exactly({"charon"}),
        # Gravy:
        # JoeDaddy:
        # Seph:
        # excluding=all_evolutions_to(seph_farming, inclusive=True),
        # never_reborn=none(),
        # SirBrychee
        # excluding=exactly({"grace"}),
        # never_reborn=has_rarity(Rarity.LEGENDARY),  # + has_rarity(Rarity.EPIC),
        gold_discount=Discount.NIGHT_FALL,
    ),
    gold_cap=2_600_000
)

logger.info(calc)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")
