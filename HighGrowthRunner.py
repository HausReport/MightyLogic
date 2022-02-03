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


# ======================================================================================================================
# Settings
# ----------------------------------------------------------------------------------------------------------------------

def bobo_settings():
    bobo_squad = {  # level/reborn these as much as possible | exclude their evolutions
        # melee
        "charon",
        "groot",
        "shaa",
        "mosura",

        # ranged
        "eostre",
        "grace",
        "strik",
        "villano",  # 1/1
    }
    bobo_to_farm = {  # level these heroes but never reborn them | exclude their evolutions
        # melee
        "amaterasu",  # 11/1
        "freddy",  # 11/0
        "ghosta",  # 11/0
        "goliath",  # 11/0
        "griffius",  # 11/1
        "shao lin",  # 16/2
        "sheer",  # 11/0

        # ranged
        "blair",  # 17/3
        "gremory",  # 19/3
        "melia",  # 11/2
        "mizu",  # 11/0
        "necro",  # 11/1
        "yorik",  # 11/0
        "yuri",  # 16/3
    }
    bobo_farming = {  # exclude these heroes | exclude their evolutions
        # melee
        "angelia",  # 1/2
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
        "tai ling",  # 1/1
        "trix",  # 1/2
        "vixen",  # locked

        # building
        "caesar",  # 1/2
    }

    file = Path("tests/HighGrowth/2022-02-03-0931_Bobo_squad_export.txt")
    exclude = all_evolutions_to(bobo_squad) + all_evolutions_to(bobo_farming, inclusive=True) + all_evolutions_to(bobo_to_farm)
    never_reborn = exactly({"charon"}) + exactly(bobo_to_farm)
    gold_discount = Discount.combine(Discount.NIGHTMARE, Discount.VIP9)

    return file, exclude, never_reborn, gold_discount


def barf_settings():
    file = None
    exclude = None
    never_reborn = None
    gold_discount = Discount.combine(Discount.NIGHT_FALL, Discount.VIP13)

    return file, exclude, never_reborn, gold_discount


def seph_settings():
    # never reborn any legendary heroes
    # keep all of tai lings heroes at lvl 1, all of villano, ghosta, and justia at lvl 1.
    # epics and rares of shaa, grace and eostre also at lvl 1 (some i accidently lvled).
    seph_farming = {  # exclude these heroes | exclude their evolutions
        "tai ling",
        "villano",
        "ghosta",
        "justia",
    }
    seph_squad = {  # level/reborn these as much as possible | exclude their evolutions
        "moona",
        "grace",
        "eostre"
    }

    file = Path("tests/HighGrowth/2022-01-31_Seph_squad_export.txt")
    exclude = all_evolutions_to(seph_squad) + all_evolutions_to(seph_farming, inclusive=True)
    never_reborn = has_rarity(Rarity.LEGENDARY)
    gold_discount = Discount.combine(Discount.NIGHT_TERROR)

    return file, exclude, never_reborn, gold_discount


def souldead_settings():
    file = None
    exclude = None
    never_reborn = None
    gold_discount = Discount.combine(Discount.NIGHTMARE, Discount.VIP12)

    return file, exclude, never_reborn, gold_discount


# ======================================================================================================================
# Runner
# ----------------------------------------------------------------------------------------------------------------------

file, exclude, never_reborn, gold_discount = seph_settings()

logger.info(f"Squad file: {file}")

logger.info("-" * 120)

collection = Collection.from_squad_export_file(file, HeroDirectory.default())

logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")

logger.info("-" * 120)

strategy = MinimizeGold(
    collection=collection,
    exclude=exclude,
    never_reborn=never_reborn,
    gold_discount=gold_discount,
)

# calc = HighGrowthCalculation.with_gold_cap(
#     strategy=strategy,
#     gold_cap=3_000_000,
#     # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_6)[0] + 21
# )

calc = HighGrowthCalculation.for_level_ups(
     strategy=strategy,
     # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_7)[0],
     level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_10)[0]
)

logger.info(calc)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")
