import csv
import importlib

import MightyLogic.Heroes
from MightyLogic.Heroes.HeroDirectory import HeroDirectory

hero_dir = HeroDirectory.default()
unseen_heroes = set(hero_dir.values())

with open("/workplace/becole/mp/scratch/evolves.csv", newline="") as evo_f:
    evo_reader = csv.DictReader(evo_f, delimiter=";")
    for row in evo_reader:
        hero = hero_dir.find_by_num(int(row["ID"]))
        assert hero.name.lower() == row["Name"].lower(), f"{hero.name} !== {row['Name']}"

        unseen_heroes.remove(hero)

        evolves_to_nums = []
        evolves_to_names = set()
        for x in ("A", "B", "C"):
            evolves_to_name = row[f"Evolves To {x}"].lower()

            if not evolves_to_name or evolves_to_name == "-":
                continue

            evolves_to = hero_dir.find(evolves_to_name)
            assert evolves_to.name.lower() == evolves_to_name, f"{evolves_to.name} !== {evolves_to_name}"
            evolves_to_nums.append(evolves_to.num)
            evolves_to_names.add(evolves_to_name)

        hero.evolves_to_nums = evolves_to_nums

        expected_names = set(hero.name.lower() for hero in hero_dir.evolutions_from(hero))
        assert evolves_to_names == expected_names, f"{evolves_to_names} !== {expected_names}"

assert not unseen_heroes, f"Data is missing for following heroes: {unseen_heroes}"

with importlib.resources.path(MightyLogic.Heroes, "UpdatedHeroDirectory.csv") as to_path:
    hero_dir.to_csv_file(to_path)
    updated_hero_dir = HeroDirectory.from_csv_file(to_path)

