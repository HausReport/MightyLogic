from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Set, FrozenSet, Any, Callable

from Heroes import create_secondary_indices, per_group, group_by, stats_for, deserialize_lines
from Heroes.Hero import Rarity
from Heroes.HeroDirectory import HeroDirectory
from Heroes.OwnedHero import OwnedHero


class OwnedHeroDirectory:
    owned_heroes = FrozenSet[OwnedHero]
    by_name: Dict[str, OwnedHero]
    by_num: Dict[int, OwnedHero]

    def __init__(self, owned_heroes: Set[OwnedHero]):
        self.owned_heroes = frozenset(owned_heroes)
        self.by_num, self.by_name = create_secondary_indices(owned_heroes, [
            lambda oh: oh.hero.num,
            lambda oh: oh.hero.name
        ])

    def find_by_name(self, name: str) -> OwnedHero:
        return self.by_name[name]

    def find_by_num(self, num: int) -> OwnedHero:
        return self.by_num[num]

    def summarize(self) -> Dict[str, Any]:
        by_rarity: Dict[Rarity, Set[OwnedHero]] = group_by(self.values(), lambda oh: oh.hero.rarity, include_all=True)
        return {
            "count_by_rarity": per_group(by_rarity, lambda heroes: len(heroes)),
            "level_by_rarity": per_group(by_rarity, lambda heroes: stats_for(list(oh.level for oh in heroes))),
        }

    def values(self) -> FrozenSet[OwnedHero]:
        return self.owned_heroes

    @staticmethod
    def __from_file(path_to_file: Path, deserializer: Callable[[str], OwnedHero]) -> OwnedHeroDirectory:
        return OwnedHeroDirectory(set(deserialize_lines(path_to_file, deserializer)))

    @staticmethod
    def from_recs_file(path_to_recs_file: Path, hero_dir: HeroDirectory) -> OwnedHeroDirectory:
        return OwnedHeroDirectory.__from_file(
            path_to_recs_file,
            lambda line: OwnedHero.from_rec(json.loads(line), hero_dir)
        )

    @staticmethod
    def from_squad_export_file(path_to_squad_export_file: Path, hero_dir: HeroDirectory) -> OwnedHeroDirectory:
        return OwnedHeroDirectory.__from_file(
            path_to_squad_export_file,
            lambda line: OwnedHero.from_squad_export(line, hero_dir)
        )
