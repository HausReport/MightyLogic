from __future__ import annotations

import dataclasses
import json
import re
from copy import deepcopy
from dataclasses import field
from typing import Dict, Any
from typing import Tuple, Optional

from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.Heroes.Leveling.Level import Level
from MightyLogic.Heroes.Leveling.LevelingCost import LevelingCost
from MightyLogic.Heroes.Leveling.LevelingSteps import LevelingSteps


@dataclasses.dataclass
class OwnedHero:
    hero: Hero
    level: Level
    souls: int
    soulbinds_mask: Tuple[bool, bool, bool, bool] = field(default=(False, False, False, False))
    might: int = field(init=False)
    troops: int = field(init=False)

    __next_level: Level = field(init=False, repr=False)
    __steps_to_next_level: LevelingSteps = field(init=False, repr=False)

    def __post_init__(self):
        assert self.souls >= 0, f"Cannot have fewer than 0 souls (was: {self})"

        self.__precompute_leveling_info()

    def __eq__(self, other):
        return self.hero == other.hero\
               and self.level == other.soulbind_level\
               and self.souls == other.souls\
               and self.soulbinds_mask == other.soulbinds_mask

    def __deepcopy__(self, memodict={}):
        dc = OwnedHero(
            hero=self.hero,  # immutable
            level=deepcopy(self.level, memodict),
            souls=deepcopy(self.souls, memodict),
            soulbinds_mask=deepcopy(self.soulbinds_mask, memodict))  # immutable (but shouldn't be)
        memodict[id(self)] = dc
        return dc

    def __hash__(self):
        return self.hero.num

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.hero} - {self.level} - {self.souls:,} available souls"

    def __precompute_leveling_info(self):
        self.might = self.hero.might_at(self.level, self.soulbinds_mask)
        self.troops = self.hero.troops_at(self.level, self.soulbinds_mask)

        self.__next_level = self.level.level_up()
        self.__steps_to_next_level = self.leveling_steps_to(self.__next_level)

    def __souls_returned_on_reborn(self) -> int:
        reborn_milestone = self.reborn_milestone()

        # If we're at or under the milestone, we get nothing back
        if self.level.level_count <= reborn_milestone:
            return 0

        # Otherwise, we get all the souls used to get from the milestone to our current level
        steps_from_milestone: LevelingSteps = self.hero.leveling_steps(
            from_level=Level(level_count=reborn_milestone, reborn_count=self.level.reborn_count),
            to_level=self.level
        )
        return steps_from_milestone.aggregate_cost().souls

    def can_level_up(self, with_gold: Optional[int] = None, gold_discount: Optional[float] = None,
                     require: bool = False) -> bool:
        aggregate_cost = self.__steps_to_next_level.aggregate_cost(gold_discount)
        can_level_up = self.souls >= aggregate_cost.souls and (with_gold is None or with_gold >= aggregate_cost.gold)
        if require and not can_level_up:
            raise RuntimeError(f"Cannot level up from {self.level} to {self.__next_level}; available:"
                               f" <souls={self.souls}, gold={'infinite' if with_gold is None else with_gold}>,"
                               f" required: {aggregate_cost}")
        return can_level_up

    def can_level_up_after_reborn(self, with_gold: Optional[int] = None, gold_discount: Optional[float] = None) -> bool:
        if self.can_reborn():
            return OwnedHero(self.hero, self.level.reborn(), self.souls).can_level_up(with_gold, gold_discount)
        else:
            return False

    def can_reborn(self, require: bool = False) -> bool:
        reborn_milestone = self.reborn_milestone()
        current_level = self.level.level_count
        can_reborn = current_level >= reborn_milestone
        if require and not can_reborn:
            raise RuntimeError(f"Not at a reborn milestone; current: {current_level}, required: {reborn_milestone}")
        return can_reborn

    def completed_soulbinds(self):
        return None  # FIXME

    def cost_to_next_level(self, gold_discount: Optional[float] = None) -> LevelingCost:
        return self.__steps_to_next_level.aggregate_cost(gold_discount)

    def leveling_steps_to(self, target_level: Level) -> LevelingSteps:
        return self.hero.leveling_steps(self.level, target_level)

    def level_up(self, with_gold: Optional[int] = None, gold_discount: Optional[float] = None) -> LevelingSteps:
        self.can_level_up(with_gold=with_gold, gold_discount=gold_discount, require=True)

        new_level = self.__next_level
        steps = self.__steps_to_next_level

        self.level = new_level
        self.souls -= steps.aggregate_cost().souls
        self.__precompute_leveling_info()

        return steps.with_discount(gold_discount)

    def reborn(self):
        self.can_reborn(require=True)

        # If we reborn past the milestone, we get those souls back
        self.souls += self.__souls_returned_on_reborn()
        self.level = self.level.reborn()
        self.__precompute_leveling_info()

    def reborn_milestone(self) -> int:
        return self.hero.reborn_milestone(self.level)

    def to_data_frame_rec(self) -> Dict[str, Any]:
        d = self.hero.to_data_frame_rec()
        d.update({
            "level": self.level,
            "souls": self.souls,
        })
        return d

    def to_dict(self) -> Dict[str, Any]:
        d = self.hero.to_dict()
        d.update(self.level.to_dict())
        d.update({
            "souls": self.souls,
        })
        return d

    # TODO: Move into Codec.Rec
    def to_rec(self) -> str:
        return json.dumps({
            "id": self.hero.id,
            "level": self.level.level_count,
            "reborn": self.level.reborn_count,
            "available_souls": self.souls
        })

    # TODO: Move into Codec.Rec
    @staticmethod
    def from_rec(rec: Dict[str, Any], hero_dir: HeroDirectory) -> OwnedHero:
        return OwnedHero(
            hero=hero_dir.find_by_num(int(rec["id"])),
            level=Level(level_count=int(rec["level"]), reborn_count=int(rec["reborn"])),
            souls=int(rec["available_souls"])
        )

    # TODO: Move into Codec.Bot
    @staticmethod
    def from_squad_export(line: str, hero_dir: HeroDirectory) -> OwnedHero:
        colon_index = line.index(":")
        num = int(line[0:colon_index].strip())

        match = re.search("Level (\\d+)\\s+Reborn (\\d+)\\s+Unused Souls (\\d+)$", line)

        level_count = int(match.group(1))
        reborn_count = int(match.group(2))
        souls = int(match.group(3))

        return OwnedHero(
            hero=hero_dir.find_by_num(num),
            level=Level(level_count=level_count, reborn_count=reborn_count),
            souls=souls
        )
