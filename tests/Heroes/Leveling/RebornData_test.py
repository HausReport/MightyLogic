import pytest

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Leveling.RebornData import RebornData, RebornDatum


# constructor

def test_init():
    all_zeroes = RebornDatum.zero()
    all_ones = RebornDatum(reborn_count=1, required_level=1, might=1, troops=1)
    all_twos = RebornDatum(reborn_count=2, required_level=2, might=2, troops=2)

    # Legit
    assert RebornData([all_zeroes])
    assert RebornData([all_zeroes, all_ones])

    # Empty
    with pytest.raises(AssertionError, match="Not enough data"):
        RebornData([])

    # Missing R0
    with pytest.raises(AssertionError, match="reborn count 0"):
        RebornData([all_ones])

    # Reborn decreasing
    with pytest.raises(AssertionError, match="consecutive"):
        RebornData([all_zeroes, all_ones, all_twos, all_twos.with_changes(reborn_count=1)])

    # Reborn increasing too quickly
    with pytest.raises(AssertionError, match="consecutive"):
        RebornData([all_zeroes, all_twos])

    # Level not increasing
    with pytest.raises(AssertionError, match="Required level"):
        RebornData([all_zeroes, all_ones, all_twos.with_changes(required_level=1)])

    # Might not increasing
    with pytest.raises(AssertionError, match="Might"):
        RebornData([all_zeroes, all_ones, all_twos.with_changes(might=1)])

    # Troops not increasing
    with pytest.raises(AssertionError, match="Troops"):
        RebornData([all_zeroes, all_ones, all_twos.with_changes(troops=1)])


# getitem

def test_getitem():
    data = RebornData.for_rarity(Rarity.COMMON)

    assert data[1] == RebornDatum(reborn_count=1, required_level=11, troops=24, might=100)


# cumulative_might

@pytest.mark.parametrize("rarity,expected_at_max", [
    (Rarity.COMMON, 1_000),
    (Rarity.RARE, 1_500),
    (Rarity.EPIC, 2_300),
    (Rarity.LEGENDARY, 4_100),
])
def test_cumulative_might(rarity: Rarity, expected_at_max: int):
    data = RebornData.for_rarity(rarity)

    assert data.cumulative_might(0) == 0
    assert data.cumulative_might(data.max_reborn_count()) == expected_at_max


# cumulative_troops

@pytest.mark.parametrize("rarity,expected_at_max", [
    (Rarity.COMMON, 307),
    (Rarity.RARE, 618),
    (Rarity.EPIC, 2_665),
    (Rarity.LEGENDARY, 5_661),
])
def test_cumulative_troops(rarity: Rarity, expected_at_max: int):
    data = RebornData.for_rarity(rarity)

    assert data.cumulative_troops(0) == 0
    assert data.cumulative_troops(data.max_reborn_count()) == expected_at_max


# is_valid_reborn_count

@pytest.mark.parametrize("rarity", [
    Rarity.COMMON,
    Rarity.RARE,
    Rarity.EPIC,
    Rarity.LEGENDARY,
])
def test_is_valid_reborn_count_given_common(rarity: Rarity):
    data = RebornData.for_rarity(rarity)

    assert not data.is_valid_reborn_count(data.min_reborn_count() - 1)

    for i in range(data.min_reborn_count(), data.max_reborn_count()):
        assert data.is_valid_reborn_count(i)

    assert not data.is_valid_reborn_count(data.max_reborn_count() + 1)


# max_reborn_count

@pytest.mark.parametrize("rarity,expected_max", [
    (Rarity.COMMON, 4),
    (Rarity.RARE, 4),
    (Rarity.EPIC, 5),
    (Rarity.LEGENDARY, 5),
])
def test_max_reborn_count(rarity: Rarity, expected_max: int):
    data = RebornData.for_rarity(rarity)

    assert data.max_reborn_count() == expected_max


# require_valid_reborn_count

@pytest.mark.parametrize("rarity", [
    Rarity.COMMON,
    Rarity.RARE,
    Rarity.EPIC,
    Rarity.LEGENDARY,
])
def test_require_valid_reborn_count(rarity: Rarity):
    data = RebornData.for_rarity(rarity)

    for i in range(data.min_reborn_count(), data.max_reborn_count()):
        data.require_valid_reborn_count(i)

    with pytest.raises(AssertionError, match="Reborn count must be"):
        data.require_valid_reborn_count(data.min_reborn_count() - 1)

    with pytest.raises(AssertionError, match="Reborn count must be"):
        data.require_valid_reborn_count(data.max_reborn_count() + 1)
