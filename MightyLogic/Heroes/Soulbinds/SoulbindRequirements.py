from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Hero import Hero


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
    def for_rarity(rarity: Rarity) -> List[SoulbindRequirements]:
        if rarity == Rarity.COMMON:
            return FOR_COMMON
        elif rarity == Rarity.RARE:
            return FOR_RARE
        elif rarity == Rarity.EPIC:
            return FOR_EPIC
        elif rarity == Rarity.LEGENDARY:
            return FOR_LEGENDARY
        else:
            raise RuntimeError(f"Unexpected rarity (was: {rarity})")

    @staticmethod
    def _from_tuple(for_rarity: Rarity, tuples: List[Tuple]) -> List[SoulbindRequirements]:
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


FOR_COMMON = SoulbindRequirements._from_tuple(Rarity.COMMON, [
    (Rarity.COMMON, 6),
    (Rarity.COMMON, 11),
    (Rarity.COMMON, 16),
    (Rarity.RARE, 11)
])
FOR_RARE = SoulbindRequirements._from_tuple(Rarity.RARE, [
    (Rarity.RARE, 5),
    (Rarity.RARE, 9),
    (Rarity.RARE, 13),
    (Rarity.EPIC, 7)
])
FOR_EPIC = SoulbindRequirements._from_tuple(Rarity.EPIC, [
    (Rarity.EPIC, 3),
    (Rarity.EPIC, 6),
    (Rarity.EPIC, 8),
    (Rarity.LEGENDARY, 5)
])
FOR_LEGENDARY = SoulbindRequirements._from_tuple(Rarity.LEGENDARY, [
    (Rarity.LEGENDARY, 2),
    (Rarity.LEGENDARY, 3),
    (Rarity.LEGENDARY, 4),
    (Rarity.LEGENDARY, 6)
])
