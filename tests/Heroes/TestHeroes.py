import pytest

from MightyLogic.Heroes.Collection import Collection, HeroSelector
from MightyLogic.Heroes.Hero import Hero, Rarity, Shape, Alignment, Gender, Level, LevelingCost, LevelingSteps
from MightyLogic.Heroes.HeroDirectory import HeroDirectory
from MightyLogic.Heroes.OwnedHero import OwnedHero

# ======================================================================================================================
# LevelOwnedHero
# ----------------------------------------------------------------------------------------------------------------------

l_1_rb_0 = Level(1, 0)
l_2_rb_0 = Level(2, 0)
l_1_rb_1 = Level(1, 1)
l_2_rb_1 = Level(2, 1)


# constructor

@pytest.mark.parametrize("__description,level,reborn", [
    ("level < min", 0, 0),
    ("level > max", 22, 0),
    ("reborn < min", 1, -1),
    ("reborn > max", 1, 5)
])
def test_level_constructor(__description, level, reborn):
    with pytest.raises(RuntimeError):
        Level(level, reborn)


# accessors

def test_level_accessors():
    assert l_1_rb_0.level_count == 1
    assert l_1_rb_0.reborn_count == 0


# mutators

def test_level_reborn():
    reborn = l_2_rb_0.reborn()
    assert reborn == l_1_rb_1  # reborn resets level to 0
    assert l_2_rb_0 == Level(2, 0)  # reborn should not mutate the original level


def test_level_level_up():
    leveled = l_1_rb_0.level_up()
    assert leveled == l_2_rb_0  # leveling doesn't increase reborn
    assert l_1_rb_0 == Level(1, 0)  # leveling should not mutate the original level


# comparators

def test_level_comparators():
    assert list(sorted([l_2_rb_0, l_1_rb_0, l_2_rb_1, l_1_rb_1, l_2_rb_1])) == [
        l_1_rb_0,
        l_2_rb_0,
        l_1_rb_1,
        l_2_rb_1,
        l_2_rb_1
    ]


# ======================================================================================================================
# LevelingCost
# ----------------------------------------------------------------------------------------------------------------------

s_1_g_10 = LevelingCost(1, 10)
s_2_g_20 = LevelingCost(2, 20)
s_3_g_30 = LevelingCost(3, 30)


# constructor

@pytest.mark.parametrize("__description,souls,gold", [
    ("souls < min", 0, 1),
    ("gold < min", 1, 0),
])
def test_level_constructor(__description, souls, gold):
    with pytest.raises(RuntimeError):
        LevelingCost(souls, gold)


# accessors

def test_leveling_cost_accessors():
    assert s_1_g_10.gold == 10
    assert s_1_g_10.souls == 1


# comparators

def test_leveling_cost_comparators():
    assert list(sorted([s_3_g_30, s_1_g_10, s_2_g_20, s_1_g_10])) == [
        s_1_g_10,
        s_1_g_10,
        s_2_g_20,
        s_3_g_30
    ]


# static factories

def test_leveling_cost_free():
    free = LevelingCost.free()
    assert free.gold == 0 and free.souls == 0


# ======================================================================================================================
# LevelingSteps
# ----------------------------------------------------------------------------------------------------------------------

test_steps = LevelingSteps([
    (l_2_rb_0, s_1_g_10),
    (l_1_rb_1, LevelingCost.free()),
    (l_2_rb_1, s_3_g_30)
])


# aggregate cost

def test_leveling_steps_aggregate_cost():
    aggregate_cost = test_steps.aggregate_cost()
    assert aggregate_cost.souls == 4 and aggregate_cost.gold == 40


# final level

def test_leveling_steps_final_level():
    assert test_steps.final_level() == l_2_rb_1


# level up count

def test_leveling_steps_level_up_count():
    assert test_steps.level_up_count() == 2  # reborn step doesn't count


# ======================================================================================================================
# Hero
# ----------------------------------------------------------------------------------------------------------------------

common_hero = Hero(1, "Common -.-", Rarity.COMMON, Shape.MELEE, Alignment.CHAOS, Gender.FEMALE)
rare_hero = Hero(2, "Rare :)", Rarity.RARE, Shape.RANGED, Alignment.ORDER, Gender.MALE)
epic_hero = Hero(3, "Epic :D", Rarity.EPIC, Shape.BUILDING, Alignment.CHAOS, Gender.SEXLESS)
legendary_hero = Hero(4, "Legendary :)))", Rarity.LEGENDARY, Shape.MELEE, Alignment.NATURE, Gender.FEMALE)


# accessors

def test_hero_accessors():
    assert epic_hero.num == 3
    assert epic_hero.name == "Epic :D"
    assert epic_hero.rarity == Rarity.EPIC
    assert epic_hero.shape == Shape.BUILDING
    assert epic_hero.alignment == Alignment.CHAOS
    assert epic_hero.gender == Gender.SEXLESS


# reborn milestone

def test_hero_reborn_milestone():
    assert common_hero.reborn_milestone(l_1_rb_0) == 11
    assert rare_hero.reborn_milestone(l_1_rb_1) == 16
    assert epic_hero.reborn_milestone(l_2_rb_0) == 6
    assert legendary_hero.reborn_milestone(l_2_rb_1) == 11


# leveling cost

def test_hero_leveling_cost():
    assert common_hero.leveling_cost(l_1_rb_0) == LevelingCost.free()
    assert rare_hero.leveling_cost(l_2_rb_1) == LevelingCost(25, 100)
    assert epic_hero.leveling_cost(Level(6, 2)) == LevelingCost(80, 1900)
    assert legendary_hero.leveling_cost(Level(21, 2)) == LevelingCost(1700, 48000)


# leveling steps

def test_hero_leveling_steps_same_reborn_():
    assert epic_hero.leveling_steps(l_1_rb_0, Level(6, 0)) == LevelingSteps([
        (Level(2, 0), LevelingCost(15, 300)),
        (Level(3, 0), LevelingCost(30, 600)),
        (Level(4, 0), LevelingCost(45, 900)),
        (Level(5, 0), LevelingCost(60, 1400)),
        (Level(6, 0), LevelingCost(80, 1900)),
    ])


def test_hero_leveling_steps_different_reborn():
    with pytest.raises(RuntimeError, match="same reborn count"):
        epic_hero.leveling_steps(l_1_rb_0, l_2_rb_1)


def test_hero_leveling_steps_from_gt_to():
    with pytest.raises(RuntimeError, match="must be lower than"):
        epic_hero.leveling_steps(l_2_rb_0, l_1_rb_0)


# ======================================================================================================================
# OwnedHero
# ----------------------------------------------------------------------------------------------------------------------

empty_oh = OwnedHero(epic_hero, l_1_rb_0, 0)
rebornable_oh = OwnedHero(common_hero, Level(11, 0), 0)
levelable_oh = OwnedHero(legendary_hero, l_1_rb_1, 100)
both_oh = OwnedHero(rare_hero, Level(11, 0), 10000)


# accessors

def test_owned_hero_accessors():
    assert empty_oh.hero == epic_hero
    assert empty_oh.level == l_1_rb_0
    assert empty_oh.souls == 0


# TODO: cost to next level
# TODO: reborn milestone
# TODO: leveling steps to


# tests

def test_owned_hero_can_reborn():
    assert empty_oh.can_reborn() is False
    assert rebornable_oh.can_reborn() is True
    assert levelable_oh.can_reborn() is False
    assert both_oh.can_reborn() is True


def test_owned_hero_can_level_up():
    # w/ infinite gold:
    assert empty_oh.can_level_up() is False
    assert rebornable_oh.can_level_up() is False
    assert levelable_oh.can_level_up() is True
    assert both_oh.can_level_up() is True

    # w/ constrained gold:
    assert levelable_oh.can_level_up(with_gold=1) is False
    assert levelable_oh.can_level_up(with_gold=100_000) is True


def test_owned_hero_can_level_up_after_reborn():
    # w/ infinite gold:
    assert empty_oh.can_level_up_after_reborn() is False
    assert rebornable_oh.can_level_up_after_reborn() is False
    assert levelable_oh.can_level_up_after_reborn() is False
    assert both_oh.can_level_up_after_reborn() is True

    # w/ constrained gold:
    assert both_oh.can_level_up_after_reborn(with_gold=1) is False
    assert both_oh.can_level_up_after_reborn(with_gold=100_000) is True


# mutators

# TODO: level up
# TODO: reborn


# static factories

def test_owned_hero_from_squad_export():
    mother_owl = Hero(22, "Mother Owl", Rarity.LEGENDARY, Shape.RANGED, Alignment.NATURE, Gender.FEMALE)
    hero_dir = HeroDirectory({mother_owl})

    oh = OwnedHero.from_squad_export(
        " 22: Mother Owl                   61/119  Level 14 Reborn 2 Unused Souls 24",
        hero_dir
    )

    assert oh.hero == mother_owl
    assert oh.level == Level(14, 2)
    assert oh.souls == 24


# ======================================================================================================================
# HeroDirectory
# ----------------------------------------------------------------------------------------------------------------------

hero_dir = HeroDirectory.default()

singer = hero_dir.find_by_name("Singer")
minstrel = hero_dir.find_by_name("Minstrel")
bard = hero_dir.find_by_name("Bard")
apollo = hero_dir.find_by_name("Apollo")


# find

def test_find():
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


def test_find_by_num():
    maybe_hero = hero_dir.find_by_num(90)
    assert maybe_hero and maybe_hero.name == "Dark Mage"

    maybe_hero = hero_dir.find_by_num(1)
    assert not maybe_hero


def test_find_by_name():
    maybe_hero = hero_dir.find_by_name("Dark Mage")
    assert maybe_hero and maybe_hero.num == 90

    maybe_hero = hero_dir.find_by_name("")
    assert not maybe_hero

    maybe_hero = hero_dir.find_by_name("asdhadjad")
    assert not maybe_hero


# evolving

def test_evolves_to():
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


def test_evolves_from():
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


def test_all_evolutions_to():
    assert not singer.all_evolutions_to()
    assert minstrel.all_evolutions_to() == {
        singer,
        hero_dir.find_by_name("Gnome"),
        hero_dir.find_by_name("Archer")
    }
    assert bard.all_evolutions_to() == minstrel.all_evolutions_to(include_self=True)
    assert apollo.all_evolutions_to() == bard.all_evolutions_to(include_self=True)


# ======================================================================================================================
# Collection
# ----------------------------------------------------------------------------------------------------------------------

collection = Collection(hero_dir, set())  # FIXME: provide non-empty set of owned heroes


# ======================================================================================================================
# HeroSelector
# ----------------------------------------------------------------------------------------------------------------------

common_selector = HeroSelector.has_rarity(Rarity.COMMON)
rare_selector = HeroSelector.has_rarity(Rarity.RARE)
epic_selector = HeroSelector.has_rarity(Rarity.EPIC)
leg_selector = HeroSelector.has_rarity(Rarity.LEGENDARY)


def test_evolutions_to():
    assert HeroSelector.all_evolutions_to({"apollo"}).select(collection) == apollo.all_evolutions_to()
    assert HeroSelector.all_evolutions_to({"minstrel"}, inclusive=True).select(collection)\
           == minstrel.all_evolutions_to(include_self=True)


def test_exactly():
    assert HeroSelector.exactly(["grace", "eostre"]).select(collection) == {
        hero_dir.find("grace"),
        hero_dir.find("eostre")
    }


def test_has_rarity():
    assert common_selector.select(collection) == set(
        hero
        for hero in hero_dir.values()
        if hero.rarity == Rarity.COMMON
    )


def test_and():
    two = common_selector + leg_selector
    assert two.of_selectors == [common_selector, leg_selector]
    assert two.select(collection) == set(
        hero
        for hero in hero_dir.values()
        if hero.rarity in {Rarity.COMMON, Rarity.LEGENDARY}
    )

    three = common_selector + rare_selector + epic_selector
    assert three.of_selectors == [common_selector, rare_selector, epic_selector]
    assert three.select(collection) == set(
        hero
        for hero in hero_dir.values()
        if hero.rarity in {Rarity.COMMON, Rarity.LEGENDARY, Rarity.EPIC}
    )


def test_complement():
    assert leg_selector.complement().select(collection) == set(
        hero
        for hero in hero_dir.values()
        if hero.rarity != Rarity.LEGENDARY
    )

    assert rare_selector.complement().complement() == rare_selector

