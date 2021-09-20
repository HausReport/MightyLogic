import pytest

from HighGrowth import Discount
from MightyLogic.HighGrowth.Calculator import CompletionTier

# ======================================================================================================================
# CompletionTier
# ----------------------------------------------------------------------------------------------------------------------

t1 = CompletionTier.TIER_1
t10 = CompletionTier.TIER_10
t15 = CompletionTier.TIER_15


def test_aggregate_to():
    assert CompletionTier.aggregate_to(t1) == (t1.level_ups, t1.gems)
    assert CompletionTier.aggregate_to(t15) == (13_150, 193_250)


def test_aggregate_between():
    assert CompletionTier.aggregate_between(t1, t1) == (0, 0)
    assert CompletionTier.aggregate_between(None, t15) == CompletionTier.aggregate_to(t15)

    to_t10 = CompletionTier.aggregate_to(t10)
    to_t15 = CompletionTier.aggregate_to(t15)
    assert CompletionTier.aggregate_between(t10, t15) == (to_t15[0] - to_t10[0], to_t15[1] - to_t10[1])


def test_for_level_ups():
    with pytest.raises(RuntimeError, match="Cannot have negative level-ups"):
        CompletionTier.for_level_ups(-1)

    assert CompletionTier.for_level_ups(0) == (None, 0)
    assert CompletionTier.for_level_ups(9) == (None, 9)
    assert CompletionTier.for_level_ups(10) == (t1, 0)
    assert CompletionTier.for_level_ups(11) == (t1, 1)
    assert CompletionTier.for_level_ups(160) == (CompletionTier.TIER_5, 0)
    assert CompletionTier.for_level_ups(13_149) == (CompletionTier.TIER_14, t15.level_ups - 1)
    assert CompletionTier.for_level_ups(13_150) == (t15, 0)
    assert CompletionTier.for_level_ups(13_151) == (t15, 1)
    assert CompletionTier.for_level_ups(1_000_000) == (t15, 1_000_000 - CompletionTier.aggregate_to(t15)[0])


def test_next():
    assert CompletionTier.next(t1) == CompletionTier.TIER_2
    assert CompletionTier.next(t15) is None


# ======================================================================================================================
# Discount
# ----------------------------------------------------------------------------------------------------------------------

def test_both():
    assert Discount.both(Discount.NIGHTMARE, Discount.CRISIS) == 0.33  # 0.3276 rounded to 2 decimal places
