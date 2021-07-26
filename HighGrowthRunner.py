import json
import logging
from pathlib import Path
from typing import Any, Dict

from HighGrowth import Discount
from HighGrowth.Calculator import HighGrowthCalculation
from HighGrowth.Strategies.MinimizeGold import MinimizeGold
from Heroes.HeroDirectory import HeroDirectory
from Heroes.OwnedHeroDirectory import OwnedHeroDirectory

# TODO: Fix format
logging.basicConfig(level=logging.INFO)


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


def pretty_print(thing: Any):
    print(pretty_format(thing).rstrip())


hero_dir = HeroDirectory.default()

print(f"All known heroes: {pretty_format(hero_dir.values())}")

print("-" * 120)

oh_dir = OwnedHeroDirectory.from_squad_export_file(
    Path("tests/HighGrowth/2021-07-25-1342_Bobo_squad_export.txt"),
    hero_dir
)

print(f"Your heroes (before): {pretty_format(oh_dir.values())}")
print(f"Summary: {pretty_format(oh_dir.summarize())}")

print("-" * 120)

calc = HighGrowthCalculation.from_strategy(
    high_growth_strategy=MinimizeGold(oh_dir, Discount.GUILD_5.value),
    gold_cap=188_000
)

print(calc)

print("-" * 120)

print(f"Your heroes (after): {pretty_format(oh_dir.values())}")
print(f"Summary: {pretty_format(oh_dir.summarize())}")
