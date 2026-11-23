"""A single square (cell) on the WSS map."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Imported only for type hints, to avoid circular imports
    from wss.items.item import Item
    from wss.world.terrain import Terrain


class Square:
    """One square of the map, about 5 miles on a side.

    Coordinates: x is the column (0 = west edge), and y is the row
    (0 = north edge).

    Attributes:
        x: Column index.
        y: Row index.
        terrain: The terrain that sets this square's entry costs.
        items: Items currently in this square (often empty).
    """

    def __init__(self, x: int, y: int, terrain: Terrain) -> None:
        self.x = x
        self.y = y
        self.terrain = terrain
        self.items: list[Item] = []

    def add_item(self, item: Item) -> None:
        """Place an item in this square."""
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        """Remove an item, such as a one-time bonus after it is collected."""
        if item in self.items:
            self.items.remove(item)

    def has_item_of_type(self, item_class: type) -> bool:
        """Return True if this square holds an item of the given class.

        Vision can use this, for example: square.has_item_of_type(FoodBonus).
        """
        return any(isinstance(item, item_class) for item in self.items)

    def __repr__(self) -> str:
        return f"Square({self.x}, {self.y}, {self.terrain.name}, items={len(self.items)})"
