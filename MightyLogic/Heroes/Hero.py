from __future__ import annotations

from copy import deepcopy, copy
from dataclasses import dataclass, field, InitVar
from enum import Enum, auto, unique
from functools import total_ordering
from typing import Any, Dict, List, Set, Tuple, Optional

import hashlib


@dataclass(order=True, frozen=True)
class LevelingCost:
    souls: int
    gold: int
    discount: Optional[float] = field(default=None, compare=False)
    allow_zero: InitVar[bool] = False

    def __post_init__(self, allow_zero: bool = False):
        min_cost = 0 if allow_zero else 1
        if self.souls < min_cost:
            raise RuntimeError(f"Souls must be greater than or equal to {min_cost} (was: {self.souls})")
        if self.gold < min_cost:
            raise RuntimeError(f"Gold must be greater than or equal to {min_cost} (was: {self.gold})")

    def __str__(self):
        return f"{self.souls:,} souls + {self.gold:,} gold"

    def with_discount(self, gold_discount: Optional[float] = None) -> LevelingCost:
        if gold_discount is None:
            gold_after_discount = self.gold
            combined_discount = self.discount
        else:
            gold_after_discount = round(float(self.gold) * (1.0 - gold_discount))
            combined_discount = gold_discount + (0 if self.discount is None else self.discount)
        return LevelingCost(souls=self.souls, gold=gold_after_discount, discount=combined_discount, allow_zero=True)

    @staticmethod
    def free() -> LevelingCost:
        return LevelingCost(0, 0, allow_zero=True)


@dataclass(frozen=True)
class Level:
    level_count: int
    reborn_count: int

    MIN_REBORN_COUNT = 0
    MAX_REBORN_COUNT = 4

    MIN_LEVEL_COUNT = 1
    MAX_LEVEL_COUNT = 31

    def __post_init__(self):
        if self.level_count < Level.MIN_LEVEL_COUNT or self.level_count > Level.MAX_LEVEL_COUNT:
            raise RuntimeError(f"Level count must be between {Level.MIN_LEVEL_COUNT} and {Level.MAX_LEVEL_COUNT},"
                               f" inclusive (was: {self.level_count})")
        if self.reborn_count < Level.MIN_REBORN_COUNT or self.reborn_count > Level.MAX_REBORN_COUNT:
            raise RuntimeError(f"Reborn count must be between {Level.MIN_REBORN_COUNT} and {Level.MAX_REBORN_COUNT}"
                               f", inclusive (was: {self.reborn_count})")

    def __abs__(self):
        # 100 is an arbitrary number that gives us a nice numerical representation (as long as max level < 100)
        return (self.reborn_count * 100) + self.level_count

    def __eq__(self, other):
        return abs(self) == abs(other)

    def __le__(self, other):
        return abs(self) <= abs(other)

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __ge__(self, other):
        return abs(self) >= abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __str__(self):
        return f"level {self.level_count} @ reborn {self.reborn_count}"

    def level_up(self) -> Level:
        return Level(self.level_count + 1, self.reborn_count)

    def reborn(self) -> Level:
        return Level(1, self.reborn_count + 1)

    def to_dict(self) -> Dict[str, Any]:
        return copy(self.__dict__)


@dataclass
class LevelingSteps:
    steps: List[Tuple[Level, LevelingCost]]

    def __add__(self, other: LevelingSteps) -> LevelingSteps:
        return LevelingSteps(self.steps + other.steps)

    def aggregate_cost(self, gold_discount: Optional[float] = None) -> LevelingCost:
        souls = sum(cost.souls for __, cost in self.steps)
        gold = sum(cost.gold for __, cost in self.steps)
        return LevelingCost(souls, gold, allow_zero=True).with_discount(gold_discount)

    def final_level(self) -> Level:
        level, __ = self.steps[-1]
        return level

    def level_up_count(self) -> int:
        return len(list(level for level, __ in self.steps if level.level_count > 1))

    def with_discount(self, gold_discount: Optional[float] = None) -> LevelingSteps:
        return LevelingSteps([
            (level, cost.with_discount(gold_discount))
            for level, cost
            in self.steps
        ])


@unique
@total_ordering
class Rarity(Enum):
    leveling_costs: Tuple
    reborn_milestones: Tuple

    COMMON = (
        (
            LevelingCost(25, 50),  # L2
            LevelingCost(50, 80),  # L3
            LevelingCost(75, 120),  # L4
            LevelingCost(100, 200),  # L5
            LevelingCost(150, 300),  # L6
            LevelingCost(200, 500),  # L7
            LevelingCost(250, 1_000),  # L8
            LevelingCost(300, 1_500),  # L9
            LevelingCost(350, 2_000),  # L10
            LevelingCost(450, 3_000),  # L11
            LevelingCost(600, 4_000),  # L12
            LevelingCost(750, 6_000),  # L13
            LevelingCost(900, 8_000),  # L14
            LevelingCost(1_100, 10_000),  # L15
            LevelingCost(1_400, 13_000),  # L16
            LevelingCost(2_000, 16_000),  # L17
            LevelingCost(2_700, 19_000),  # L18
            LevelingCost(3_500, 22_000),  # L19
            LevelingCost(4_500, 25_000),  # L20
            LevelingCost(6_000, 28_000),  # L21
            LevelingCost(7_500, 32_000),  # L22
            LevelingCost(9_500, 36_000),  # L23
            LevelingCost(12_000, 40_000),  # L24
            LevelingCost(15_000, 45_000),  # L25
            LevelingCost(18_000, 50_000)  # L26
        ),
        (11, 16, 21, 26, 32, 32)
    )
    RARE = (
        (
            LevelingCost(25, 100),  # L2
            LevelingCost(50, 300),  # L3
            LevelingCost(75, 600),  # L4
            LevelingCost(100, 900),  # L5
            LevelingCost(130, 1_400),  # L6
            LevelingCost(160, 2_000),  # L7
            LevelingCost(190, 3_500),  # L8
            LevelingCost(200, 4_000),  # L9
            LevelingCost(250, 5_000),  # L10
            LevelingCost(330, 6_000),  # L11
            LevelingCost(420, 8_000),  # L12
            LevelingCost(500, 10_000),  # L13
            LevelingCost(600, 12_000),  # L14
            LevelingCost(750, 14_000),  # L15
            LevelingCost(950, 16_000),  # L16
            LevelingCost(1_400, 19_000),  # L17
            LevelingCost(1_900, 22_000),  # L18
            LevelingCost(2_400, 25_000),  # L19
            LevelingCost(3_000, 28_000),  # L20
            LevelingCost(3_700, 32_000),  # L21
            LevelingCost(4_500, 36_000),  # L22
            LevelingCost(5_500, 40_000),  # L23
            LevelingCost(7_000, 45_000),  # L24
            LevelingCost(9_000, 50_000),  # L25
            LevelingCost(12_000, 55_000),  # L26
            LevelingCost(12_150, 57_000),  # L27
            LevelingCost(12_350, 60_000),  # L28
            LevelingCost(12_550, 92_180),  # L29
            LevelingCost(12_800, 66_000),  # L30
            LevelingCost(13_100, 70_000)  # L31
        ),
        (11, 16, 21, 26, 32, 32)
    )
    EPIC = (
        (
            LevelingCost(15, 300),  # L2
            LevelingCost(30, 600),  # L3
            LevelingCost(45, 900),  # L4
            LevelingCost(60, 1_400),  # L5
            LevelingCost(80, 1_900),  # L6
            LevelingCost(100, 2_500),  # L7
            LevelingCost(120, 4_000),  # L8
            LevelingCost(140, 5_000),  # L9
            LevelingCost(160, 6_000),  # L10
            LevelingCost(200, 7_000),  # L11
            LevelingCost(250, 9_000),  # L12
            LevelingCost(320, 11_000),  # L13
            LevelingCost(400, 13_000),  # L14
            LevelingCost(500, 16_000),  # L15
            LevelingCost(650, 19_000),  # L16
            LevelingCost(900, 22_000),  # L17
            LevelingCost(1_100, 26_000),  # L18
            LevelingCost(1_350, 30_000),  # L19
            LevelingCost(1_800, 34_000),  # L20
            LevelingCost(2_300, 38_000),  # L21
            LevelingCost(3_000, 42_000),  # L22
            LevelingCost(4_000, 47_000),  # L23
            LevelingCost(5_000, 52_000),  # L24
            LevelingCost(6_300, 58_000),  # L25
            LevelingCost(8_000, 65_000),  # L26
            LevelingCost(8_200, 67_000),  # L27
            LevelingCost(8_400, 70_000),  # L28
            LevelingCost(8_650, 73_000),  # L29
            LevelingCost(8_950, 77_000),  # L30
            LevelingCost(9_300, 82_000)  # L31
        ),
        (6, 11, 16, 21, 26, 32)
    )
    LEGENDARY = (
        (
            LevelingCost(5, 600),  # L2
            LevelingCost(10, 900),  # L3
            LevelingCost(15, 1_400),  # L4
            LevelingCost(20, 1_900),  # L5
            LevelingCost(40, 2_500),  # L6
            LevelingCost(60, 3_500),  # L7
            LevelingCost(80, 5_500),  # L8
            LevelingCost(100, 7_000),  # L9
            LevelingCost(120, 9_000),  # L10
            LevelingCost(150, 11_000),  # L11
            LevelingCost(200, 14_000),  # L12
            LevelingCost(250, 17_000),  # L13
            LevelingCost(320, 20_000),  # L14
            LevelingCost(400, 24_000),  # L15
            LevelingCost(500, 28_000),  # L16
            LevelingCost(700, 32_000),  # L17
            LevelingCost(850, 36_000),  # L18
            LevelingCost(1_000, 40_000),  # L19
            LevelingCost(1_300, 44_000),  # L20
            LevelingCost(1_700, 48_000),  # L21
            LevelingCost(2_200, 52_000),  # L22
            LevelingCost(2_900, 57_000),  # L23
            LevelingCost(3_700, 62_000),  # L24
            LevelingCost(4_800, 68_000),  # L25
            LevelingCost(6_000, 75_000),  # L26
            LevelingCost(6_150, 80_000),  # L27
            LevelingCost(6_300, 86_000),  # L28
            LevelingCost(6_450, 93_000),  # L29
            LevelingCost(6_650, 101_000),  # L30
            LevelingCost(6_900, 110_000)  # L31
        ),
        (6, 11, 16, 21, 26, 32)
    )

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, leveling_costs: Tuple, reborn_milestones: Tuple):
        self.leveling_costs = leveling_costs
        self.reborn_milestones = reborn_milestones

    def __eq__(self, other: Rarity) -> bool:
        return other and self.name == other.name

    def __hash__(self) -> int:
        return self.leveling_costs[0].gold

    def __lt__(self, other: Rarity) -> bool:
        return self.leveling_costs[0].gold < other.leveling_costs[0].gold

    def __str__(self) -> str:
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Rarity]:
        try:
            return Rarity[s.upper()]
        except KeyError:
            return None

    @staticmethod
    def optimal_soulbind_level(for_rarity: Rarity) -> int:
        return max(
            req.target_level_count
            for rarity in Rarity
            for req in Rarity.soulbind_requirements(rarity)
            if req.target_rarity == for_rarity
        )

    @staticmethod
    def soulbind_requirements(for_rarity: Rarity) -> List[SoulbindRequirements]:
        return SOULBIND_REQUIREMENTS_BY_RARITY[for_rarity]


@unique
class Shape(Enum):
    BUILDING = auto()
    MELEE = auto()
    RANGED = auto()

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Shape]:
        try:
            return Shape[s.upper()]
        except KeyError:
            return None


@unique
class Alignment(Enum):
    CHAOS = auto()
    NATURE = auto()
    ORDER = auto()

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Alignment]:
        try:
            return Alignment[s.upper()]
        except KeyError:
            return None


@unique
class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    SEXLESS = auto()

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Gender]:
        try:
            return Gender[s.upper()]
        except KeyError:
            return None


@dataclass(frozen=True)
class SoulbindRequirements:
    for_rarity: Rarity
    soulbind_level: int
    target_rarity: Rarity
    target_hero_count: int
    target_level_count: int

    def validate(self, for_hero: Hero, target_heroes: List[Hero]):
        assert for_hero.rarity == self.for_rarity
        for target_hero in target_heroes:
            assert target_hero.rarity == self.target_rarity
        assert len(target_heroes) == self.target_hero_count

    @staticmethod
    def from_tuple(for_rarity, tuples):
        hero_counts = [1, 2, 2, 3]
        return [
            SoulbindRequirements(
                for_rarity=for_rarity,
                soulbind_level=i + 1,
                target_rarity=target_rarity,
                target_hero_count=hero_counts[i],
                target_level_count=target_hero_level
            )
            for i, (target_rarity, target_hero_level) in enumerate(tuples)
        ]


@dataclass(frozen=True)
class Soulbind:
    for_hero: Hero
    target_heroes: List[Hero]
    requirements: SoulbindRequirements

    def __post_init__(self):
        self.requirements.validate(self.for_hero, self.target_heroes)


SOULBIND_REQUIREMENTS_BY_RARITY = {
    Rarity.COMMON   : SoulbindRequirements.from_tuple(Rarity.COMMON, [
        (Rarity.COMMON, 6),
        (Rarity.COMMON, 11),
        (Rarity.COMMON, 16),
        (Rarity.RARE, 11)
    ]),
    Rarity.RARE     : SoulbindRequirements.from_tuple(Rarity.RARE, [
        (Rarity.RARE, 5),
        (Rarity.RARE, 9),
        (Rarity.RARE, 13),
        (Rarity.EPIC, 7)
    ]),
    Rarity.EPIC     : SoulbindRequirements.from_tuple(Rarity.EPIC, [
        (Rarity.EPIC, 3),
        (Rarity.EPIC, 6),
        (Rarity.EPIC, 8),
        (Rarity.LEGENDARY, 5)
    ]),
    Rarity.LEGENDARY: SoulbindRequirements.from_tuple(Rarity.LEGENDARY, [
        (Rarity.LEGENDARY, 2),
        (Rarity.LEGENDARY, 3),
        (Rarity.LEGENDARY, 4),
        (Rarity.LEGENDARY, 6)
    ])
}


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
    soulbinds: List[Soulbind] = field(default=None)

    def __post_init__(self):
        if self.shape is Shape.BUILDING and self.gender is not Gender.SEXLESS:
            raise RuntimeError(f"Buildings must be sexless (was: {self})")

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

    def leveling_cost(self, to_level: Level) -> LevelingCost:
        return LevelingCost.free() if to_level.level_count == 1 else self.rarity.leveling_costs[
            to_level.level_count - 2]

    def leveling_steps(self, from_level: Level, to_level: Level) -> LevelingSteps:
        if from_level >= to_level:
            raise RuntimeError(f"From must be lower than the to (was from: {from_level}, to: {to_level})")

        # This originally supported various reborn strategies, but it made things complicated
        if from_level.reborn_count != to_level.reborn_count:
            raise RuntimeError(f"Levels must be at the same reborn count (was from: {from_level}, to: {to_level}")

        current_level = from_level
        steps = []
        while current_level < to_level:
            next_level = current_level.level_up()
            steps.append((next_level, self.leveling_cost(next_level)))
            current_level = next_level
        return LevelingSteps(steps)

    def reborn_milestone(self, for_level: Level) -> int:
        # TODO: Support the upper bound
        return self.rarity.reborn_milestones[for_level.reborn_count]

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
