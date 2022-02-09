import pytest

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Leveling.Level import Level


@pytest.fixture
def l_1_rb_0() -> Level:
    return Level(1, 0)


@pytest.fixture
def l_2_rb_0() -> Level:
    return Level(2, 0)


@pytest.fixture
def l_1_rb_1() -> Level:
    return Level(1, 1)


@pytest.fixture
def l_2_rb_1() -> Level:
    return Level(2, 1)


# constructor

@pytest.mark.parametrize("__description,level_count,reborn_count", [
    ("level < min", 0, 0),
    ("level > max", 32, 0),
    ("reborn < min", 1, -1),
    ("reborn > max", 1, 6)
])
def test_level_constructor(__description, level_count, reborn_count):
    with pytest.raises(AssertionError):
        Level(level_count, reborn_count)


# accessors

def test_level_accessors(l_1_rb_0):
    assert l_1_rb_0.level_count == 1
    assert l_1_rb_0.reborn_count == 0


def test_might():
    assert Level(26, 4).might_for(Rarity.COMMON) == 2_150
    assert Level(26, 4).might_for(Rarity.RARE) == 3_200
    assert Level(31, 5).might_for(Rarity.EPIC) == 5_625
    assert Level(31, 5).might_for(Rarity.LEGENDARY) == 9_090


def test_troops():
    assert Level(26, 4).troops_for(Rarity.COMMON) == 557
    assert Level(26, 4).troops_for(Rarity.RARE) == 1_018
    assert Level(31, 5).troops_for(Rarity.EPIC) == 4_660
    assert Level(31, 5).troops_for(Rarity.LEGENDARY) == 10_316


# mutators

def test_level_reborn(l_2_rb_0, l_1_rb_1):
    reborn = l_2_rb_0.reborn()
    assert reborn == l_1_rb_1  # reborn resets level to 0
    assert l_2_rb_0 == Level(2, 0)  # reborn should not mutate the original level


def test_level_level_up(l_1_rb_0, l_2_rb_0):
    leveled = l_1_rb_0.level_up()
    assert leveled == l_2_rb_0  # leveling doesn't increase reborn
    assert l_1_rb_0 == Level(1, 0)  # leveling should not mutate the original level


# comparators

def test_level_comparators(l_1_rb_0, l_2_rb_0, l_1_rb_1, l_2_rb_1):
    assert list(sorted([l_2_rb_0, l_1_rb_0, l_2_rb_1, l_1_rb_1, l_2_rb_1])) == [
        l_1_rb_0,
        l_2_rb_0,
        l_1_rb_1,
        l_2_rb_1,
        l_2_rb_1
    ]
