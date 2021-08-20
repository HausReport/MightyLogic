from __future__ import annotations

import json
from typing import Any, Dict, Tuple

from Heroes import Rarity, Shape, Alignment, Gender, LevelingCost, Level, LevelingSteps


class Hero:
    num: int
    name: str
    rarity: Rarity
    shape: Shape
    alignment: Alignment
    gender: Gender
    evolves_to_nums: Tuple
    soulbind_nums: Tuple

    def __init__(self, num: int, name: str, rarity: Rarity, shape: Shape, alignment: Alignment, gender: Gender,
                 evolves_to_nums: Tuple = (), soulbind_nums: Tuple = ()):
        if shape is Shape.BUILDING and gender is not Gender.SEXLESS:
            raise RuntimeError(f"Buildings must be sexless (was: {num}. {name}: {shape}, {gender})")

        self.num = num
        self.name = name
        self.rarity = rarity
        self.shape = shape
        self.alignment = alignment
        self.gender = gender
        self.evolves_to_nums = evolves_to_nums
        self.soulbind_nums = soulbind_nums

    def __eq__(self, other):
        return self.num == other.num

    def __hash__(self):
        return self.num

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.num}: {self.name} ({self.rarity} / {self.shape} / {self.alignment} / {self.gender})"

    def leveling_cost(self, to_level: Level) -> LevelingCost:
        return LevelingCost.free() if to_level.level_count == 1 else self.rarity.leveling_costs[to_level.level_count - 2]

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
        return self.to_dict()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.num,
            "name": self.name,
            "rarity": self.rarity.name.capitalize(),
            "shape": self.shape.name.capitalize(),
            "alignment": self.alignment.name.capitalize(),
            "gender": self.gender.name.capitalize(),
            "evolves_to": self.evolves_to_nums
        }

    # TODO: Move into Codec.Rec
    def to_rec(self) -> Dict[str, Any]:
        return self.to_dict()

    @staticmethod
    def from_csv(row: Dict[str, Any]) -> Hero:
        return Hero.from_rec(row)

    @staticmethod
    def from_rec(rec: Dict[str, Any]) -> Hero:
        def evolves_to_nums(serialized):
            return serialized if isinstance(serialized, list) else json.loads(serialized)

        return Hero(
            num=int(rec["id"]),
            name=rec["name"],
            rarity=Rarity.from_s(rec["rarity"]),
            shape=Shape.from_s(rec["shape"]),
            alignment=Alignment.from_s(rec["alignment"]),
            gender=Gender.from_s(rec["gender"]),
            evolves_to_nums=evolves_to_nums(rec["evolves_to"]) if "evolves_to" in rec.keys() else ()
        )
