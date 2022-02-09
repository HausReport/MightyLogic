from __future__ import annotations

from copy import deepcopy, copy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple

import hashlib

from MightyLogic.Heroes.Attributes.Alignment import Alignment
from MightyLogic.Heroes.Attributes.Gender import Gender
from MightyLogic.Heroes.Leveling.Level import Level
from MightyLogic.Heroes.Leveling.LevelingCost import LevelingCost
from MightyLogic.Heroes.Leveling.LevelingSteps import LevelingSteps
from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Attributes.Shape import Shape


@dataclass
class Hero:
    num: int
    name: str
    rarity: Rarity
    shape: Shape
    alignment: Alignment
    gender: Gender
    evolves_from: Set[Hero] = field(default=None)
    evolves_to: Set[Hero] = field(default=None)
    # TODO soulbinds: List[Soulbind] = field(default=None)

    def __post_init__(self):
        is_building = self.shape is Shape.BUILDING
        is_sexless = self.gender is Gender.SEXLESS
        assert is_building == is_sexless, f"Buildings must be sexless (was: {self})"

    def __eq__(self, other: Hero) -> bool:
        return self.num == other.num

    def __hash__(self) -> int:
        return self.num

    def __lt__(self, other: Hero) -> bool:
        return self.num < other.num

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.num}: {self.name} ({self.rarity} / {self.shape} / {self.alignment} / {self.gender})"

    def all_evolutions_to(self, include_self: bool = False) -> Set[Hero]:
        evolutions_to: Set[Hero] = set()
        q: List[Hero] = [self]
        while q:
            hero = q.pop(0)
            if include_self or hero != self:
                evolutions_to.add(hero)
            q.extend(hero.evolves_from)
        return evolutions_to

    def might_at(self, level: Level, soulbinds_mask: Tuple[bool, bool, bool, bool] = (False, False, False, False)) \
            -> int:
        # TODO: soulbinds
        return level.might_for(self.rarity)

    def leveling_cost(self, to_level: Level) -> LevelingCost:
        return LevelingCost.to(to_level.level_count, self.rarity)

    def leveling_steps(self, from_level: Level, to_level: Level) -> LevelingSteps:
        assert to_level > from_level, f"From must be lower than the to (was from: {from_level}, to: {to_level})"

        # This originally supported various reborn strategies, but it made things complicated
        assert from_level.reborn_count == to_level.reborn_count, \
            f"Levels must be at the same reborn count (was from: {from_level}, to: {to_level}"

        current_level = from_level
        steps = []
        while current_level < to_level:
            next_level = current_level.level_up()
            steps.append((next_level, self.leveling_cost(next_level)))
            current_level = next_level
        return LevelingSteps(steps)

    def reborn_milestone(self, for_level: Level) -> int:
        return for_level.next_reborn_milestone_for(self.rarity)

    def to_csv(self) -> Dict[str, Any]:
        return self.to_rec()

    def to_data_frame_rec(self) -> Dict[str, Any]:
        d = self.to_dict()
        for k in ["evolves_from", "evolves_to", "soulbinds"]:
            if k in d.keys():
                del d[k]
        return d

    def to_dict(self) -> Dict[str, Any]:
        return copy(self.__dict__)

    # TODO: Move into Codec.Rec
    def to_rec(self) -> Dict[str, Any]:
        d = self.to_dict()

        # Expose num as id
        d["id"] = d["num"]
        del d["num"]

        # Serialize evolves_to as hero id's
        d["evolves_to"] = list(hero.num for hero in d["evolves_to"])

        # Removes evolves_from
        del d["evolves_from"]

        # FIXME: soulbinds
        del d["soulbinds"]

        return d

    def troops_at(self, level: Level, soulbinds_mask: Tuple[bool, bool, bool, bool] = (False, False, False, False))\
            -> int:
        # TODO: soulbinds
        return level.troops_for(self.rarity)

    def icon_url(self, width=100, local=True) -> str:
        if local:
            return Hero._local_icon_url(self.name)
        else:
            return Hero._icon_url(self.name)

    @staticmethod
    def _local_icon_url(bName: str) -> str:
        aName = bName.replace(' ', '_')  # need to replace spaces with underline
        aName += '.png'
        return aName

    @staticmethod
    def _icon_url(bName: str) -> str:
        aName = bName.replace(' ', '_')  # need to replace spaces with underline
        aName += '.png'
        # print(aName)
        m = hashlib.md5()
        m.update(aName.encode('utf-8'))
        d = m.hexdigest()
        # print(d)
        ret = "https://static.wikia.nocookie.net/mightyparty/images/"
        ret += d[0] + '/' + d[ 0:2] + '/' + aName #+ '/revision/latest/scale-to-width-down/' + str(width)
        # print(ret)
        return ret

    @staticmethod
    def from_csv(row: Dict[str, Any]) -> Hero:
        return Hero.from_rec(row)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Hero:
        updated_d = deepcopy(d)
        updated_d["num"] = d["id"]
        del updated_d["id"]
        return Hero(updated_d)

    @staticmethod
    def from_rec(rec: Dict[str, Any]) -> Hero:
        return Hero(
            num=int(rec["id"]),
            name=rec["name"],
            rarity=Rarity.from_s(rec["rarity"]),
            shape=Shape.from_s(rec["shape"]),
            alignment=Alignment.from_s(rec["alignment"]),
            gender=Gender.from_s(rec["gender"])
        )
