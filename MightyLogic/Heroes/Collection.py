from __future__ import annotations

from pathlib import Path

from Heroes.HeroDirectory import HeroDirectory
from Heroes.OwnedHeroDirectory import OwnedHeroDirectory
from Heroes.SoulbindDirectory import SoulbindDirectory


class Collection:
    hero_dir: HeroDirectory
    oh_dir: OwnedHeroDirectory
    sb_dir: SoulbindDirectory

    def __init__(self, hero_dir: HeroDirectory, oh_dir: OwnedHeroDirectory, sb_dir: SoulbindDirectory):
        self.hero_dir = hero_dir
        self.oh_dir = oh_dir
        self.sb_dir = sb_dir

    @staticmethod
    def from_squad_export_file(path_to_squad_export_file: Path) -> Collection:
        hero_dir = HeroDirectory.default()
        oh_dir = OwnedHeroDirectory.from_squad_export_file(path_to_squad_export_file, hero_dir)
        sb_dir = SoulbindDirectory(hero_dir)
        return Collection(hero_dir, oh_dir, sb_dir)
