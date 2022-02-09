import pytest

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.HeroSelector import HeroSelector, UnionSelector, IntersectionSelector

from tests.Heroes.HeroDirectory_test import hero_dir, singer, minstrel, bard, apollo
from tests.Heroes.Collection_test import collection


@pytest.fixture
def common_selector() -> HeroSelector:
    return HeroSelector.has_rarity(Rarity.COMMON)


@pytest.fixture
def rare_selector() -> HeroSelector:
    return HeroSelector.has_rarity(Rarity.RARE)


@pytest.fixture
def epic_selector() -> HeroSelector:
    return HeroSelector.has_rarity(Rarity.EPIC)


@pytest.fixture
def leg_selector() -> HeroSelector:
    return HeroSelector.has_rarity(Rarity.LEGENDARY)


# all_evolutions_to

def test_all_evolutions_to(hero_dir, collection, minstrel, apollo):
    assert HeroSelector.all_evolutions_to({"apollo"}).select(collection) == apollo.all_evolutions_to()
    assert HeroSelector.all_evolutions_to({"minstrel"}, inclusive=True).select(collection) \
           == minstrel.all_evolutions_to(include_self=True)


# exactly

def test_exactly(hero_dir, collection):
    assert HeroSelector.exactly(["grace", "eostre"]).select(collection) == {
        hero_dir.find("grace"),
        hero_dir.find("eostre")
    }


# has_rarity

def test_has_rarity(hero_dir, collection, common_selector):
    assert common_selector.select(collection) == set(
        hero
        for hero in hero_dir.values()
        if hero.rarity == Rarity.COMMON
    )


# add

def test_and(hero_dir, collection, common_selector, rare_selector, epic_selector, leg_selector):
    two: UnionSelector = common_selector + leg_selector
    assert two.of_selectors == [common_selector, leg_selector]
    assert sorted(two.select(collection)) == sorted(set(
        hero
        for hero in hero_dir.values()
        if hero.rarity in {Rarity.COMMON, Rarity.LEGENDARY}
    ))

    three: UnionSelector = common_selector + rare_selector + epic_selector
    assert three.of_selectors == [common_selector, rare_selector, epic_selector]
    assert sorted(three.select(collection)) == sorted(set(
        hero
        for hero in hero_dir.values()
        if hero.rarity in {Rarity.COMMON, Rarity.RARE, Rarity.EPIC}
    ))


# complement

def test_complement(hero_dir, collection, rare_selector, leg_selector):
    assert leg_selector.complement().select(collection) == set(
        hero
        for hero in hero_dir.values()
        if hero.rarity != Rarity.LEGENDARY
    )

    assert rare_selector.complement().complement() == rare_selector


# union

def test_intersection(collection, singer, minstrel, bard, apollo, common_selector):
    two: IntersectionSelector = common_selector & HeroSelector.exactly({singer, minstrel, bard})
    assert len(two.of_selectors) == 2
    assert sorted(two.select(collection)) == [singer]

    three: IntersectionSelector = common_selector & HeroSelector.exactly({singer, minstrel, bard}) \
            & HeroSelector.all_evolutions_to({apollo}, inclusive=True)
    assert len(three.of_selectors) == 3
    assert sorted(three.select(collection)) == [singer]
