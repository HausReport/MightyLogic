from pathlib import Path
from typing import Iterable

from MightyLogic.Heroes.OwnedHero import OwnedHero
from MightyLogic.Heroes.Hero import Rarity
from MightyLogic.Heroes.Collection import Collection
from MightyLogic.Heroes.HeroDirectory import HeroDirectory


def header(s):
    print()
    print("=" * 120)
    print(s)
    print("-" * 120)


def sort_by_level_desc(owned_heroes):
    return list(sorted(owned_heroes, key=lambda oh: oh.level, reverse=True))


def print_by_level(owned_heroes):
    print(*map(lambda oh: f"{oh.level} - {oh.hero.name} ({oh.souls:,} souls)", owned_heroes), sep="\n")


def reborn_and_level(owned_heroes: Iterable[OwnedHero]):
    for oh in owned_heroes:
        while oh.can_reborn() or oh.can_level_up():
            if oh.can_reborn():
                oh.reborn()
            if oh.can_level_up():
                oh.level_up()


collection = Collection.from_squad_export_file(
    Path("tests/HighGrowth/2021-10-29-1945_Bobo_squad_export.txt"),
    HeroDirectory.default()
)

header("Your heroes (before)")
print(*collection.all_owned_heroes(), sep="\n")
print()
print(collection.summarize())

header("Legendaries (before)")
legs = sort_by_level_desc(oh for oh in collection.all_owned_heroes() if oh.hero.rarity == Rarity.LEGENDARY)
print_by_level(legs)

# TODO: evolve

header("Legendaries (after)")
reborn_and_level(legs)
legs = sort_by_level_desc(legs)
print_by_level(legs)
