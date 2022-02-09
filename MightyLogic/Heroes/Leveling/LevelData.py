from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from MightyLogic.Heroes.Attributes.Rarity import Rarity


@dataclass(frozen=True)
class LevelDatum:
    level_count: int
    souls: int
    gold: int
    might: int
    troops: int
    required_league: int

    def __post_init__(self):
        assert self.level_count >= 1, "Level count should be >= 1"
        assert self.souls == 0 if self.level_count == 1 else self.souls > 0, \
            "Souls should == 0 for level 1 and be a positive integer in all other cases"
        assert self.gold == 0 if self.level_count == 1 else self.gold > 0, \
            "Gold should == 0 for level 1 and be a positive integer in all other cases"
        assert self.might > 0, "Might should be > 0"
        assert self.troops > 0, "Troops should be > 0"
        assert 1 <= self.required_league <= 30, "Required league should be between 1 and 30 (inclusive)"

    # For easier testing, really
    def with_changes(self, **changed_fields) -> LevelDatum:
        d = self.__dict__.copy()
        d.update(changed_fields)
        return LevelDatum(**d)


@dataclass(frozen=True)
class LevelData:
    data: List[LevelDatum]

    def __post_init__(self):
        assert self.max_level_count() >= self.min_level_count(), \
            f"Not enough data provided (expected: >={self.min_level_count()}, received: {self.max_level_count()})"

        previous = None
        for current in self.data:
            if previous is None:
                assert current.level_count == self.min_level_count(), \
                    f"First datum should be for level count {self.min_level_count()} (was: {current})"
            else:
                assert current.level_count == previous.level_count + 1, \
                    f"Datum should be consecutive and sequential (was: {current}, prior: {previous})"
                assert current.souls > previous.souls, f"Souls should increase (was: {current}, prior: {previous})"
                assert current.gold > previous.gold, f"Gold should increase (was: {current}, prior: {previous})"
                assert current.might > previous.might, f"Might should increase (was: {current}, prior: {previous})"
                assert current.troops > previous.troops, f"Troops should increase (was: {current}, prior: {previous})"
                assert current.required_league <= previous.required_league, \
                    f"Required league should remain the same OR decrease (was: {current}, prior: {previous})"

            previous = current

    def __getitem__(self, level_count: int) -> LevelDatum:
        self.require_valid_level_count(level_count)

        datum = self.data[level_count - 1]
        assert datum.level_count == level_count
        return datum

    def is_valid_level_count(self, level_count: int) -> bool:
        return self.min_level_count() <= level_count <= self.max_level_count()

    def max_level_count(self) -> int:
        return len(self.data)

    @staticmethod
    def min_level_count() -> int:
        return 1

    def require_valid_level_count(self, level_count: int):
        assert self.is_valid_level_count(level_count), \
            f"Level count must be >= {self.min_level_count()} and <= {self.max_level_count()} (was: {level_count})"

    @staticmethod
    def for_rarity(rarity: Rarity) -> LevelData:
        return LEVELING_DATA_BY_RARITY[rarity]

    @staticmethod
    def _from_tuples(tuples: Tuple) -> LevelData:
        return LevelData([LevelDatum(*t) for t in tuples])


COMMON_LEVELING_DATA = (
    # level |  souls |   gold  | might | troops | league
    # ------+--------+---------+-------+--------+-------
    (     1 ,      0 ,       0 ,   100 ,     20 ,    30 ),
    (     2 ,     25 ,      50 ,   110 ,     22 ,    30 ),
    (     3 ,     50 ,      80 ,   120 ,     24 ,    30 ),
    (     4 ,     75 ,     120 ,   130 ,     26 ,    29 ),
    (     5 ,    100 ,     200 ,   140 ,     28 ,    28 ),
    (     6 ,    150 ,     300 ,   150 ,     30 ,    27 ),
    # ------+--------+---------+-------+--------+-------
    (     7 ,    200 ,    500 ,    170 ,     34 ,    27 ),
    (     8 ,    250 ,  1_000 ,    190 ,     38 ,    26 ),
    (     9 ,    300 ,  1_500 ,    210 ,     42 ,    25 ),
    (    10 ,    350 ,  2_000 ,    230 ,     46 ,    24 ),
    (    11 ,    450 ,  3_000 ,    250 ,     50 ,    24 ),
    # ------+--------+---------+-------+--------+-------
    (    12 ,    600 ,   4_000 ,   280 ,     58 ,    23 ),
    (    13 ,    750 ,   6_000 ,   310 ,     66 ,    23 ),
    (    14 ,    900 ,   8_000 ,   340 ,     74 ,    22 ),
    (    15 ,  1_100 ,  10_000 ,   370 ,     82 ,    21 ),
    (    16 ,  1_400 ,  13_000 ,   400 ,     90 ,    20 ),
    # ------+--------+---------+-------+--------+-------
    (    17 ,  2_000 ,  16_000 ,   450 ,     106 ,   18 ),
    (    18 ,  2_700 ,  19_000 ,   500 ,     122 ,   18 ),
    (    19 ,  3_500 ,  22_000 ,   550 ,     138 ,   18 ),
    (    20 ,  4_500 ,  25_000 ,   600 ,     154 ,   15 ),
    (    21 ,  6_000 ,  28_000 ,   650 ,     170 ,   15 ),
    # ------+--------+---------+-------+--------+-------
    (    22 ,  7_500 ,  32_000 ,   750 ,     186 ,   13 ),
    (    23 ,  9_500 ,  36_000 ,   850 ,     202 ,   13 ),
    (    24 , 12_000 ,  40_000 ,   950 ,     218 ,   13 ),
    (    25 , 15_000 ,  45_000 , 1_050 ,     234 ,   12 ),
    (    26 , 18_000 ,  50_000 , 1_150 ,     250 ,   10 )
)

RARE_LEVELING_DATA = (
    # level |  souls |   gold  | might | troops | league
    # ------+--------+---------+-------+--------+-------
    (     1 ,      0 ,       0 ,   120 ,     25 ,    30 ),
    (     2 ,     25 ,     100 ,   135 ,     28 ,    30 ),
    (     3 ,     50 ,     300 ,   150 ,     31 ,    28 ),
    (     4 ,     75 ,     600 ,   170 ,     34 ,    28 ),
    (     5 ,    100 ,     900 ,   185 ,     37 ,    28 ),
    (     6 ,    130 ,   1_400 ,   200 ,     40 ,    27 ),
    # ------+--------+---------+-------+--------+-------
    (     7 ,    160 ,   2_000 ,   230 ,     46 ,    26 ),
    (     8 ,    190 ,   3_500 ,   260 ,     52 ,    26 ),
    (     9 ,    200 ,   4_000 ,   290 ,     58 ,    24 ),
    (    10 ,    250 ,   5_000 ,   320 ,     64 ,    23 ),
    (    11 ,    330 ,   6_000 ,   350 ,     70 ,    22 ),
    # ------+--------+---------+-------+--------+-------
    (    12 ,    420 ,   8_000 ,   400 ,     82 ,    21 ),
    (    13 ,    500 ,  10_000 ,   450 ,     94 ,    20 ),
    (    14 ,    600 ,  12_000 ,   500 ,    106 ,    19 ),
    (    15 ,    750 ,  14_000 ,   550 ,    118 ,    19 ),
    (    16 ,    950 ,  16_000 ,   600 ,    130 ,    18 ),
    # ------+--------+---------+-------+--------+-------
    (    17 ,  1_400 ,  19_000 ,   680 ,    156 ,    15 ),
    (    18 ,  1_900 ,  22_000 ,   760 ,    182 ,    15 ),
    (    19 ,  2_400 ,  25_000 ,   840 ,    208 ,    13 ),
    (    20 ,  3_000 ,  28_000 ,   920 ,    234 ,    13 ),
    (    21 ,  3_700 ,  32_000 , 1_000 ,    260 ,    13 ),
    # ------+--------+---------+-------+--------+-------
    (    22 ,  4_500 ,  36_000 , 1_140,     288 ,    12 ),
    (    23 ,  5_500 ,  40_000 , 1_280 ,    326 ,    10 ),
    (    24 ,  7_000 ,  45_000 , 1_420 ,    344 ,     9 ),
    (    25 ,  9_000 ,  50_000 , 1_560 ,    372 ,     9 ),
    (    26 , 12_000 ,  55_000 , 1_700 ,    400 ,     9 ),
    # ------+--------+---------+-------+--------+-------
    (    27 , 12_150 ,  57_000 , 1_812 ,    426 ,     7 ),
    (    28 , 12_350 ,  60_000 , 1_924 ,    452 ,     7 ),
    (    29 , 12_550 ,  63_000 , 2_036 ,    478 ,     7 ),
    (    30 , 12_800 ,  66_000 , 2_148 ,    504 ,     6 ),
    (    31 , 13_100 ,  70_000 , 2_260 ,    530 ,     6 ),
)

EPIC_LEVELING_DATA = (
    # level |  souls |   gold  | might | troops | league
    # ------+--------+---------+-------+--------+-------
    (     1 ,      0 ,       0 ,   200 ,     60 ,    30 ),
    (     2 ,     15 ,     300 ,   230 ,     70 ,    30 ),
    (     3 ,     30,      600 ,   260 ,     80 ,    28 ),
    (     4 ,     45,      900 ,   290 ,     90 ,    26 ),
    (     5 ,     60,    1_400 ,   320 ,    100 ,    24 ),
    (     6 ,     80,    1_900 ,   350 ,    110 ,    22 ),
    # ------+--------+---------+-------+--------+-------
    (     7 ,    100,    2_500 ,   390 ,    128 ,    21 ),
    (     8 ,    120,    4_000 ,   430 ,    146 ,    20 ),
    (     9 ,    140,    5_000 ,   470 ,    164 ,    20 ),
    (    10 ,    160,    6_000 ,   510 ,    182 ,    18 ),
    (    11 ,    200,    7_000 ,   550 ,    200 ,    18 ),
    # ------+--------+---------+-------+--------+-------
    (    12 ,    250,    9_000 ,   620 ,    242 ,    17 ),
    (    13 ,    320,   11_000 ,   690 ,    284 ,    17 ),
    (    14 ,    400,   13_000 ,   760 ,    326 ,    15 ),
    (    15 ,    500,   16_000 ,   830 ,    368 ,    15 ),
    (    16 ,    650,   19_000 ,   900 ,    410 ,    13 ),
    # ------+--------+---------+-------+--------+-------
    (    17 ,    900,   22_000 , 1_020 ,    580 ,    13 ),
    (    18 ,  1_100,   26_000 , 1_140 ,    606 ,    13 ),
    (    19 ,  1_350,   30_000 , 1_260 ,    704 ,    12 ),
    (    20 ,  1_800,   34_000 , 1_380 ,    802 ,    10 ),
    (    21 ,  2_300,   38_000 , 1_500 ,    900 ,     9 ),
    # ------+--------+---------+-------+--------+-------
    (    22 ,  3_000,   42_000 , 1_700 ,  1_020 ,     9 ),
    (    23 ,  4_000,   47_000 , 1_900 ,  1_140 ,     9 ),
    (    24 ,  5_000,   52_000 , 2_100 ,  1_260 ,     8 ),
    (    25 ,  6_300,   58_000 , 2_300 ,  1_380 ,     5 ),
    (    26 ,  8_000,   65_000 , 2_500 ,  1_500 ,     5 ),
    # ------+--------+---------+-------+--------+-------
    (    27 ,  8_200,   67_000 , 2_665 ,  1_599 ,     5 ),
    (    28 ,  8_400,   70_000 , 2_830 ,  1_698 ,     5 ),
    (    29 ,  8_650,   73_000 , 2_995 ,  1_797 ,     5 ),
    (    30 ,  8_950,   77_000 , 3_160 ,  1_896 ,     4 ),
    (    31 ,  9_300,   82_000 , 3_325 ,  1_995 ,     4 ),
)

LEGENDARY_LEVELING_DATA = (
    # level |  souls |   gold  | might | troops | league
    # ------+--------+---------+-------+--------+-------
    (     1 ,      0 ,       0 ,   350 ,    100 ,    30 ),
    (     2 ,      5 ,     600 ,   390 ,    118 ,    30 ),
    (     3 ,     10 ,     900 ,   430 ,    136 ,    28 ),
    (     4 ,     15 ,   1_400 ,   470 ,    154 ,    26 ),
    (     5 ,     20 ,   1_900 ,   510 ,    172 ,    24 ),
    (     6 ,     40 ,   2_500 ,   550 ,    190 ,    20 ),
    # ------+--------+---------+-------+--------+-------
    (     7 ,     60 ,   3_500 ,   620 ,    228 ,    18 ),
    (     8 ,     80 ,   5_500 ,   690 ,    266 ,    17 ),
    (     9 ,    100 ,   7_000 ,   760 ,    304 ,    17 ),
    (    10 ,    120 ,   9_000 ,   830 ,    342 ,    16 ),
    (    11 ,    150 ,  11_000 ,   900 ,    380 ,    16 ),
    # ------+--------+---------+-------+--------+-------
    (    12 ,    200 ,  14_000 , 1_010 ,    470 ,    14 ),
    (    13 ,    250 ,  17_000 , 1_120 ,    560 ,    14 ),
    (    14 ,    320 ,  20_000 , 1_230 ,    650 ,    13 ),
    (    15 ,    400 ,  24_000 , 1_340 ,    740 ,    13 ),
    (    16 ,    500 ,  28_000 , 1_450 ,    830 ,    12 ),
    # ------+--------+---------+-------+--------+-------
    (    17 ,    700 ,  32_000 , 1_630 ,  1_064 ,    10 ),
    (    18 ,    850 ,  36_000 , 1_810 ,  1_298 ,     9 ),
    (    19 ,  1_000 ,  40_000 , 1_990 ,  1_532 ,     9 ),
    (    20 ,  1_300 ,  44_000 , 2_170 ,  1_766 ,     9 ),
    (    21 ,  1_700 ,  48_000 , 2_350 ,  2_000 ,     8 ),
    # ------+--------+---------+-------+--------+-------
    (    22 ,  2_200 ,  52_000 , 2_630 ,  2_300 ,     5 ),
    (    23 ,  2_900 ,  57_000 , 2_910 ,  2_600 ,     5 ),
    (    24 ,  3_700 ,  62_000 , 3_190 ,  2_900 ,     4 ),
    (    25 ,  4_800 ,  68_000 , 3_470 ,  3_200 ,     4 ),
    (    26 ,  6_000 ,  75_000 , 3_750 ,  3_500 ,     4 ),
    # ------+--------+---------+-------+--------+-------
    (    27 ,  6_150 ,  80_000 , 3_998 ,  3_731 ,     3 ),
    (    28 ,  6_300 ,  86_000 , 4_246 ,  3_962 ,     3 ),
    (    29 ,  6_450 ,  93_000 , 4_494 ,  4_193 ,     3 ),
    (    30 ,  6_650 , 101_000 , 4_742 ,  4_424 ,     2 ),
    (    31 ,  6_900 , 110_000 , 4_990 ,  4_655 ,     2 ),
)

LEVELING_DATA_BY_RARITY = {
    Rarity.COMMON: LevelData._from_tuples(COMMON_LEVELING_DATA),
    Rarity.RARE: LevelData._from_tuples(RARE_LEVELING_DATA),
    Rarity.EPIC: LevelData._from_tuples(EPIC_LEVELING_DATA),
    Rarity.LEGENDARY: LevelData._from_tuples(LEGENDARY_LEVELING_DATA)
}
