from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Set, FrozenSet, Any, Callable, List, Iterable, Optional

from Heroes import create_secondary_index, per_group, group_by, stats_for, deserialize_lines
from Heroes.Hero import Rarity, Hero
from Heroes.HeroDirectory import HeroDirectory
from Heroes.OwnedHero import OwnedHero


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

    def summarize(self) -> Dict[str, Any]:
        by_rarity: Dict[Rarity, Set[OwnedHero]] = group_by(self.all_owned_heroes(), lambda oh: oh.hero.rarity,
                                                           include_all=True)
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


# ======================================================================================================================
# Selectors
# ----------------------------------------------------------------------------------------------------------------------

class HeroSelector:

    def __add__(self, other: HeroSelector) -> HeroSelector:
        return self.union(other)

    def __and__(self, other: HeroSelector) -> HeroSelector:
        return self.intersection(other)

    def __or__(self, other: HeroSelector) -> HeroSelector:
        return self.union(other)

    def complement(self) -> HeroSelector:
        # If we're already a complement, optimize by returning the underlying selector instead
        # (complement(complement(x)) == x)
        return self.of_selector if isinstance(self, ComplementSelector) else HeroSelector.complement_of(self)

    def describe(self, collection: Collection) -> str:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def intersection(self, other: HeroSelector) -> HeroSelector:
        # Optimize by flattening multiple intersection selectors
        self_selectors = self.of_selectors if isinstance(self, IntersectionSelector) else [self]
        other_selectors = other.of_selectors if isinstance(other, IntersectionSelector) else [other]
        return IntersectionSelector(self_selectors + other_selectors)

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        raise NotImplementedError("Method needs to be implemented by subclasses")

    def union(self, other: HeroSelector) -> HeroSelector:
        # Optimize by flattening multiple union selectors
        self_selectors = self.of_selectors if isinstance(self, UnionSelector) else [self]
        other_selectors = other.of_selectors if isinstance(other, UnionSelector) else [other]
        return self.union_of(self_selectors + other_selectors)

    @staticmethod
    def all_evolutions_to(hero_identifiers: Set[Any], inclusive: bool = False) -> HeroSelector:
        return EvolutionsSelector(frozenset(hero_identifiers), inclusive=inclusive)

    @staticmethod
    def complement_of(selector: HeroSelector) -> HeroSelector:
        return ComplementSelector(selector)

    @staticmethod
    def exactly(hero_identifiers: Set[Any]) -> HeroSelector:
        return ExactlySelector(frozenset(hero_identifiers))

    @staticmethod
    def has_rarity(rarity: Rarity) -> HeroSelector:
        return RaritySelector(rarity)

    @staticmethod
    def intersection_of(selectors: List[HeroSelector]) -> HeroSelector:
        return IntersectionSelector(selectors)

    @staticmethod
    def none() -> HeroSelector:
        return NoneSelector()

    @staticmethod
    def union_of(selectors: List[HeroSelector]) -> HeroSelector:
        return UnionSelector(selectors)


# -- identity operations

class NoneSelector(HeroSelector):

    def describe(self, collection: Collection) -> str:
        return "none"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        return frozenset()


@dataclass
class ExactlySelector(HeroSelector):
    hero_identifiers: FrozenSet[Any]
    __heroes: FrozenSet[Hero] = field(default=None)

    def describe(self, collection: Collection) -> str:
        return f"exactly {stringify_heroes(self.select(collection))}"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        if not self.__heroes:
            self.__heroes = frozenset(
                collection.hero_dir.find(identifier)
                for identifier in self.hero_identifiers
            )
        return self.__heroes


# -- set operations

@dataclass
class ComplementSelector(HeroSelector):
    of_selector: HeroSelector

    def describe(self, collection: Collection) -> str:
        return f"complement of <{self.of_selector.describe(collection)}>"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        return frozenset(
            hero
            for hero in collection.all_heroes()
            if hero not in self.of_selector.select(collection)
        )


@dataclass
class SetOpSelector(HeroSelector):
    operation_name: str
    operation_callable: Callable[[Set[Hero], FrozenSet[Hero]], Set[Hero]]
    of_selectors: List[HeroSelector]

    def describe(self, collection: Collection) -> str:
        prefix = "\n   - "
        nested_descriptions = prefix.join(f"{selector.describe(collection)}" for selector in self.of_selectors)
        return f"{self.operation_name} of:{prefix}{nested_descriptions}"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        heroes = None
        for selector in self.of_selectors:
            selector_result = selector.select(collection)
            heroes = selector_result if heroes is None else self.operation_callable(heroes, selector_result)
        return frozenset() if heroes is None else frozenset(heroes)


class IntersectionSelector(SetOpSelector):
    def __init__(self, of_selectors: List[HeroSelector]):
        super(IntersectionSelector, self).__init__(
            operation_name="intersection",
            operation_callable=lambda aggregate, individual: aggregate.intersection(individual),
            of_selectors=of_selectors
        )


class UnionSelector(SetOpSelector):

    def __init__(self, of_selectors: List[HeroSelector]):
        super(UnionSelector, self).__init__(
            operation_name="union",
            operation_callable=lambda aggregate, individual: aggregate.union(individual),
            of_selectors=of_selectors
        )


# -- hero attributes

@dataclass
class EvolutionsSelector(HeroSelector):
    hero_identifiers: FrozenSet[Any]
    inclusive: bool
    __target_heroes: FrozenSet = field(default=None)
    __heroes: FrozenSet[Hero] = field(default=None)

    def describe(self, collection: Collection) -> str:
        heroes = self.select(collection)
        return f"evolutions to {stringify_heroes(self.__target_heroes)} " \
               f"({'inclusive' if self.inclusive else 'exclusive'}), i.e. {stringify_heroes(heroes)}"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        if not self.__heroes:
            self.__target_heroes = ExactlySelector(self.hero_identifiers).select(collection)
            self.__heroes = frozenset(
                from_hero
                for to_hero in self.__target_heroes
                for from_hero in to_hero.all_evolutions_to(include_self=self.inclusive)
            )
        return self.__heroes


@dataclass
class RaritySelector(HeroSelector):
    rarity: Rarity
    __heroes: FrozenSet[Hero] = field(default=None)

    def describe(self, collection: Collection) -> str:
        return f"all {self.rarity} heroes, i.e. {stringify_heroes(self.select(collection))}"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        if not self.__heroes:
            self.__heroes = frozenset(
                hero
                for hero in collection.all_heroes()
                if hero.rarity == self.rarity
            )
        return self.__heroes
