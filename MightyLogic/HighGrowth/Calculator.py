from __future__ import annotations

from typing import Dict, Optional, FrozenSet

from Heroes.Hero import LevelingSteps, Hero
from Heroes.OwnedHero import OwnedHero
from HighGrowth.Strategies import HighGrowthStrategy


class HighGrowthCalculation:
    strategy: HighGrowthStrategy
    gold_remaining: Optional[int]
    gold_discount: int
    gold_required: int = 0
    completion_tier: int = 0  # TODO
    level_ups_completed: int = 0
    level_ups_remaining: int = 0  # TODO
    steps_by_hero: Dict[Hero, LevelingSteps] = dict()

    def __init__(self, strategy: HighGrowthStrategy, gold_cap: Optional[int]):
        self.strategy = strategy
        self.gold_remaining = gold_cap
        self.gold_discount = strategy.gold_discount

    def __str__(self):
        s = f"Gold: required={self.gold_required}, remaining={self.gold_remaining}, discount="
        s += "NONE" if self.gold_discount is None else f"{self.gold_discount}%"
        s += f"\nLevel ups: completed={self.level_ups_completed}, remaining={self.level_ups_remaining}," \
             f" tier={self.completion_tier}\n"
        s += f"Strategy: {self.strategy}\n"
        s += "End state for each hero:\n"
        for i, (hero, steps) in enumerate(self.steps_by_hero.items()):
            s += f"{i + 1}. Take hero: {hero}\n    all the way to: {steps.final_level()}\n" \
                 f"    for: {steps.aggregate_cost()}\n"
        return s

    def add_steps(self, owned_hero: OwnedHero, steps: LevelingSteps):
        if not steps:
            return

        hero = owned_hero.hero
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

    @staticmethod
    def from_strategy(strategy: HighGrowthStrategy, gold_cap: Optional[int]) -> HighGrowthCalculation:
        calc = HighGrowthCalculation(strategy, gold_cap)
        while strategy.has_next(calc.gold_remaining):
            hero, steps = strategy.process_next(calc.gold_remaining)
            calc.add_steps(hero, steps)
        return calc
