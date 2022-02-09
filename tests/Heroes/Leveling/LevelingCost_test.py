import pytest

from MightyLogic.Heroes.Leveling.LevelingCost import LevelingCost


@pytest.fixture
def s_1_g_10() -> LevelingCost:
    return LevelingCost(souls=1, gold=10)


@pytest.fixture
def s_2_g_20() -> LevelingCost:
    return LevelingCost(souls=2, gold=20)


@pytest.fixture
def s_3_g_30() -> LevelingCost:
    return LevelingCost(souls=3, gold=30)


@pytest.fixture
def free() -> LevelingCost:
    return LevelingCost.free()


# constructor

@pytest.mark.parametrize("__description,souls,gold", [
    ("souls < min", 0, 1),
    ("gold < min", 1, 0),
])
def test_level_constructor(__description, souls, gold):
    with pytest.raises(RuntimeError):
        LevelingCost(souls, gold)


# accessors

def test_leveling_cost_accessors(s_1_g_10):
    assert s_1_g_10.gold == 10
    assert s_1_g_10.souls == 1


# comparators

def test_leveling_cost_comparators(s_1_g_10, s_2_g_20, s_3_g_30):
    assert list(sorted([s_3_g_30, s_1_g_10, s_2_g_20, s_1_g_10])) == [
        s_1_g_10,
        s_1_g_10,
        s_2_g_20,
        s_3_g_30
    ]


# static factories

def test_leveling_cost_free(free):
    assert free.gold == 0
    assert free.souls == 0
