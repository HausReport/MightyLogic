from __future__ import annotations

from dataclasses import field, dataclass
from typing import FrozenSet, Set, Any, Optional, List, Callable

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Collection import Collection, stringify_heroes
from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.OwnedHero import OwnedHero


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
    def has_level(level_count: int, reborn_count: Optional[int] = None) -> HeroSelector:
        return LevelSelector(level_count, reborn_count)

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
class LevelSelector(HeroSelector):
    level_count: int
    reborn_count: Optional[int] = None
    __heroes: FrozenSet[Hero] = field(default=None)

    def describe(self, collection: Collection) -> str:
        return f"all level {self.level_count} @ reborn {'ANY' if self.reborn_count is None else self.reborn_count}" \
               f" heroes, i.e. {stringify_heroes(self.select(collection))}"

    def select(self, collection: Collection) -> FrozenSet[Hero]:
        if not self.__heroes:
            self.__heroes = frozenset(
                oh.hero
                for oh in collection.all_owned_heroes()
                if self.__test(oh)
            )
        return self.__heroes

    def __test(self, oh: OwnedHero):
        right_level = oh.level.level_count == self.level_count
        right_reborn = self.reborn_count is None or oh.level.reborn_count == self.reborn_count
        return right_level and right_reborn


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
