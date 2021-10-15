import logging
import sys
from pathlib import Path
from typing import Any

from Heroes.Hero import Rarity
from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.HighGrowth import Discount
from MightyLogic.HighGrowth.Calculator import HighGrowthCalculation, CompletionTier
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
    Path("tests/HighGrowth/2021-10-14-2023_Bobo_squad_export.txt"),
    HeroDirectory.default()
)

logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")

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
    "arioch",  # 15R2
    "chuba",  # 12R2
    "shao lin",  # 15R2

    # ranged
    "alex",  # 14R2
    "aphro",  # 14R2
    "melia",  # 6R2
    "mina",  # 11R2
}
bobo_farming = {  # exclude these heroes + minimize evolutions to them
    # melee
    "angelia",  # 1R2
    "dead lord",  # locked
    "diana",  # 1R0
    "dominus",  # locked
    "flap",  # 1R0
    "fury",  # 1R2
    "legion",  # 1R2
    "mi",  # 1R2
    "mosura",  # 1R1
    "scrap",  # locked
    "super mary",  # locked

    # ranged
    "agony",  # 1R2
    "draggara",  # 1R2
    "flos",  # 1R1
    "frost",  # 1R0
    "ghosta",  # locked
    "justia",  # locked
    "necro",  # 2R0
    "red woman",  # 1R2
    "trix",  # 1R2
    "vixen",  # locked
    "yorik",  # locked
}

not_adam_farming = {  # exclude these heroes + all evolutions to them
    "vixen",
    "scrap",
    "mosura",
    "aphro"
}

seph_farming = {
    "alexandria",
    "dominus"
}

strategy = MinimizeGold(
    collection=collection,

    # Bobo:
    # exclude=exactly(bobo_farming) + (
    #         (
    #                 all_evolutions_to(bobo_squad) +
    #                 all_evolutions_to(bobo_farming) +
    #                 all_evolutions_to(bobo_to_farm)
    #         ) & has_rarity(Rarity.EPIC)
    # ),
    # minimize=all_evolutions_to(bobo_squad) +
    #          all_evolutions_to(bobo_farming) +
    #          all_evolutions_to(bobo_to_farm, inclusive=True),
    # never_reborn=exactly({"charon"}),

    # Gravy:
    # none

    # JoeDaddy:
    # none

    # MikeLouie:
    # none

    # NotAdam:
    # exclude=all_evolutions_to(not_adam_farming, inclusive=True),

    # Seph:
    # exclude=all_evolutions_to(seph_farming, inclusive=True),
    # never_reborn=none(),

    # SirBrychee
    # exclude=exactly({"grace"}),
    # never_reborn=has_rarity(Rarity.LEGENDARY),  # + has_rarity(Rarity.EPIC),

    gold_discount=Discount.combine(Discount.NIGHTMARE, Discount.VIP8),
)

# calc = HighGrowthCalculation.with_gold_cap(
#     strategy=strategy,
#     gold_cap=3_000_000
# )

calc = HighGrowthCalculation.for_level_ups(
    strategy=strategy,
    level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_11)[0]
)

logger.info(calc)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")
