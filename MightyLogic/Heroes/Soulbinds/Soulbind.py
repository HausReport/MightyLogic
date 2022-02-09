from __future__ import annotations

from dataclasses import dataclass
from typing import List

from MightyLogic.Heroes.Attributes.Rarity import Rarity
from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.Soulbinds.SoulbindRequirements import SoulbindRequirements


@dataclass(frozen=True)
class Soulbind:
    for_hero: Hero
    target_heroes: List[Hero]
    requirements: SoulbindRequirements

    def __post_init__(self):
        self.requirements.validate(self.for_hero, self.target_heroes)

    @staticmethod
    def optimal_soulbind_level(for_rarity: Rarity) -> int:
        return max(
            req.target_level_count
            for rarity in Rarity
            for req in Rarity.soulbind_requirements(rarity)
            if req.target_rarity == for_rarity
        )
