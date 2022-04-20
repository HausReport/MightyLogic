import logging
import sys
from pathlib import Path
from typing import Any

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Collection import Collection
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.Heroes.HeroSelector import HeroSelector
from MightyLogic.HighGrowth import Discount
from MightyLogic.HighGrowth.Calculator import HighGrowthCalculation, CompletionTier
from MightyLogic.HighGrowth.Strategies import HighGrowthStrategy
from MightyLogic.HighGrowth.Strategies.Greedy import Greedy

logging.basicConfig(stream=sys.stdout, format='[%(asctime)s] %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

all_evolutions_to = HeroSelector.all_evolutions_to
exactly = HeroSelector.exactly
has_level = HeroSelector.has_level
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
# Profiles
# ----------------------------------------------------------------------------------------------------------------------

class Profile:

    def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    @staticmethod
    def bobo():
        squad = {  # level/reborn these as much as possible | exclude their evolutions
            # melee
            "charon",  # never reborn!
            "fury",  # R2
            "mosura",
            "shao lin",

            # ranged
            "aphro",  # R3
            "eostre",
            "grace",
            "madam agony",
            "villano",
        }
        to_farm = {  # level these heroes but never reborn them | exclude their evolutions
            # melee
            "airavata",  # R0
            "amaterasu",  # R1
            "apep",  # R2 -- TBC
            "d'arc",  # R0
            "dominus",  # R0
            "freddy",  # R0
            "goliath",  # R0
            "griffius",  # R1
            "sheer",  # R0

            # ranged
            "ghosta",  # R0
            "gremory",  # R3
            "mizu",  # R0
            "necro",  # R1
            "strik",  # R3
            "vixen",  # R0
            "yorik",  # R0
            "yuri",  # R3
        }
        farming = {  # exclude these heroes | exclude their evolutions
            # melee
            "chuba",  # R3
            "dead lord",  # R2
            "groot",  # R4
            "legion",  # R2
            "mi",  # R3
            "scrap",  # R1
            "shaa",  # R4

            # ranged
            "blair",  # R4
            "frost",  # R1
            "justia",  # R0
            "madam lo'trix",  # R2
            "tai ling",  # R1

            # building
            "caesar",  # R2
            "void jewel",  # R3
        }

        class BoboProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=all_evolutions_to(squad) + all_evolutions_to(farming, inclusive=True) + all_evolutions_to(
                        to_farm),
                    never_reborn=exactly({"charon"}) + exactly(to_farm),
                    gold_discount=Discount.combine(Discount.NIGHTMARE, Discount.VIP9, Discount.CRISIS)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                # return HighGrowthCalculation.with_gold_cap(
                #     strategy=strategy,
                #     gold_cap=1_700_000,
                #     # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_6)[0] + 21
                # )
                return HighGrowthCalculation.for_level_ups(
                    strategy=strategy,
                    level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_7)[0],
                    level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_8)[0]
                )

        return BoboProfile()

    @staticmethod
    def bobobo():
        squad = {  # level/reborn these as much as possible | exclude their evolutions
        }
        to_farm = {  # level these heroes but never reborn them | exclude their evolutions
        }
        farming = {  # exclude these heroes | exclude their evolutions
        }

        class BoboboProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=all_evolutions_to(squad) + all_evolutions_to(farming, inclusive=True) + all_evolutions_to(
                        to_farm),
                    never_reborn=exactly({"charon"}) + exactly(to_farm),
                    gold_discount=Discount.combine(Discount.NIGHT_SLEEPER, Discount.CRISIS)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                return HighGrowthCalculation.with_gold_cap(
                    strategy=strategy,
                    # gold_cap=3_000_000,
                    # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_6)[0] + 21
                )
                # return HighGrowthCalculation.for_level_ups(
                #     strategy=strategy,
                #     level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_5)[0] + 3,
                #     level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_8)[0]
                # )

        return BoboboProfile()

    @staticmethod
    def souldead():
        class SouldeadProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=none(),
                    never_reborn=none(),
                    gold_discount=Discount.combine(Discount.NIGHTMARE, Discount.VIP12),
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                return None

        return SouldeadProfile()


# ======================================================================================================================
# Runner
# ----------------------------------------------------------------------------------------------------------------------

profile = Profile.bobo()
file = Path("tests/HighGrowth/2022-04-19-2018_Bobo_squad_export.txt")

logger.info(f"Squad file: {file}")

logger.info("-" * 120)

collection = Collection.from_squad_export_file(file, HeroDirectory.default())

# logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary (before):\n{collection.summarize()}")

logger.info("-" * 120)

strategy = profile.get_strategy(collection)
calculation = profile.run_calculation(strategy)

logger.info(calculation)

logger.info("-" * 120)

# logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary (after):\n{collection.summarize()}")
