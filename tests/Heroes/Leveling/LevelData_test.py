import pytest

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Leveling.LevelData import LevelData, LevelDatum


# TODO: init
# getitem

def test_getitem():
    data = LevelData.for_rarity(Rarity.COMMON)

    assert data[2] == LevelDatum(level_count=2, souls=25, gold=50, might=110, troops=22, required_league=30)


# is_valid_level_count

@pytest.mark.parametrize("rarity", [
    Rarity.COMMON,
    Rarity.RARE,
    Rarity.EPIC,
    Rarity.LEGENDARY,
])
def test_is_valid_level_count(rarity: Rarity):
    data = LevelData.for_rarity(rarity)

    assert not data.is_valid_level_count(data.min_level_count() - 1)

    for i in range(data.min_level_count(), data.max_level_count()):
        assert data.is_valid_level_count(i)

    assert not data.is_valid_level_count(data.max_level_count() + 1)


# max_level_count

@pytest.mark.parametrize("rarity,expected_max", [
    (Rarity.COMMON, 26),
    (Rarity.RARE, 31),
    (Rarity.EPIC, 31),
    (Rarity.LEGENDARY, 31),
])
def test_max_level_count(rarity: Rarity, expected_max: int):
    data = LevelData.for_rarity(rarity)

    assert data.max_level_count() == expected_max


# require_valid_level_count

@pytest.mark.parametrize("rarity", [
    Rarity.COMMON,
    Rarity.RARE,
    Rarity.EPIC,
    Rarity.LEGENDARY,
])
def test_require_valid_level_count(rarity: Rarity):
    data = LevelData.for_rarity(rarity)

    for i in range(data.min_level_count(), data.max_level_count()):
        data.require_valid_level_count(i)

    with pytest.raises(AssertionError, match="Level count must be"):
        data.require_valid_level_count(data.min_level_count() - 1)

    with pytest.raises(AssertionError, match="Level count must be"):
        data.require_valid_level_count(data.max_level_count() + 1)
