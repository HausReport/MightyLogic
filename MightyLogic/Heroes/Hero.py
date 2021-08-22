from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, InitVar
from enum import Enum, auto, unique
from typing import Any, Dict, List, Set, Tuple, Optional


@dataclass(order=True, frozen=True)
class LevelingCost:
    souls: int
    gold: int
    discount: Optional[int] = field(default=None, compare=False)
    allow_zero: InitVar[bool] = False

    def __post_init__(self, allow_zero: bool = False):
        min_cost = 0 if allow_zero else 1
        if self.souls < min_cost:
            raise RuntimeError(f"Souls must be greater than or equal to {min_cost} (was: {self.souls})")
        if self.gold < min_cost:
            raise RuntimeError(f"Gold must be greater than or equal to {min_cost} (was: {self.gold})")

    def __str__(self):
        return f"{self.souls:,} souls + {self.gold:,} gold"

    def with_discount(self, gold_discount: Optional[int] = None) -> LevelingCost:
        if gold_discount is None:
            gold_after_discount = self.gold
            combined_discount = self.discount
        else:
            gold_after_discount = round(float(self.gold) * ((100 - gold_discount) / 100))
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

    # TODO: Increase max level - 21 isn't the cap, just where I'd stopped pulling data
    MIN_LEVEL_COUNT = 1
    MAX_LEVEL_COUNT = 21

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


@dataclass
class LevelingSteps:
    steps: List[Tuple[Level, LevelingCost]]

    def __add__(self, other: LevelingSteps) -> LevelingSteps:
        return LevelingSteps(self.steps + other.steps)

    def aggregate_cost(self, gold_discount: Optional[int] = None) -> LevelingCost:
        souls = sum(cost.souls for __, cost in self.steps)
        gold = sum(cost.gold for __, cost in self.steps)
        return LevelingCost(souls, gold, allow_zero=True).with_discount(gold_discount)

    def final_level(self) -> Level:
        level, __ = self.steps[-1]
        return level

    def level_up_count(self) -> int:
        return len(list(level for level, __ in self.steps if level.level_count > 1))

    def with_discount(self, gold_discount: Optional[int] = None) -> LevelingSteps:
        return LevelingSteps([
            (level, cost.with_discount(gold_discount))
            for level, cost
            in self.steps
        ])


@unique
class Rarity(Enum):
    leveling_costs: Tuple
    reborn_milestones: Tuple
    soulbind_reqs: Tuple

    COMMON = ((
                  LevelingCost(25, 50),  # L2
                  LevelingCost(50, 80),  # L3
                  LevelingCost(75, 120),  # L4
                  LevelingCost(100, 200),  # L5
                  LevelingCost(150, 300),  # L6
                  LevelingCost(200, 500),  # L7
                  LevelingCost(250, 1000),  # L8
                  LevelingCost(300, 1500),  # L9
                  LevelingCost(350, 2000),  # L10
                  LevelingCost(450, 3000),  # L11
                  LevelingCost(600, 4000),  # L12
                  LevelingCost(750, 6000),  # L13
                  LevelingCost(900, 8000),  # L14
                  LevelingCost(1100, 10000),  # L15
                  LevelingCost(1400, 13000),  # L16
                  LevelingCost(2000, 16000),  # L17
                  LevelingCost(2700, 19000),  # L18
                  LevelingCost(3500, 22000),  # L19
                  LevelingCost(4500, 25000),  # L20
                  LevelingCost(6000, 28000)  # L21
              ), (11, 16, 21, 26), (
                  ("COMMON", 6, 1),
                  ("COMMON", 11, 2),
                  ("COMMON", 16, 2),
                  ("RARE", 11, 3)
              ))
    RARE = ((
                LevelingCost(25, 100),  # L2
                LevelingCost(50, 300),  # L3
                LevelingCost(75, 600),  # L4
                LevelingCost(100, 900),  # L5
                LevelingCost(130, 1400),  # L6
                LevelingCost(160, 2000),  # L7
                LevelingCost(190, 3500),  # L8
                LevelingCost(200, 4000),  # L9
                LevelingCost(250, 5000),  # L10
                LevelingCost(330, 6000),  # L11
                LevelingCost(420, 8000),  # L12
                LevelingCost(500, 10000),  # L13
                LevelingCost(600, 12000),  # L14
                LevelingCost(750, 14000),  # L15
                LevelingCost(950, 16000),  # L16
                LevelingCost(1400, 19000),  # L17
                LevelingCost(1900, 22000),  # L18
                LevelingCost(2400, 25000),  # L19
                LevelingCost(3000, 28000),  # L20
                LevelingCost(3700, 32000)  # L21
            ), (11, 16, 21, 26), (
                ("RARE", 5, 1),
                ("RARE", 9, 2),
                ("RARE", 13, 2),
                ("EPIC", 7, 3)
            ))
    EPIC = ((
                LevelingCost(15, 300),  # L2
                LevelingCost(30, 600),  # L3
                LevelingCost(45, 900),  # L4
                LevelingCost(60, 1400),  # L5
                LevelingCost(80, 1900),  # L6
                LevelingCost(100, 2500),  # L7
                LevelingCost(120, 4000),  # L8
                LevelingCost(140, 5000),  # L9
                LevelingCost(160, 6000),  # L10
                LevelingCost(200, 7000),  # L11
                LevelingCost(250, 9000),  # L12
                LevelingCost(320, 11000),  # L13
                LevelingCost(400, 13000),  # L14
                LevelingCost(500, 16000),  # L15
                LevelingCost(650, 19000),  # L16
                LevelingCost(900, 22000),  # L17
                LevelingCost(1100, 26000),  # L18
                LevelingCost(1350, 30000),  # L19
                LevelingCost(1800, 34000),  # L20
                LevelingCost(2300, 38000)  # L21
            ), (6, 11, 16, 21, 26), (
                ("EPIC", 3, 1),
                ("EPIC", 6, 2),
                ("EPIC", 8, 2),
                ("LEGENDARY", 5, 3)
            ))
    LEGENDARY = ((
                     LevelingCost(5, 600),  # L2
                     LevelingCost(10, 900),  # L3
                     LevelingCost(15, 1400),  # L4
                     LevelingCost(20, 1900),  # L5
                     LevelingCost(40, 2500),  # L6
                     LevelingCost(60, 3500),  # L7
                     LevelingCost(80, 5500),  # L8
                     LevelingCost(100, 7000),  # L9
                     LevelingCost(120, 9000),  # L10
                     LevelingCost(150, 11000),  # L11
                     LevelingCost(200, 14000),  # L12
                     LevelingCost(250, 17000),  # L13
                     LevelingCost(320, 20000),  # L14
                     LevelingCost(400, 24000),  # L15
                     LevelingCost(500, 28000),  # L16
                     LevelingCost(700, 32000),  # L17
                     LevelingCost(850, 36000),  # L18
                     LevelingCost(1000, 40000),  # L19
                     LevelingCost(1300, 44000),  # L20
                     LevelingCost(1700, 48000)  # L21
                 ), (6, 11, 16, 21, 26), (
                     ("LEGENDARY", 2, 1),
                     ("LEGENDARY", 3, 2),
                     ("LEGENDARY", 4, 2),
                     ("LEGENDARY", 6, 3)
                 ))

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, leveling_costs: Tuple, reborn_milestones: Tuple, soulbind_reqs: Tuple):
        self.leveling_costs = leveling_costs
        self.reborn_milestones = reborn_milestones
        self.soulbind_reqs = soulbind_reqs

    def __str__(self):
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
            needed_level
            for rarity in Rarity
            for needed_rarity_name, needed_level, __ in rarity.soulbind_reqs
            if needed_rarity_name == for_rarity.name
        )


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


@dataclass(frozen=True)
class Soulbind:
    for_hero: Hero
    target_heroes: List[Hero]
    requirements: SoulbindRequirements

    def __post_init__(self):
        self.requirements.validate(self.for_hero, self.target_heroes)


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

    def __eq__(self, other):
        return self.num == other.num

    def __hash__(self):
        return self.num

    def __repr__(self):
        return self.__str__()

    def __str__(self):
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
        return LevelingCost.free() if to_level.level_count == 1 else self.rarity.leveling_costs[to_level.level_count-2]

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
        return self.rarity.reborn_milestones[for_level.reborn_count]

    def to_csv(self) -> Dict[str, Any]:
        return self.to_rec()

    def to_dict(self) -> Dict[str, Any]:
        return deepcopy(self.__dict__)

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
