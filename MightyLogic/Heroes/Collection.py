from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Dict, Set, FrozenSet, Any, Callable, Iterable, Optional

import pandas
from pandas import Series, DataFrame

from MightyLogic.Heroes import create_secondary_index, deserialize_lines
from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.Heroes.OwnedHero import OwnedHero


def stringify_heroes(heroes: Iterable[Hero]) -> str:
    return "[" + ", ".join(f"\"{hero.name}\"" for hero in heroes) + "]"


class Collection:
    hero_dir: HeroDirectory
    owned_heroes = FrozenSet[OwnedHero]
    by_hero: Dict[Hero, OwnedHero]

    def __init__(self, hero_dir: HeroDirectory, owned_heroes: Set[OwnedHero]):
        self.hero_dir = hero_dir
        self.owned_heroes = frozenset(owned_heroes)
        self.by_hero = create_secondary_index(owned_heroes, lambda oh: oh.hero)

    def __deepcopy__(self, memodict={}):
        dc = Collection(
            hero_dir=self.hero_dir,  # immutable - ok to pass as-is
            owned_heroes=deepcopy(self.owned_heroes, memodict))  # mutable - needs to be copied
        memodict[id(self)] = dc
        return dc

    def all_heroes(self) -> FrozenSet[Hero]:
        return self.hero_dir.values()

    def all_owned_heroes(self) -> FrozenSet[OwnedHero]:
        return self.owned_heroes

    def __by_hero(self, maybe_hero: Optional[Hero]) -> Optional[OwnedHero]:
        return self.by_hero[maybe_hero] if maybe_hero else None

    def find(self, identifier: Any) -> Optional[OwnedHero]:
        maybe_hero: Optional[Hero] = None

        # 1: if we're given an owned hero, just fetch the hero
        if isinstance(identifier, OwnedHero):
            maybe_hero = identifier.hero

        # 2: if we're given a hero, just use that
        if not maybe_hero and isinstance(identifier, Hero):
            maybe_hero = identifier

        # 3: otherwise, try find the hero in the hero directory
        if not maybe_hero:
            maybe_hero = self.hero_dir.find(identifier)

        return self.__by_hero(maybe_hero)

    def find_by_name(self, name: str) -> OwnedHero:
        return self.__by_hero(self.hero_dir.find_by_name(name))

    def find_by_num(self, num: int) -> OwnedHero:
        return self.__by_hero(self.hero_dir.find_by_num(num))

    def might(self) -> int:
        return sum(oh.might for oh in self.owned_heroes)

    def summarize(self) -> DataFrame | Series | None:
        data_frame = self.to_data_frame()
        # TODO: def mymean(x):
        #     return x.mean()
        #  data_frame["A"].agg(["sum", mymean])
        return data_frame.groupby("rarity")["level"].agg(["count", "min", "max"])

    def to_data_frame(self) -> pandas.DataFrame:
        records = [oh.to_data_frame_rec() for oh in self.owned_heroes]
        return pandas.DataFrame.from_records(data=records, index="num")

    def to_csv_file(self, path_to_csv_file: Path) -> None:
        with path_to_csv_file.open("w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=[
                "num",
                "name",
                "rarity",
                "alignment",
                "gender",
                "shape",
                "evolves_to",
                "level_count",
                "reborn_count",
                "souls"
            ])
            writer.writeheader()
            for oh in self.owned_heroes:
                d = oh.to_dict()
                del d["evolves_from"]
                del d["soulbinds"]
                writer.writerow(d)

    def troops(self) -> int:
        return sum(oh.troops for oh in self.owned_heroes)

    @staticmethod
    def __from_file(path_to_file: Path, hero_dir: HeroDirectory, deserializer: Callable[[str], OwnedHero])\
            -> Collection:
        return Collection(hero_dir, set(deserialize_lines(path_to_file, deserializer)))

    @staticmethod
    def from_recs_file(path_to_recs_file: Path, hero_dir: HeroDirectory) -> Collection:
        return Collection.__from_file(
            path_to_recs_file,
            hero_dir,
            lambda line: OwnedHero.from_rec(json.loads(line), hero_dir)
        )

    @staticmethod
    def from_squad_export_file(path_to_squad_export_file: Path, hero_dir: HeroDirectory) -> Collection:
        return Collection.__from_file(
            path_to_squad_export_file,
            hero_dir,
            lambda line: OwnedHero.from_squad_export(line, hero_dir)
        )
