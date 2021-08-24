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
    Path("tests/HighGrowth/2021-08-20-2210_Bobo_squad_export.txt"),
    HeroDirectory.default()
)

logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary: {pretty_format(collection.summarize())}")

logger.info("-" * 120)

bobo_squad = {
    # melee
    "shaa",
    "arioch",
    "shao lin",

    # ranged
    "eostre",
    "blair",
    "yuri",
    "grace",
    "strik",
    "alex",
    "aphro"
}
bobo_farming = {
    "diana",
    "groot",
    "charon",
    "vixen",
    "dominus",
    "chuba",
    "legion",
    "frost",
    "angelia",
    "super mary",
    "ghosta",
    "trix",
    "red woman",
    "melia",
    "draggara"
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
        excluding=all_evolutions_to(bobo_squad, inclusive=False) + all_evolutions_to(bobo_farming, inclusive=True),
        never_reborn=none(),
        # Gravy:
        #excluding=none(),
        #never_reborn=none(),
        # SirBrychee
        #excluding=exactly({"grace"}),
        #never_reborn=has_rarity(Rarity.LEGENDARY),  # + has_rarity(Rarity.EPIC),
        # Seph:
        #excluding=all_evolutions_to(seph_farming, inclusive=True),
        #never_reborn=none(),
        gold_discount=Discount.NIGHTMARE,
    ),
    gold_cap=3_000_000
)

logger.info(calc)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary: {pretty_format(collection.summarize())}")
