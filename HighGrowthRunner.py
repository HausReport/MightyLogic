import logging
import sys
from pathlib import Path
from typing import Any

from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.Hero import Rarity
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


file = Path("tests/HighGrowth/2022-01-09-1521_Bobo_squad_export.txt")

logger.info(f"Squad file: {file}")

logger.info("-" * 120)

collection = Collection.from_squad_export_file(file, HeroDirectory.default())

logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")

logger.info("-" * 120)

bobo_squad = {  # level/reborn these as much as possible | exclude their evolutions
    # melee
    "charon",
    "groot",
    "shaa",
    "mosura",

    # ranged
    "blair",
    "eostre",
    "grace",
    "strik",
}
bobo_to_farm = {  # level these heroes but never reborn them | exclude their evolutions
    # melee
    "diana",  # 21/3
    "flap",  # 18/3
    "freddy",  # 6/0
    "ghosta",  # 6/0
    "goliath",  # 8/0
    "shao lin",  # 16/1
    "sheer",  # 6/0

    # ranged
    "gremory",  # 19/3
    "melia",  # 9/2
    "mizu",  # 6/0
    "necro",  # 6/1
    "mina",  # 16/2
    "yorik",  # 6/0
    "yuri",  # 16/3
}
bobo_farming = {  # exclude these heroes | exclude their evolutions
    # melee
    "angelia",  # 1/2
    "arthur",  # 1/1
    "chuba",  # 1/3
    "d'arc",  # 1/0
    "dead lord",  # 1/2
    "dominus",  # locked
    "fury",  # 1/2
    "legion",  # 1/2
    "mi",  # 1/3
    "scrap",  # 1/1

    # ranged
    "agony",  # 1/2
    "aphro",  # 1/3
    "frost",  # 1/1
    "justia",  # 1/0
    "trix",  # 1/2
    "vixen",  # locked
    "villano",  # 1/1

    # building
    "caesar",  # 1/1
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

    # BabyBobo:
    # none

    # Bobo:
    exclude=all_evolutions_to(bobo_squad) + all_evolutions_to(bobo_farming, inclusive=True) + all_evolutions_to(bobo_to_farm),
    never_reborn=exactly({"charon"}) + exactly(bobo_to_farm),

    # Gravy:
    # none

    # JoeDaddy:
    # none

    # MikeLouie:
    # none

    # Minato:
    # exclude=exactly({"draggara", "yorik"}),
    # never_reborn=exactly({"grace", "charon"}),

    # NotAdam:
    # exclude=all_evolutions_to(not_adam_farming, inclusive=True),

    # Seph:
    # exclude=all_evolutions_to(seph_farming, inclusive=True),
    # never_reborn=none(),

    # SirBrychee:
    # exclude=has_rarity(Rarity.LEGENDARY),
    # never_reborn=none(),  # + has_rarity(Rarity.EPIC),

    # SoulD3aD:
    # none

    # Stalguard:
    # exclude=all_evolutions_to({"dominus", "mosura"}, inclusive=True) + all_evolutions_to({"grace"}),

    gold_discount=Discount.combine(Discount.NIGHTMARE, Discount.VIP8),
)

# calc = HighGrowthCalculation.with_gold_cap(
#     strategy=strategy,
#     gold_cap=3_000_000,
#     # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_6)[0] + 21
# )

calc = HighGrowthCalculation.for_level_ups(
     strategy=strategy,
     level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_7)[0],
     level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_8)[0]
)

logger.info(calc)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")
