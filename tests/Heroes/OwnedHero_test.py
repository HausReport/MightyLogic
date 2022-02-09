import pytest

from MightyLogic.Heroes.Attributes.Alignment import Alignment
from MightyLogic.Heroes.Attributes.Gender import Gender
from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Attributes.Shape import Shape
from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.Heroes.Leveling.Level import Level
from MightyLogic.Heroes.OwnedHero import OwnedHero
from tests.Heroes.Hero_test import epic_hero, rare_hero, common_hero, legendary_hero


@pytest.fixture
def empty_oh(epic_hero) -> OwnedHero:
    return OwnedHero(epic_hero, Level(1, 0), 0)


@pytest.fixture
def rebornable_oh(common_hero) -> OwnedHero:
    return OwnedHero(common_hero, Level(11, 0), 0)


@pytest.fixture
def levelable_oh(legendary_hero) -> OwnedHero:
    return OwnedHero(legendary_hero, Level(1, 1), 100)


@pytest.fixture
def both_oh(rare_hero) -> OwnedHero:
    return OwnedHero(rare_hero, Level(11, 0), 10000)


# accessors

def test_owned_hero_accessors(empty_oh, epic_hero):
    assert empty_oh.hero == epic_hero
    assert empty_oh.level == Level(1, 0)
    assert empty_oh.souls == 0


# TODO: cost to next level
# TODO: reborn milestone
# TODO: leveling steps to


# tests

def test_owned_hero_can_reborn(empty_oh, rebornable_oh, levelable_oh, both_oh):
    assert empty_oh.can_reborn() is False
    assert rebornable_oh.can_reborn() is True
    assert levelable_oh.can_reborn() is False
    assert both_oh.can_reborn() is True


def test_owned_hero_can_level_up(empty_oh, rebornable_oh, levelable_oh, both_oh):
    # w/ infinite gold:
    assert empty_oh.can_level_up() is False
    assert rebornable_oh.can_level_up() is False
    assert levelable_oh.can_level_up() is True
    assert both_oh.can_level_up() is True

    # w/ constrained gold:
    assert levelable_oh.can_level_up(with_gold=1) is False
    assert levelable_oh.can_level_up(with_gold=100_000) is True


def test_owned_hero_can_level_up_after_reborn(empty_oh, rebornable_oh, levelable_oh, both_oh):
    # w/ infinite gold:
    assert empty_oh.can_level_up_after_reborn() is False
    assert rebornable_oh.can_level_up_after_reborn() is False
    assert levelable_oh.can_level_up_after_reborn() is False
    assert both_oh.can_level_up_after_reborn() is True

    # w/ constrained gold:
    assert both_oh.can_level_up_after_reborn(with_gold=1) is False
    assert both_oh.can_level_up_after_reborn(with_gold=100_000) is True


# mutators

# TODO: level up
# TODO: reborn


# static factories

def test_owned_hero_from_squad_export():
    mother_owl = Hero(22, "Mother Owl", Rarity.LEGENDARY, Shape.RANGED, Alignment.NATURE, Gender.FEMALE)
    hero_dir = HeroDirectory({mother_owl})

    oh = OwnedHero.from_squad_export(
        " 22: Mother Owl                   61/119  Level 14 Reborn 2 Unused Souls 24",
        hero_dir
    )

    assert oh.hero == mother_owl
    assert oh.level == Level(14, 2)
    assert oh.souls == 24
