import pytest

from MightyLogic.Heroes.Collection import Collection
from tests.Heroes.HeroDirectory_test import hero_dir


@pytest.fixture
def collection(hero_dir) -> Collection:
    return Collection(hero_dir, set())  # FIXME: provide non-empty set of owned heroes


# TODO: Tests!!!
