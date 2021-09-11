from heapq import heapify, heappush, heappop
from typing import List, Tuple, Optional

from Heroes.Collection import Collection, HeroSelector
from Heroes.Hero import LevelingSteps
from Heroes.OwnedHero import OwnedHero
from HighGrowth.Strategies import HighGrowthStrategy, PrioritizedItem


class MinimizeGold(HighGrowthStrategy):
    """
    Always level up the cheapest hero, and reborn everything as soon as possible. At some point this should normalize to
    getting everything to a consistent level, i.e. the point at which the gold cost for level-ups converge: L6 for
    legendary ~= L7/8 for epic/rare ~= L11 for common.
    """
    never_reborn: HeroSelector
    cost_heap: List[PrioritizedItem]  # actually a min-heap - Python is weird

    def __init__(self, collection: Collection, excluding: HeroSelector, never_reborn: HeroSelector,
                 gold_discount: Optional[int]):
        super(MinimizeGold, self).__init__(collection, excluding, gold_discount)

        self.never_reborn = never_reborn
        self.cost_heap = []
        heapify(self.cost_heap)
        for oh in collection.all_owned_heroes():
            self.__offer(oh)

    def __str__(self):
        return "minimize gold, i.e. always level up the cheapest hero, and reborn everything as soon as possible\n" \
               f" - exclusions: {self.excluding.describe(self.collection)}\n" \
               f" - never reborn: {self.never_reborn.describe(self.collection)}"

    def __offer(self, oh: OwnedHero):
        if oh.hero in self.excluding.select(self.collection):
            return

        # Reborn all heroes if we can level up them up afterwards (cost is lowest after a reborn)
        # FIXME: Need to factor in available gold otherwise we'll reborn for no reason
        if oh.can_level_up_after_reborn() and oh.hero not in self.never_reborn.select(self.collection):
            oh.reborn()

        level_up_cost = oh.cost_to_next_level()
        # TODO: Consider tie breaks - do we want to factor in rarity or # of souls/potential level ups?
        # TODO: There becomes a point where it becomes more optimal to eat an expensive reborn cost to unlock the cheap
        #  level-ups after the fact, i.e. the expensive step is amortized within the average cost per level up
        rank = level_up_cost.gold

        # Push the hero onto the heap but ensure only the rank is considered when determining priority
        heappush(self.cost_heap, PrioritizedItem(rank, oh))

    def has_next(self, remaining_gold: Optional[int]) -> bool:
        # This check isn't 100% accurate (theoretically we should peek a the next value and ensure we have enough gold
        # to level it up), but it's still a valid terminal condition (we just end up exhausting the heap)
        return (remaining_gold is None or remaining_gold > 0) and self.cost_heap

    def process_next(self, remaining_gold: Optional[int]) -> Tuple[OwnedHero, LevelingSteps]:
        oh = heappop(self.cost_heap).item
        steps = None

        # If reborning means we can level up, do so - this will always be cheaper
        if oh.hero not in self.never_reborn.select(self.collection) \
                and oh.can_level_up_after_reborn(remaining_gold, self.gold_discount):
            oh.reborn()

        # If we an level up, do so
        if oh.can_level_up(remaining_gold, self.gold_discount):
            steps = oh.level_up(remaining_gold, self.gold_discount)
            self.__offer(oh)

        return oh, steps
