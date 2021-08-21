from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Set, FrozenSet, Any, Callable, List

from Heroes import create_secondary_index, per_group, group_by, stats_for, deserialize_lines
from Heroes.Hero import Rarity, Hero
from Heroes.HeroDirectory import HeroDirectory
from Heroes.OwnedHero import OwnedHero


class HeroSelector:

    def __add__(self, other: HeroSelector) -> HeroSelector:
        return self.all_of([self, other])

    def select(self, collection: Collection) -> Set[Hero]:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    @staticmethod
    def all_evolutions_to(hero_identifiers: Set[Any], including: bool = False) -> HeroSelector:
        return EvolutionsSelector(frozenset(hero_identifiers), including=including)

    @staticmethod
    def all_of(selectors: List[HeroSelector]) -> HeroSelector:
        return UnionSelector(selectors)

    @staticmethod
    def exactly(hero_identifiers: Set[Any]) -> HeroSelector:
        return ExactlySelector(frozenset(hero_identifiers))

    @staticmethod
    def has_rarity(rarity: Rarity) -> HeroSelector:
        return RaritySelector(rarity)

    @staticmethod
    def none() -> HeroSelector:
        return NoneSelector()


class NoneSelector(HeroSelector):

    def select(self, collection: Collection) -> Set[Hero]:
        return set()


@dataclass()
class UnionSelector(HeroSelector):
    selectors: List[HeroSelector]

    def select(self, collection: Collection) -> Set[Hero]:
        return set(
            hero
            for selector in self.selectors
            for hero in selector.select(collection)
        )


@dataclass
class ExactlySelector(HeroSelector):
    hero_identifiers: FrozenSet[Any]

    def select(self, collection: Collection) -> Set[Hero]:
        return set(
            collection.hero_dir.find(identifier)
            for identifier in self.hero_identifiers
        )


@dataclass
class EvolutionsSelector(HeroSelector):
    hero_identifiers: FrozenSet[Any]
    including: bool

    def select(self, collection: Collection) -> Set[Hero]:
        return set(
            from_hero
            for to_hero in ExactlySelector(self.hero_identifiers).select(collection)
            for from_hero in to_hero.all_evolutions_to(include_self=self.including)
        )


@dataclass
class RaritySelector(HeroSelector):
    rarity: Rarity

    def select(self, collection: Collection) -> Set[Hero]:
        return set(
            hero
            for hero in collection.all_heroes()
            if hero.rarity == self.rarity
        )


class Collection:
    hero_dir: HeroDirectory
    owned_heroes = FrozenSet[OwnedHero]
    by_num: Dict[int, OwnedHero]

    def __init__(self, hero_dir: HeroDirectory, owned_heroes: Set[OwnedHero]):
        self.hero_dir = hero_dir
        self.owned_heroes = frozenset(owned_heroes)
        self.by_num = create_secondary_index(owned_heroes, lambda oh: oh.hero.num)

    def all_heroes(self) -> FrozenSet[Hero]:
        return self.hero_dir.values()

    def all_owned_heroes(self) -> FrozenSet[OwnedHero]:
        return self.owned_heroes

    def find(self, identifier: Any) -> OwnedHero:
        hero = self.hero_dir.find(identifier)
        return self.by_num[hero.num]

    def find_by_name(self, name: str) -> OwnedHero:
        hero = self.hero_dir.find_by_name(name)
        return self.by_num[hero.num]

    def find_by_num(self, num: int) -> OwnedHero:
        return self.by_num[num]

    def resolve(self, selector: HeroSelector) -> Set[Hero]:
        return selector.select(self)

    def summarize(self) -> Dict[str, Any]:
        by_rarity: Dict[Rarity, Set[OwnedHero]] = group_by(self.all_owned_heroes(), lambda oh: oh.hero.rarity, include_all=True)
        return {
            "count_by_rarity": per_group(by_rarity, lambda heroes: len(heroes)),
            "level_by_rarity": per_group(by_rarity, lambda heroes: stats_for(list(oh.level for oh in heroes))),
        }

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
