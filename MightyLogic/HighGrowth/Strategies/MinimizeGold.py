from typing import Tuple, Optional

from Heroes.Collection import Collection, HeroSelector
from Heroes.Hero import LevelingSteps, Rarity
from Heroes.OwnedHero import OwnedHero
from HighGrowth.IndexedMinHeap import IndexedMinHeap
from HighGrowth.Strategies import HighGrowthStrategy


class MinimizeGold(HighGrowthStrategy):
    """
    Always level up the cheapest hero, and reborn everything as soon as possible. At some point this should normalize to
    getting everything to a consistent level, i.e. the point at which the gold cost for level-ups converge: L6 for
    legendary ~= L7/8 for epic/rare ~= L11 for common.
    """
    minimize: HeroSelector
    never_reborn: HeroSelector
    unconstrained_cost_heap: IndexedMinHeap
    minimized_cost_heap: IndexedMinHeap

    def __init__(self, collection: Collection, exclude: HeroSelector = HeroSelector.none(),
                 minimize: HeroSelector = HeroSelector.none(), never_reborn: HeroSelector = HeroSelector.none(),
                 gold_discount: Optional[float] = None):
        super(MinimizeGold, self).__init__(collection, exclude, gold_discount)

        self.minimize = minimize
        self.never_reborn = never_reborn

        self.unconstrained_cost_heap = IndexedMinHeap(
            index_fn=MinimizeGold.extract_rarity,
            prioritization_fn=MinimizeGold.rank_by_cost)
        self.minimized_cost_heap = IndexedMinHeap(
            index_fn=MinimizeGold.extract_rarity,
            prioritization_fn=MinimizeGold.rank_by_cost)  # this only works because cost scale proportional to level

        for oh in collection.all_owned_heroes():
            self.__offer(oh)

    def __str__(self):
        return "minimize gold, i.e. always level up the cheapest hero, and reborn everything as soon as possible\n" \
               f" - exclude: {self.exclude.describe(self.collection)}\n" \
               f" - minimize: {self.minimize.describe(self.collection)}\n" \
               f" - never reborn: {self.never_reborn.describe(self.collection)}"

    @staticmethod
    def __cost(oh: OwnedHero) -> int:
        # TODO: Factor in reborns... somehow
        return 10_000_000 if oh is None else oh.cost_to_next_level().gold

    def __level_up(self, oh: OwnedHero, remaining_gold: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        steps = None

        # If reborning means we can level up, do so - this will always be cheaper
        if self.__should_reborn(oh, remaining_gold, self.gold_discount):
            oh.reborn()

        # If we an level up, do so
        if oh.can_level_up(remaining_gold, self.gold_discount):
            steps = oh.level_up(remaining_gold, self.gold_discount)
            self.__offer(oh)

        return oh, steps

    def __offer(self, oh: OwnedHero):
        if oh.hero in self.exclude.select(self.collection):
            return

        # Reborn all heroes if we can level up them up afterwards (cost is lowest after a reborn)
        # FIXME: Need to factor in available gold otherwise we'll reborn for no reason
        # FIXME: There becomes a point where the amortized cost of leveling above a reborn milestone is optimal
        if self.__should_reborn(oh, None, None):
            oh.reborn()

        # Push the hero onto one of our heaps
        if oh.hero in self.minimize.select(self.collection):
            self.minimized_cost_heap.push(oh)
        else:
            self.unconstrained_cost_heap.push(oh)

    def __should_reborn(self, oh: OwnedHero, with_gold: Optional[int], gold_discount: Optional[float]) -> bool:
        eligible_to_reborn = oh.hero not in self.never_reborn.select(self.collection)
        can_level_up_afterwards = oh.can_level_up_after_reborn(with_gold=with_gold, gold_discount=gold_discount)
        return eligible_to_reborn and can_level_up_afterwards

    def has_next(self, remaining_gold: Optional[int]) -> bool:
        # This check isn't 100% accurate (theoretically we should peek a the next value and ensure we have enough gold
        # to level it up), but it's still a valid terminal condition (we just end up exhausting the heap)
        return (remaining_gold is None or remaining_gold > 0) and self.unconstrained_cost_heap  # FIXME: min termination

    def process_next(self, remaining_gold: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        min_unconstrained_hero: OwnedHero = self.unconstrained_cost_heap.peek()
        cost_of_min_unconstrained = self.__cost(min_unconstrained_hero)

        min_minimized_hero: OwnedHero = self.minimized_cost_heap.peek()
        cost_of_min_minimized = self.__cost(min_minimized_hero)

        # TODO: There should be special prioritization for getting rebornable min heroes thru a milestone and back to L1
        if cost_of_min_minimized < cost_of_min_unconstrained:
            # Only level up if doing so will not make the level of this hero == the level of the cheapest (i.e.
            # lowest-leveled) hero of the same rarity (we always want to be the lowest level for this rarity)
            min_unconstrained_hero_of_same_rarity: OwnedHero = \
                self.unconstrained_cost_heap.peek(min_minimized_hero.hero.rarity)
            if min_unconstrained_hero_of_same_rarity and \
                    min_minimized_hero.level.level_count < min_unconstrained_hero_of_same_rarity.level.level_count - 1:
                return self.__level_up(self.minimized_cost_heap.pop(), remaining_gold)

        return self.__level_up(self.unconstrained_cost_heap.pop(), remaining_gold)

    @staticmethod
    def extract_rarity(oh: OwnedHero) -> Rarity:
        return oh.hero.rarity

    @staticmethod
    def rank_by_level(oh: OwnedHero) -> int:  # or just use level?
        return oh.level.level_count

    @staticmethod
    def rank_by_cost(oh: OwnedHero) -> int:
        # p1: Prioritize leveling up heroes which cost the least amount of gold
        level_up_cost = oh.cost_to_next_level().gold

        # p2: Then consider leveling up heroes closest to reborn milestone (smallest distance to reborn milestone)
        distance_to_reborn_milestone = oh.reborn_milestone() - oh.level.level_count

        # TODO: There becomes a point where it becomes more optimal to eat an expensive reborn cost to unlock the cheap
        #  level-ups after the fact, i.e. the expensive step is amortized within the average cost per level up
        return (level_up_cost * 100) + distance_to_reborn_milestone
