import pytest

from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.HeroDirectory import HeroDirectory


@pytest.fixture
def hero_dir() -> HeroDirectory:
    return HeroDirectory.default()


@pytest.fixture
def singer(hero_dir) -> Hero:
    return hero_dir.find_by_name("Singer")


@pytest.fixture
def minstrel(hero_dir) -> Hero:
    return hero_dir.find_by_name("Minstrel")


@pytest.fixture
def bard(hero_dir) -> Hero:
    return hero_dir.find_by_name("Bard")


@pytest.fixture
def apollo(hero_dir) -> Hero:
    return hero_dir.find_by_name("Apollo")


# find

def test_find(hero_dir):
    # ID
    maybe_hero = hero_dir.find(186)
    assert maybe_hero and maybe_hero.name == "Tani Windrunner"

    # str(ID)
    maybe_hero = hero_dir.find("186")
    assert maybe_hero and maybe_hero.name == "Tani Windrunner"

    # Exact name
    maybe_hero = hero_dir.find("Tani Windrunner")
    assert maybe_hero and maybe_hero.num == 186

    # Word
    maybe_hero = hero_dir.find("tAnI")  # Ti[tani]a comes first when ordered by ID, hence biasing for word matches
    assert maybe_hero and maybe_hero.num == 186

    # Substring
    maybe_hero = hero_dir.find("rOOm")  # Only match is Sh[room]kin
    assert maybe_hero and maybe_hero.num == 162


def test_find_by_num(hero_dir):
    maybe_hero = hero_dir.find_by_num(90)
    assert maybe_hero and maybe_hero.name == "Dark Mage"

    maybe_hero = hero_dir.find_by_num(1)
    assert not maybe_hero


def test_find_by_name(hero_dir):
    maybe_hero = hero_dir.find_by_name("Dark Mage")
    assert maybe_hero and maybe_hero.num == 90

    maybe_hero = hero_dir.find_by_name("")
    assert not maybe_hero

    maybe_hero = hero_dir.find_by_name("asdhadjad")
    assert not maybe_hero


# evolving

def test_evolves_to(singer, minstrel, bard, apollo, hero_dir):
    # Hero w/ no evolutions (any legendary works)
    assert not apollo.evolves_to

    # Hero w/ exactly one evolution
    assert minstrel.evolves_to == {bard}
    assert bard.evolves_to == {apollo}

    # Hero w/ many evolutions
    assert singer.evolves_to == {
        minstrel,
        hero_dir.find_by_name("Voltage Tower"),
        hero_dir.find_by_name("Squire")
    }


def test_evolves_from(singer, minstrel, bard, apollo, hero_dir):
    # Hero w/ no evolutions to (any common works)
    assert not singer.evolves_from

    # Hero w/ exactly one evolution to
    assert bard.evolves_from == {minstrel}
    assert apollo.evolves_from == {bard}

    # Hero w/ multiple evolutions to
    assert minstrel.evolves_from == {
        singer,
        hero_dir.find_by_name("Gnome"),
        hero_dir.find_by_name("Archer")
    }


def test_all_evolutions_to(singer, minstrel, bard, apollo, hero_dir):
    assert not singer.all_evolutions_to()
    assert minstrel.all_evolutions_to() == {
        singer,
        hero_dir.find_by_name("Gnome"),
        hero_dir.find_by_name("Archer")
    }
    assert bard.all_evolutions_to() == minstrel.all_evolutions_to(include_self=True)
    assert apollo.all_evolutions_to() == bard.all_evolutions_to(include_self=True)
