import pytest

from MightyLogic.Heroes.Leveling.Level import Level
from MightyLogic.Heroes.Leveling.LevelingCost import LevelingCost
from MightyLogic.Heroes.Leveling.LevelingSteps import LevelingSteps


@pytest.fixture
def test_steps() -> LevelingSteps:
    return LevelingSteps([
        (Level(2, 0), LevelingCost(souls=1, gold=10)),
        (Level(1, 1), LevelingCost.free()),
        (Level(2, 1), LevelingCost(souls=3, gold=30))
    ])


# aggregate cost

def test_leveling_steps_aggregate_cost(test_steps):
    aggregate_cost = test_steps.aggregate_cost()
    assert aggregate_cost.souls == 4
    assert aggregate_cost.gold == 40


# final level

def test_leveling_steps_final_level(test_steps):
    assert test_steps.final_level() == Level(2, 1)


# level up count

def test_leveling_steps_level_up_count(test_steps):
    assert test_steps.level_up_count() == 2  # reborn step doesn't count
