from dataclasses import dataclass
from typing import Dict, List

from Heroes import Rarity
from Heroes.Hero import Hero
from Heroes.HeroDirectory import HeroDirectory


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


class SoulbindDirectory:
    soulbinds_by_hero: Dict[int, List[Soulbind]]

    def __init__(self, hero_dir: HeroDirectory):
        requirements_by_rarity: Dict[Rarity, List[SoulbindRequirements]] = self.__resolve_requirements()
        self.soulbinds_by_hero = self.__resolve_soulbinds(hero_dir, requirements_by_rarity)

    def soulbinds_needed_by(self, hero: Hero):
        return None  # FIXME

    def soulbinds_provided_by(self, hero: Hero):
        return None  # FIXME

    @staticmethod
    def __resolve_soulbinds(hero_dir: HeroDirectory, requirements_by_rarity: Dict[Rarity, List[SoulbindRequirements]])\
            -> Dict[int, List[Soulbind]]:
        soulbinds_by_hero: Dict[int, List[Soulbind]] = dict()
        for hero in hero_dir.values():
            if not hero.soulbind_nums:  # TODO: remove this once soulbind info is added
                continue

            soulbinds: List[Soulbind] = list()
            for expected_level, requirements in enumerate(requirements_by_rarity[hero.rarity]):
                assert expected_level == requirements.soulbind_level
                target_heroes = list(
                    hero_dir.find_by_num(target_hero_num)
                    for target_hero_num in hero.soulbind_nums[requirements.soulbind_level]
                )
                soulbinds.append(Soulbind(hero, target_heroes, requirements))
            soulbinds_by_hero[hero.num] = soulbinds
        return soulbinds_by_hero

    @staticmethod
    def __resolve_requirements() -> Dict[Rarity, List[SoulbindRequirements]]:
        requirements_by_rarity: Dict[Rarity, List[SoulbindRequirements]] = dict()
        for rarity in Rarity:
            requirements_by_rarity[rarity] = list(
                SoulbindRequirements(rarity, level, Rarity[target_rarity_name], target_level, target_count)
                for level, (target_rarity_name, target_level, target_count) in enumerate(rarity.soulbind_reqs)
            )
        return requirements_by_rarity
