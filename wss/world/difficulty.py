"""Difficulty levels and the map-generation settings for each one.

Generation strategy (this is the documentation the assignment asks for):

    For every square, the generator rolls a number from 1 to 100 and picks
    the terrain whose range contains that roll. The ranges come from the
    terrain percentages below, laid end to end. For example, on Easy,
    Plains covers rolls 1-45, Forest 46-70, and so on.

    Then, for each item type (food, water, gold, trader), it rolls 1-100
    again. If the roll is at or below that item's chance, the item is
    added to the square. A second roll decides whether a bonus repeats.
    Traders always repeat.

    Easy   - Mostly plains and forest, with plenty of items.
    Medium - A balanced mix of terrain, with fewer items.
    Hard   - Mostly swamp, desert, and mountain, with scarce items and
             almost no repeating bonuses.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from wss.world.terrain import Desert, Forest, Mountain, Plains, Swamp, Terrain


class Difficulty(Enum):
    """The difficulty levels the user can choose from."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ItemType(Enum):
    """The kinds of items the generator can place in a square."""
    FOOD = "food"
    WATER = "water"
    GOLD = "gold"
    TRADER = "trader"


@dataclass(frozen=True)
class DifficultySettings:
    """All the numbers the map generator needs for one difficulty.

    Attributes:
        terrain_percents: Terrain class -> percent chance (must total 100).
        item_chances: Item type -> percent chance a square gets that item.
        repeat_chances: Item type -> percent chance the bonus repeats.
            Traders are not listed because they always repeat.
    """
    terrain_percents: dict[type[Terrain], int]
    item_chances: dict[ItemType, int]
    repeat_chances: dict[ItemType, int]


# One settings object per difficulty. Change these numbers to rebalance.
DIFFICULTY_SETTINGS: dict[Difficulty, DifficultySettings] = {
    Difficulty.EASY: DifficultySettings(
        terrain_percents={Plains: 45, Forest: 25, Swamp: 10, Desert: 10, Mountain: 10},
        item_chances={ItemType.FOOD: 12, ItemType.WATER: 12,
                      ItemType.GOLD: 8, ItemType.TRADER: 4},
        repeat_chances={ItemType.FOOD: 30, ItemType.WATER: 40, ItemType.GOLD: 10},
    ),
    Difficulty.MEDIUM: DifficultySettings(
        terrain_percents={Plains: 30, Forest: 25, Swamp: 15, Desert: 15, Mountain: 15},
        item_chances={ItemType.FOOD: 8, ItemType.WATER: 8,
                      ItemType.GOLD: 6, ItemType.TRADER: 3},
        repeat_chances={ItemType.FOOD: 20, ItemType.WATER: 30, ItemType.GOLD: 5},
    ),
    Difficulty.HARD: DifficultySettings(
        terrain_percents={Plains: 15, Forest: 20, Swamp: 20, Desert: 20, Mountain: 25},
        item_chances={ItemType.FOOD: 5, ItemType.WATER: 5,
                      ItemType.GOLD: 4, ItemType.TRADER: 2},
        repeat_chances={ItemType.FOOD: 10, ItemType.WATER: 20, ItemType.GOLD: 0},
    ),
}
