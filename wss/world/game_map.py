"""The WSS map: a grid of squares, plus the logic that generates it.

This file is named game_map.py instead of map.py because map() is a
built-in Python function, and a module named "map" would be confusing.
"""

from __future__ import annotations

import random
from typing import Optional

from wss.items.bonus import FoodBonus, GoldBonus, WaterBonus
from wss.items.item import Item
from wss.items.trader import TRADER_TYPES
from wss.world.difficulty import (DIFFICULTY_SETTINGS, Difficulty,
                                  DifficultySettings, ItemType)
from wss.world.square import Square
from wss.world.terrain import Terrain

# How much each bonus gives, as an inclusive (low, high) range.
BONUS_AMOUNT_RANGES: dict[ItemType, tuple[int, int]] = {
    ItemType.FOOD: (3, 6),
    ItemType.WATER: (3, 6),
    ItemType.GOLD: (1, 5),
}


class Map:
    """A rectangular grid of squares.

    Coordinates: x is the column (0 = west edge, width - 1 = east edge),
    and y is the row (0 = north edge, height - 1 = south edge).

    Attributes:
        width: Number of squares from west to east.
        height: Number of squares from north to south.
    """

    def __init__(self, rng: Optional[random.Random] = None) -> None:
        """Create an empty map. Call generate() to fill it.

        Args:
            rng: Optional random number generator. Pass random.Random(seed)
                to get the same map every time, which helps with testing.
        """
        self.width = 0
        self.height = 0
        self._squares: list[list[Square]] = []  # Indexed as _squares[y][x]
        self._rng = rng or random.Random()

    # ------------------------------------------------------------------
    # Public methods (match the class diagram)
    # ------------------------------------------------------------------

    def generate(self, width: int, height: int, difficulty: Difficulty) -> None:
        """Build a new map of the given size using the difficulty's settings.

        Follows the map-generation activity diagram: for every square, pick
        a terrain by rolling 1-100, then roll for each item type.
        """
        if width < 1 or height < 1:
            raise ValueError("Map width and height must be at least 1.")

        self.width = width
        self.height = height
        settings = DIFFICULTY_SETTINGS[difficulty]

        self._squares = []
        for y in range(height):
            row = []
            for x in range(width):
                square = Square(x, y, self._roll_terrain(settings))
                self._roll_items(square, settings)
                row.append(square)
            self._squares.append(row)

    def get_square(self, x: int, y: int) -> Optional[Square]:
        """Return the square at (x, y), or None if it is off the map."""
        if not self.in_bounds(x, y):
            return None
        return self._squares[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is a valid square on the map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def random_start_row(self) -> int:
        """Pick a random row on the west edge for the player to start in."""
        return self._rng.randrange(self.height)

    def all_squares(self) -> list[Square]:
        """Return every square, row by row, from north-west to south-east."""
        return [square for row in self._squares for square in row]

    # ------------------------------------------------------------------
    # Generation helpers
    # ------------------------------------------------------------------

    def _roll_terrain(self, settings: DifficultySettings) -> Terrain:
        """Roll 1-100 and return the terrain whose range contains the roll.

        The percentages are laid end to end. With Plains 45 and Forest 25,
        Plains covers rolls 1-45 and Forest covers 46-70.
        """
        roll = self._rng.randint(1, 100)
        upper_bound = 0
        for terrain_class, percent in settings.terrain_percents.items():
            upper_bound += percent
            if roll <= upper_bound:
                return terrain_class()
        raise ValueError("Terrain percentages must add up to 100.")

    def _roll_items(self, square: Square, settings: DifficultySettings) -> None:
        """Roll once per item type, and add any items that pass their roll."""
        for item_type, chance in settings.item_chances.items():
            if self._rng.randint(1, 100) <= chance:
                square.add_item(self._create_item(item_type, settings))

    def _create_item(self, item_type: ItemType, settings: DifficultySettings) -> Item:
        """Make one item of the given type, including the repeating roll."""
        if item_type == ItemType.TRADER:
            # Traders always repeat. The player can't tell the types apart.
            return self._rng.choice(TRADER_TYPES)()

        repeating = self._rng.randint(1, 100) <= settings.repeat_chances[item_type]
        low, high = BONUS_AMOUNT_RANGES[item_type]
        amount = self._rng.randint(low, high)

        bonus_classes = {
            ItemType.FOOD: FoodBonus,
            ItemType.WATER: WaterBonus,
            ItemType.GOLD: GoldBonus,
        }
        return bonus_classes[item_type](amount, repeating)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def render(self, player_position: Optional[tuple[int, int]] = None) -> str:
        """Return a text picture of the map for the console.

        Each square shows its terrain letter. If the square has items, the
        letter is followed by a marker: f = food, w = water, g = gold,
        t = trader, + = more than one item. The player is shown as @.
        """
        lines = []
        for row in self._squares:
            cells = []
            for square in row:
                if player_position == (square.x, square.y):
                    cells.append("@ ")
                else:
                    cells.append(square.terrain.symbol + self._item_marker(square))
            lines.append(" ".join(cells))
        lines.append("")
        lines.append("Terrain: . Plains  F Forest  S Swamp  D Desert  M Mountain")
        lines.append("Items:   f food  w water  g gold  t trader  + several  @ player")
        return "\n".join(lines)

    @staticmethod
    def _item_marker(square: Square) -> str:
        """Return the one-character item marker for a square."""
        if not square.items:
            return " "
        if len(square.items) > 1:
            return "+"
        markers = {"FoodBonus": "f", "WaterBonus": "w", "GoldBonus": "g"}
        return markers.get(type(square.items[0]).__name__, "t")
