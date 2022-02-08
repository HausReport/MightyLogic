import logging
import sys
from pathlib import Path
from typing import Any

from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.Hero import Rarity
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
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
    def _1337():
        class _1337Profile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=has_rarity(Rarity.LEGENDARY) + exactly({"caesar"}),
                    never_reborn=exactly({"charon"}),
                    gold_discount=Discount.combine(Discount.NIGHTMARE)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                return HighGrowthCalculation.for_level_ups(
                    strategy=strategy,
                    level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_9)[0],
                    level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_10)[0]
                )

        return _1337Profile()

    @staticmethod
    def bobo():
        squad = {  # level/reborn these as much as possible | exclude their evolutions
            # melee
            "charon",  # never reborn!
            "diana",
            "groot",
            "mosura",
            "shaa",
            "shao lin",  # 16/2

            # ranged
            "blair",  # 17/3
            "eostre",
            "grace",
            "gremory",  # 19/3
            "strik",
            "villano",  # 1/1
            "yuri",  # 16/3
        }
        to_farm = {  # level these heroes but never reborn them | exclude their evolutions
            # melee
            "amaterasu",  # 11/1
            "apep",  # 13/2 -- TBC
            "d'arc",  # 1/0
            "dominus",  # locked
            "freddy",  # 11/0
            "goliath",  # 11/0
            "griffius",  # 11/1
            "sheer",  # 11/0

            # ranged
            "ghosta",  # 11/0
            "mizu",  # 11/0
            "necro",  # 11/1
            "vixen",  # locked
            "yorik",  # 11/0
        }
        farming = {  # exclude these heroes | exclude their evolutions
            # melee
            "chuba",  # 1/3
            "dead lord",  # 1/2
            "fury",  # 1/2
            "legion",  # 1/2
            "mi",  # 1/3
            "scrap",  # 1/1

            # ranged
            "aphro",  # 1/3
            "frost",  # 1/1
            "justia",  # 1/0
            "madam agony",  # 1/2
            "madam lo'trix",  # 1/2
            "tai ling",  # 1/1

            # building
            "caesar",  # 1/2
        }

        class BoboProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=all_evolutions_to(squad) + all_evolutions_to(farming, inclusive=True) + all_evolutions_to(
                        to_farm),
                    never_reborn=exactly({"charon"}) + exactly(to_farm),
                    gold_discount=Discount.combine(Discount.NIGHTMARE, Discount.VIP9)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                # return HighGrowthCalculation.with_gold_cap(
                #     strategy=strategy,
                #     gold_cap=3_000_000,
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
                    gold_discount=Discount.combine(Discount.NIGHT_SLEEPER)
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
    def barf():
        squad = {
            "dead lord",
            "ghosta",
            "mi",
            "charon",
            "eostre",
            "grace",
            "mosura",
            "gremory"
        }

        class BarfProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                squad_epics = all_evolutions_to(squad) & has_rarity(Rarity.EPIC)
                farming = has_level(level_count=1) & has_rarity(Rarity.LEGENDARY)
                farming_epics = exactly(farming.select(collection)) & has_rarity(Rarity.EPIC)

                return Greedy(
                    collection=collection,
                    exclude=squad_epics + farming + farming_epics,
                    never_reborn=exactly(squad),
                    gold_discount=Discount.combine(Discount.NIGHT_FALL, Discount.VIP13)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                # return HighGrowthCalculation.with_gold_cap(
                #     strategy=strategy,
                #     # gold_cap=3_000_000,
                #     # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_6)[0] + 21
                # )
                return HighGrowthCalculation.for_level_ups(
                    strategy=strategy,
                    # level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_7)[0],
                    level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_10)[0]
                )

        return BarfProfile()

    @staticmethod
    def iahobo():
        class IahoboProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=has_rarity(Rarity.LEGENDARY) + has_rarity(Rarity.EPIC),
                    never_reborn=none(),
                    gold_discount=Discount.combine(Discount.NIGHT_TERROR, Discount.VIP8)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                return HighGrowthCalculation.for_level_ups(
                    strategy=strategy,
                    level_ups_already_completed=CompletionTier.aggregate_to(CompletionTier.TIER_11)[0],
                    level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_12)[0]
                )

        return IahoboProfile()

    @staticmethod
    def seph():
        # never reborn any legendary heroes
        # keep all of tai lings heroes at lvl 1, all of villano, ghosta, and justia at lvl 1.
        # epics and rares of shaa, grace and eostre also at lvl 1 (some i accidently lvled).
        farming = {  # exclude these heroes | exclude their evolutions
            "tai ling",
            "villano",
            "ghosta",
            "justia",
        }
        squad = {  # level/reborn these as much as possible | exclude their evolutions
            "moona",
            "grace",
            "eostre"
        }

        class SephProfile(Profile):

            def get_strategy(self, collection: Collection) -> HighGrowthStrategy:
                return Greedy(
                    collection=collection,
                    exclude=all_evolutions_to(squad) + all_evolutions_to(farming, inclusive=True),
                    never_reborn=has_rarity(Rarity.LEGENDARY),
                    gold_discount=Discount.combine(Discount.NIGHT_TERROR)
                )

            def run_calculation(self, strategy: HighGrowthStrategy) -> HighGrowthCalculation:
                return HighGrowthCalculation.with_gold_cap(
                    strategy=strategy,
                    gold_cap=3_000_000,
                )
                # return HighGrowthCalculation.for_level_ups(
                #     strategy=strategy,
                #     level_ups_goal=CompletionTier.aggregate_to(CompletionTier.TIER_10)[0]
                # )

        return SephProfile()

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
file = Path("tests/HighGrowth/2022-02-06-1537_Bobo_squad_export.txt")

logger.info(f"Squad file: {file}")

logger.info("-" * 120)

collection = Collection.from_squad_export_file(file, HeroDirectory.default())

logger.info(f"Your heroes (before): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")

logger.info("-" * 120)

strategy = profile.get_strategy(collection)
calculation = profile.run_calculation(strategy)

logger.info(calculation)

logger.info("-" * 120)

logger.info(f"Your heroes (after): {pretty_format(collection.all_owned_heroes())}")
logger.info(f"Summary:\n{collection.summarize()}")
