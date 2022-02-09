from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from MightyLogic.Heroes.Attributes.Rarity import Rarity


@dataclass
class RebornDatum:
    reborn_count: int
    required_level: int
    might: int
    troops: int

    def __post_init__(self):
        assert self.reborn_count >= 0, "Reborn count must be >= 0"
        assert self.required_level == 0 if self.reborn_count == 0 else self.required_level > 0, \
            "Required level must == 0 for reborn 0 and be a positive integer in all other cases"
        assert self.might == 0 if self.reborn_count == 0 else self.might > 0, \
            "Might must == 0 for reborn 0 and be a positive integer in all other cases"
        assert self.troops == 0 if self.reborn_count == 0 else self.troops > 0, \
            "Troops must == 0 for reborn 0 and be a positive integer in all other cases"

    # For easier testing, really
    def with_changes(self, **changed_fields) -> RebornDatum:
        d = self.__dict__.copy()
        d.update(changed_fields)
        return RebornDatum(**d)

    @staticmethod
    def zero() -> RebornDatum:
        return RebornDatum(0, 0, 0, 0)


@dataclass
class RebornData:
    data: List[RebornDatum]

    def __post_init__(self):
        assert self.max_reborn_count() >= self.min_reborn_count(), \
            f"Not enough data provided (expected: >={self.min_reborn_count()}, received: {self.max_reborn_count()})"

        previous = None
        for current in self.data:
            if previous is None:
                assert current.reborn_count == self.min_reborn_count(),\
                    f"First datum must be for reborn count {self.min_reborn_count()} (was: {current})"
            else:
                assert current.reborn_count == previous.reborn_count + 1, \
                    f"Datum must be consecutive and sequential (was: {current}, prior: {previous})"
                assert current.required_level > previous.required_level, \
                    f"Required level must increase with each reborn (was: {current}, prior: {previous})"
                assert current.might > previous.might, \
                    f"Might must increase with each reborn (was: {current}, prior: {previous})"
                assert current.troops > previous.troops, \
                    f"Troops must increase with each reborn (was: {current}, prior: {previous})"

            previous = current

    def __getitem__(self, reborn_count: int) -> RebornDatum:
        self.require_valid_reborn_count(reborn_count)

        datum = self.data[reborn_count]
        assert datum.reborn_count == reborn_count
        return datum

    def cumulative_might(self, reborn_count: int) -> int:
        self.require_valid_reborn_count(reborn_count)

        return sum([d.might for d in self.data if d.reborn_count <= reborn_count])

    def cumulative_troops(self, reborn_count: int) -> int:
        self.require_valid_reborn_count(reborn_count)

        return sum([d.troops for d in self.data if d.reborn_count <= reborn_count])

    def is_valid_reborn_count(self, reborn_count: int) -> bool:
        return self.min_reborn_count() <= reborn_count <= self.max_reborn_count()

    def max_reborn_count(self) -> int:
        return len(self.data) - 1

    @staticmethod
    def min_reborn_count() -> int:
        return 0

    def require_valid_reborn_count(self, reborn_count: int) -> None:
        assert self.is_valid_reborn_count(reborn_count), \
            f"Reborn count must be >= 0 and <= {self.max_reborn_count()} (was: {reborn_count})"

    @staticmethod
    def for_rarity(rarity: Rarity) -> RebornData:
        return REBORN_DATA_BY_RARITY[rarity]

    @staticmethod
    def _from_tuples(tuples: Tuple) -> RebornData:
        return RebornData([RebornDatum(*t) for t in tuples])

COMMON_REBORN_DATA = (
    # reborn | lvl | might | troops
    (      0 ,   0 ,     0 ,      0 ),
    (      1 ,  11 ,   100 ,     24 ),
    (      2 ,  16 ,   150 ,     48 ),
    (      3 ,  21 ,   250 ,     85 ),
    (      4 ,  26 ,   500 ,    150 ),
)

RARE_REBORN_DATA = (
    # reborn | lvl | might | troops
    (      0 ,   0 ,     0 ,      0 ),
    (      1 ,  11 ,   150 ,     42 ),
    (      2 ,  16 ,   250 ,     88 ),
    (      3 ,  21 ,   400 ,    168 ),
    (      4 ,  26 ,   700 ,    320 ),
)

EPIC_REBORN_DATA = (
    # reborn | lvl | might | troops
    (      0 ,   0 ,     0 ,      0 ),
    (      1 ,   6 ,   150 ,     60 ),
    (      2 ,  11 ,   200 ,    145 ),
    (      3 ,  16 ,   350 ,    360 ),
    (      4 ,  21 ,   600 ,    750 ),
    (      5 ,  26 , 1_000 ,  1_350 ),
)

LEGENDARY_REBORN_DATA = (
    # reborn | lvl | might | troops
    (      0 ,   0 ,     0 ,      0 ),
    (      1 ,   6 ,   200 ,    102 ),
    (      2 ,  11 ,   350 ,    268 ),
    (      3 ,  16 ,   650 ,    751 ),
    (      4 ,  21 , 1_200 ,  1_583 ),
    (      5 ,  26 , 1_700 ,  2_957 ),
)

REBORN_DATA_BY_RARITY = {
    Rarity.COMMON: RebornData._from_tuples(COMMON_REBORN_DATA),
    Rarity.RARE: RebornData._from_tuples(RARE_REBORN_DATA),
    Rarity.EPIC: RebornData._from_tuples(EPIC_REBORN_DATA),
    Rarity.LEGENDARY: RebornData._from_tuples(LEGENDARY_REBORN_DATA)
}
