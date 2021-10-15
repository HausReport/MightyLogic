from __future__ import annotations

from enum import unique, Enum
from typing import Dict, Optional, Tuple

from Heroes.Hero import LevelingSteps, Hero
from Heroes.OwnedHero import OwnedHero
from HighGrowth.Strategies import HighGrowthStrategy


@unique
class CompletionTier(Enum):
    level_ups: int
    gems: int

    TIER_1 = (    10,    50)
    TIER_2 = (    15,   100)
    TIER_3 = (    25,   200)
    TIER_4 = (    40,   350)
    TIER_5 = (    70,   650)
    TIER_6 = (   115, 1_100)
    TIER_7 = (   175, 1_800)
    TIER_8 = (   250, 3_000)
    TIER_9 = (   350, 4_500)
    TIER_10 = (  500, 7_500)
    TIER_11 = (  800, 12_000)
    TIER_12 = (1_300, 19_500)
    TIER_13 = (2_000, 30_000)
    TIER_14 = (3_000, 45_000)
    TIER_15 = (4_500, 67_500)

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, level_ups: int, gems: int):
        self.level_ups = level_ups
        self.gems = gems

    def __abs__(self):
        return self.level_ups

    def __le__(self, other: CompletionTier) -> bool:
        return abs(self) <= abs(other)

    def __lt__(self, other: CompletionTier) -> bool:
        return abs(self) <= abs(other)

    def __ge__(self, other: CompletionTier) -> bool:
        return abs(self) >= abs(other)

    def __gt__(self, other: CompletionTier) -> bool:
        return abs(self) > abs(other)

    def __str__(self):
        return f"{self.name} (level ups={self.level_ups:,}, gems={self.gems:,})"

    @staticmethod
    def aggregate_between(from_tier: Optional[CompletionTier], to_tier: CompletionTier) -> Tuple[int, int]:
        if from_tier and from_tier > to_tier:
            raise RuntimeError("From tier {from_tier} is greater than to tier {to_tier}")

        level_ups = 0
        gems = 0
        for __, tier in CompletionTier.__members__.items():
            if from_tier and tier <= from_tier:
                continue

            if tier > to_tier:
                break

            level_ups += tier.level_ups
            gems += tier.gems

        return level_ups, gems

    @staticmethod
    def aggregate_to(to_tier: CompletionTier) -> Tuple[int, int]:
        return CompletionTier.aggregate_between(None, to_tier)

    @staticmethod
    def for_level_ups(level_ups: int) -> Tuple[Optional[CompletionTier], int]:
        if level_ups < 0:
            raise RuntimeError(f"Cannot have negative level-ups (was: {level_ups})")

        remaining = level_ups
        previous_tier = None
        for __, tier in CompletionTier.__members__.items():
            if remaining < tier.level_ups:
                return previous_tier, remaining

            remaining -= tier.level_ups
            previous_tier = tier
        return (CompletionTier.TIER_15, remaining) if remaining >= 0 else (None, remaining)

    @staticmethod
    def next(from_tier: CompletionTier) -> Optional[CompletionTier]:
        previous_tier = None
        for __, tier in CompletionTier.__members__.items():
            if from_tier == previous_tier:
                return tier
            previous_tier = tier
        return None


class HighGrowthCalculation:
    strategy: HighGrowthStrategy
    gold_cap: Optional[int]
    gold_remaining: Optional[int]
    gold_discount: float
    gold_required: int = 0
    level_ups_goal: Optional[int]
    level_ups_completed: int = 0
    steps_by_hero: Dict[Hero, LevelingSteps] = dict()

    def __init__(self, strategy: HighGrowthStrategy, gold_cap: Optional[int] = None,
                 level_ups_goal: Optional[int] = None):
        self.strategy = strategy
        self.gold_cap = gold_cap
        self.gold_remaining = gold_cap
        self.gold_discount = strategy.gold_discount
        self.level_ups_goal = level_ups_goal

    def __str__(self):
        s = f"Strategy: {self.strategy}\n"

        s += f"Gold:\n" \
            f" - cap: " + ("none" if self.gold_cap is None else f"{self.gold_cap:,}") + "\n" \
            f" - discount: " + ("none" if self.gold_discount is None else f"{self.gold_discount * 100}%") + "\n" \
            f" - required: {self.gold_required:,}\n" \
            f" - remaining: " + ("infinite" if self.gold_remaining is None else f"{self.gold_remaining:,}") + "\n"

        completion_tier, level_ups_remaining = CompletionTier.for_level_ups(self.level_ups_completed)
        next_tier = CompletionTier.next(completion_tier)

        s += f"Level-ups:\n" \
             f" - goal: " + ("none" if self.level_ups_goal is None else f"{self.level_ups_goal:,}") + "\n" \
             f" - completed: {self.level_ups_completed:,}\n" \

        s += f"Tier and gems:\n" \
             f" - tier completed: {completion_tier}\n" \
             f" - total gems: {CompletionTier.aggregate_to(completion_tier)[1]:,}\n" \
             f" - next tier: {next_tier}\n" \
             f" - progress to next tier: {level_ups_remaining:,} of {next_tier.level_ups:,} level ups\n"
        s += "End state for each hero:\n"
        for i, (hero, steps) in enumerate(self.steps_by_hero.items()):
            s += f"{i + 1}. Take hero: {hero}\n    all the way to: {steps.final_level()}\n" \
                 f"    for: {steps.aggregate_cost()}\n"
        return s

    def add_steps(self, oh: OwnedHero, steps: LevelingSteps):
        if not steps:
            return

        hero = oh.hero
        if hero in self.steps_by_hero.keys():
            self.steps_by_hero[hero] += steps
        else:
            self.steps_by_hero[hero] = steps

        gold_required = steps.aggregate_cost().gold
        self.gold_required += gold_required
        if self.gold_remaining is not None:
            self.gold_remaining -= gold_required

        level_ups = steps.level_up_count()
        self.level_ups_completed += level_ups

    def calculate(self) -> HighGrowthCalculation:
        while self.can_level_up() and not self.satisfied_level_ups_goal():
            hero, steps = self.strategy.process_next(self.gold_remaining)
            self.add_steps(hero, steps)

        if not self.satisfied_level_ups_goal():
            raise RuntimeError(f"Not possible to reach {self.level_ups_goal} level ups with infinite gold; it is only"
                               f"possible to make {self.level_ups_completed} with the constraints provided.")

        return self

    def can_level_up(self) -> bool:
        return self.strategy.has_next(self.gold_remaining)

    def satisfied_level_ups_goal(self) -> bool:
        return self.level_ups_goal is None or self.level_ups_completed >= self.level_ups_goal

    @staticmethod
    def for_level_ups(strategy: HighGrowthStrategy, level_ups_goal: int) -> HighGrowthCalculation:
        return HighGrowthCalculation(strategy=strategy, level_ups_goal=level_ups_goal).calculate()

    @staticmethod
    def with_gold_cap(strategy: HighGrowthStrategy, gold_cap: Optional[int]) -> HighGrowthCalculation:
        return HighGrowthCalculation(strategy=strategy, gold_cap=gold_cap).calculate()
