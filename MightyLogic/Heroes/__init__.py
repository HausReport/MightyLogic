from __future__ import annotations

import logging
from collections import defaultdict
from enum import Enum, auto, unique
from pathlib import Path
from typing import Iterable, Any, List, Callable, Dict, Set
from typing import Tuple, Optional

MIN_REBORN_COUNT = 0
MAX_REBORN_COUNT = 4

# TODO: Increase max level - 21 isn't the cap, just where I'd stopped pulling data
MIN_LEVEL_COUNT = 1
MAX_LEVEL_COUNT = 21

logger = logging.getLogger("MightyLogic.Heroes")


def create_secondary_indices(data: Iterable[Any], for_accessors: List[Callable[[Any], Any]]) -> List[Dict[Any, Any]]:
    secondary_indices = [dict() for _accessor in for_accessors]
    for datum in data:
        for i, accessor in enumerate(for_accessors):
            index = secondary_indices[i]
            key = accessor(datum)
            if key in index.keys():
                raise KeyError(f"Data for key \"{key}\" already exists in {index}")
            index[key] = datum
    return secondary_indices


def deserialize_lines(path_to_file: Path, deserializer: Callable[[str], Any]) -> List[Any]:
    _list = []
    with path_to_file.open() as file:
        for line in file:
            line = line.strip()
            try:
                deserialized = deserializer(line)
                logger.debug(f"Deserialized {deserialized} (created from \"{line}\")")
                _list.append(deserialized)
            except Exception as e:
                raise RuntimeError(f"Failed to deserialize: \"{line}\"") from e
    return _list


def group_by(values: Set[Any], grouper: Callable[[Any], Any], include_all: bool) -> Dict[Any, Set[Any]]:
    grouped = defaultdict(set)
    for value in values:
        if include_all:
            grouped["all"].add(value)
        grouped[grouper(value)].add(value)
    return grouped


def per_group(grouped: Dict[Any, Set[Any]], do: Callable[[Set[Any]], Any]) -> Dict[Any, Any]:
    return dict((name, do(group)) for name, group in grouped.items())


def stats_for(values: Iterable[Any]) -> Dict[str, float]:
    return {
        "min": min(values) if values else None,
        #"mean": mean(values) if values else None,
        #"median": median(values) if values else None,
        #"mode": mode(values) if values else None,
        "max": max(values) if values else None,
        #"variance": pvariance(values) if values else None,
        #"stdev": stdev(values) if values else None,
        # TODO: "quantiles": quantiles(values, n=4, method="inclusive")
    }


# TODO: Factor this all out into dedicated files

class Level:
    level_count: int
    reborn_count: int

    def __init__(self, level_count: int, reborn_count: int):
        if level_count < MIN_LEVEL_COUNT or level_count > MAX_LEVEL_COUNT:
            raise RuntimeError(f"Level count must be between {MIN_LEVEL_COUNT} and {MAX_LEVEL_COUNT}, inclusive"
                               f" (was: {level_count})")
        self.level_count = level_count

        if reborn_count < MIN_REBORN_COUNT or reborn_count > MAX_REBORN_COUNT:
            raise RuntimeError(f"Reborn count must be between {MIN_REBORN_COUNT} and {MAX_REBORN_COUNT}, inclusive"
                               f" (was: {reborn_count})")
        self.reborn_count = reborn_count

    def __abs__(self):
        # 100 is an arbitrary number that gives us a nice numerical representation (as long as max level < 100)
        return (self.reborn_count * 100) + self.level_count

    def __eq__(self, other):
        return self.level_count == other.level_count and self.reborn_count == other.reborn_count

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


class LevelingCost:
    souls: int
    gold: int
    discount: Optional[int]

    def __init__(self, souls: int, gold: int, discount: Optional[int] = None, allow_zero: bool = False):
        min_cost = 0 if allow_zero else 1

        if souls < min_cost:
            raise RuntimeError(f"Souls must be greater than or equal to {min_cost} (was: {souls})")
        self.souls = souls

        if gold < min_cost:
            raise RuntimeError(f"Gold must be greater than or equal to {min_cost} (was: {gold})")
        self.gold = gold

        self.discount = discount

    def __eq__(self, other):
        return self.souls == other.souls and self.gold == other.gold

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __lt__(self, other):
        return self.souls < other.souls or self.gold < other.gold

    def __ge__(self, other):
        return self.souls >= other.souls and self.gold >= other.gold

    def __gt__(self, other):
        return self.souls > other.souls and self.gold > other.gold

    def __str__(self):
        return f"{self.souls} souls + {self.gold} gold"

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


class LevelingSteps:
    steps: List[Tuple[Level, LevelingCost]]

    def __init__(self, steps: List[Tuple[Level, LevelingCost]]):
        self.steps = steps

    def __add__(self, other: LevelingSteps) -> LevelingSteps:
        return LevelingSteps(self.steps + other.steps)

    def __eq__(self, other):
        return self.steps == other.steps

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
              ), (11, 16, 21, 26))
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
            ), (11, 16, 21, 26))
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
            ), (6, 11, 16, 21, 26))
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
                 ), (6, 11, 16, 21, 26))

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, leveling_costs: Tuple, reborn_milestones: Tuple):
        self.leveling_costs = leveling_costs
        self.reborn_milestones = reborn_milestones

    def __str__(self):
        return self.name.lower().capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Rarity]:
        try:
            return Rarity[s.upper()]
        except KeyError:
            return None


@unique
class Shape(Enum):
    BUILDING = auto()
    MELEE = auto()
    RANGED = auto()

    def __str__(self):
        return self.name.lower().capitalize()

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
        return self.name.lower().capitalize()

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
        return self.name.lower().capitalize()

    @staticmethod
    def from_s(s: str) -> Optional[Gender]:
        try:
            return Gender[s.upper()]
        except KeyError:
            return None
