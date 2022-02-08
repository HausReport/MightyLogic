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


inp_file = Path("tests/HighGrowth/2022-02-05-1107_Bobo_squad_export.txt")
print(f"Loading collection from: {inp_file}...")

collection = Collection.from_squad_export_file(
    inp_file,
    HeroDirectory.default()
)

header("Your heroes (before)")
print(*collection.all_owned_heroes(), sep="\n")
print()
print(collection.summarize())

# header("Legendaries (before)")
# legs = sort_by_level_desc(oh for oh in collection.all_owned_heroes() if oh.hero.rarity == Rarity.LEGENDARY)
# print_by_level(legs)
#
# # TODO: evolve
#
# header("Legendaries (after)")
# reborn_and_level(legs)
# legs = sort_by_level_desc(legs)
# print_by_level(legs)

header("Export")
exp_file = inp_file.with_suffix(".csv")
collection.to_csv_file(Path(exp_file))
print(f"Exported collection to: {exp_file}...")
