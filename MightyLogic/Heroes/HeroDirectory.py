from __future__ import annotations

import importlib.resources
import json
from pathlib import Path
from typing import Dict, Set, FrozenSet, Optional

import Heroes
from Heroes import create_secondary_indices, deserialize_lines
from Heroes.Hero import Hero


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

    def find_by_name(self, name: str) -> Optional[Hero]:
        return self.by_name[name] if name in self.by_name.keys() else None

    def find_by_num(self, num: int) -> Optional[Hero]:
        return self.by_num[num] if num in self.by_num.keys() else None

    def values(self) -> FrozenSet[Hero]:
        return self.heroes

    @staticmethod
    def default() -> HeroDirectory:
        with importlib.resources.path(Heroes, "HeroDirectory.recs") as path:
            return HeroDirectory.from_recs_file(path)

    @staticmethod
    def from_csv_file(path_to_csv_file: str) -> HeroDirectory:
        raise RuntimeError("Not yet implemented")

    @staticmethod
    def from_recs_file(path_to_recs_file: Path) -> HeroDirectory:
        return HeroDirectory(set(deserialize_lines(
            path_to_recs_file,
            lambda line: Hero.from_rec(json.loads(line)))
        ))
