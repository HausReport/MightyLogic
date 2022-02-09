import pytest

from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.Attributes.Gender import Gender
from MightyLogic.Heroes.Attributes.Alignment import Alignment
from MightyLogic.Heroes.Attributes.Shape import Shape
from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Leveling.LevelingCost import LevelingCost
from MightyLogic.Heroes.Leveling.LevelingSteps import LevelingSteps
from MightyLogic.Heroes.Leveling.Level import Level


@pytest.fixture
def common_hero() -> Hero:
    return Hero(1, "Common -.-", Rarity.COMMON, Shape.MELEE, Alignment.CHAOS, Gender.FEMALE)


@pytest.fixture
def rare_hero() -> Hero:
    return Hero(2, "Rare :)", Rarity.RARE, Shape.RANGED, Alignment.ORDER, Gender.MALE)


@pytest.fixture
def epic_hero() -> Hero:
    return Hero(3, "Epic :D", Rarity.EPIC, Shape.BUILDING, Alignment.CHAOS, Gender.SEXLESS)


@pytest.fixture
def legendary_hero() -> Hero:
    return Hero(4, "Legendary :)))", Rarity.LEGENDARY, Shape.MELEE, Alignment.NATURE, Gender.FEMALE)


# accessors

def test_hero_accessors(epic_hero):
    assert epic_hero.num == 3
    assert epic_hero.name == "Epic :D"
    assert epic_hero.rarity == Rarity.EPIC
    assert epic_hero.shape == Shape.BUILDING
    assert epic_hero.alignment == Alignment.CHAOS
    assert epic_hero.gender == Gender.SEXLESS


# reborn milestone

def test_hero_reborn_milestone(common_hero, rare_hero, epic_hero, legendary_hero):
    assert common_hero.reborn_milestone(Level(1, 0)) == 11
    assert rare_hero.reborn_milestone(Level(1, 1)) == 16
    assert epic_hero.reborn_milestone(Level(2, 0)) == 6
    assert legendary_hero.reborn_milestone(Level(2, 1)) == 11


# leveling cost

def test_hero_leveling_cost(common_hero, rare_hero, epic_hero, legendary_hero):
    assert common_hero.leveling_cost(Level(1, 0)) == LevelingCost.free()
    assert rare_hero.leveling_cost(Level(2, 1)) == LevelingCost(25, 100)
    assert epic_hero.leveling_cost(Level(6, 2)) == LevelingCost(80, 1900)
    assert legendary_hero.leveling_cost(Level(21, 2)) == LevelingCost(1700, 48000)


# leveling steps

def test_hero_leveling_steps_same_reborn_(epic_hero):
    assert epic_hero.leveling_steps(Level(1, 0), Level(6, 0)) == LevelingSteps([
        (Level(2, 0), LevelingCost(15, 300)),
        (Level(3, 0), LevelingCost(30, 600)),
        (Level(4, 0), LevelingCost(45, 900)),
        (Level(5, 0), LevelingCost(60, 1400)),
        (Level(6, 0), LevelingCost(80, 1900)),
    ])


def test_hero_leveling_steps_different_reborn(epic_hero):
    with pytest.raises(AssertionError, match="same reborn count"):
        epic_hero.leveling_steps(Level(1, 0), Level(2, 1))


def test_hero_leveling_steps_from_gt_to(epic_hero):
    with pytest.raises(AssertionError, match="must be lower than"):
        epic_hero.leveling_steps(Level(2, 0), Level(1, 0))
