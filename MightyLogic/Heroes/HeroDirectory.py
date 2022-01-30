from __future__ import annotations

import csv
import importlib.resources
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set, FrozenSet, Optional, Any

from MightyLogic import Heroes
from MightyLogic.Heroes import create_secondary_indices, deserialize_lines
from MightyLogic.Heroes.Hero import Hero


class HeroDirectory:
    heroes = FrozenSet[Hero]
    by_name: Dict[str, Hero]
    by_num: Dict[int, Hero]

    def __init__(self, heroes: Set[Hero]):
        self.heroes = frozenset(heroes)
        self.by_num, self.by_name = create_secondary_indices(heroes, [
            lambda hero: hero.num,
            lambda hero: hero.name
        ])

    def find(self, identifier: Any) -> Optional[Hero]:
        if isinstance(identifier, Hero):
            return identifier

        # We only know how to work with ints and strs
        if not (isinstance(identifier, str) or isinstance(identifier, int)):
            raise RuntimeError(f"Not sure how to find hero given identifier {identifier}")

        maybe_hero: Optional[Hero] = None
        identifier_s = str(identifier)

        # p1: numerical lookups
        if identifier_s.isnumeric():
            maybe_hero = self.find_by_num(int(identifier))

        # p2: exact, case-sensitive, name matches
        if not maybe_hero:
            maybe_hero = self.find_by_name(identifier_s)

        # p3: exact, case-insensitive, name matches
        if not maybe_hero:
            maybe_hero = next((hero for hero in self.heroes if hero.name.lower() == identifier_s.lower()), None)

        # p4: word matches
        word_re = re.compile(f"\\b{identifier_s}\\b", flags=re.IGNORECASE)
        if not maybe_hero:
            maybe_hero = next((hero for hero in self.heroes if word_re.search(hero.name)), None)

        # p5: first substring match
        if not maybe_hero:
            maybe_hero = next((hero for hero in self.heroes if identifier_s.lower() in hero.name.lower()), None)

        return maybe_hero

    def find_by_name(self, name: str) -> Optional[Hero]:
        foo = name
        # if foo.startswith("Eostre"):
        #     foo = "Eostre, the Dawn Glow"
        return self.by_name[foo] if foo in self.by_name.keys() else None

    def find_by_num(self, num: int) -> Optional[Hero]:
        return self.by_num[num] if num in self.by_num.keys() else None

    def values(self) -> FrozenSet[Hero]:
        return self.heroes

    def to_csv_file(self, path_to_csv_file: Path) -> None:
        with path_to_csv_file.open("w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=[
                "id",
                "name",
                "rarity",
                "alignment",
                "gender",
                "shape",
                "evolves_to"
            ])
            writer.writeheader()
            for hero in self.heroes:
                writer.writerow(hero.to_dict())

    @staticmethod
    def default() -> HeroDirectory:
        with importlib.resources.path(Heroes, "HeroDirectory.csv") as path:
            return HeroDirectory.from_csv_file(path)

    @staticmethod
    def from_csv_file(path_to_csv_file: Path) -> HeroDirectory:
        def find_all_by_num(nums: Set[int]) -> FrozenSet[Hero]:
            return frozenset(hero_dir.find_by_num(num) for num in nums if num)

        with path_to_csv_file.open(newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            heroes: Set[Hero] = set()
            evolves_to_by_num: Dict[int, Set[int]] = dict()
            evolves_from_by_num: Dict[int, Set[int]] = defaultdict(set)
            for row in reader:
                hero = Hero.from_csv(row)
                heroes.add(hero)

                evolves_to = json.loads(row["evolves_to"])
                evolves_to_by_num[hero.num] = evolves_to
                for to_num in evolves_to:
                    evolves_from_by_num[to_num].add(hero.num)

            hero_dir = HeroDirectory(heroes)
            for hero in hero_dir.values():
                hero.evolves_to = find_all_by_num(evolves_to_by_num[hero.num])
                hero.evolves_from = find_all_by_num(evolves_from_by_num[hero.num])
            return hero_dir

    @staticmethod
    def from_recs_file(path_to_recs_file: Path) -> HeroDirectory:
        return HeroDirectory(set(deserialize_lines(
            path_to_recs_file,
            lambda line: Hero.from_rec(json.loads(line)))
        ))
