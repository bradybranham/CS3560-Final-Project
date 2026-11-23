"""Terrain types for the WSS map.

Every square on the map has exactly one terrain. Each terrain has three
costs that the player pays when ENTERING a square of that terrain:
movement (strength), water, and food.

Cost reasoning:
    Plains   - open, easy ground. Cheapest in every way.
    Forest   - slower going through trees, but shade keeps water cost low.
    Swamp    - very slow, and wading is tiring, so food cost is high.
    Desert   - moderate to walk, but the heat makes water very expensive.
    Mountain - the hardest climb; costs the most strength.
"""

from __future__ import annotations

from abc import ABC


class Terrain(ABC):
    """Abstract base class for all terrain types.

    Subclasses only need to pass their costs, name, and map symbol to
    this constructor. Terrain is abstract because a square should always
    hold a specific kind of terrain, never a generic one.
    """

    def __init__(self, name: str, symbol: str,
                 movement_cost: int, water_cost: int, food_cost: int) -> None:
        self.name = name
        self.symbol = symbol  # Single character used when printing the map
        self.movement_cost = movement_cost
        self.water_cost = water_cost
        self.food_cost = food_cost

    def __repr__(self) -> str:
        return (f"{self.name}(move={self.movement_cost}, "
                f"water={self.water_cost}, food={self.food_cost})")


class Plains(Terrain):
    """Open grassland: the cheapest terrain to cross."""

    def __init__(self) -> None:
        super().__init__("Plains", ".", movement_cost=1, water_cost=1, food_cost=1)


class Forest(Terrain):
    """Wooded area: slower to move through, but shaded."""

    def __init__(self) -> None:
        super().__init__("Forest", "F", movement_cost=2, water_cost=1, food_cost=1)


class Swamp(Terrain):
    """Wet, muddy ground: slow and tiring."""

    def __init__(self) -> None:
        super().__init__("Swamp", "S", movement_cost=3, water_cost=1, food_cost=2)


class Desert(Terrain):
    """Hot, dry sand: water is the main cost."""

    def __init__(self) -> None:
        super().__init__("Desert", "D", movement_cost=2, water_cost=3, food_cost=1)


class Mountain(Terrain):
    """Steep, rocky ground: the most strength to cross."""

    def __init__(self) -> None:
        super().__init__("Mountain", "M", movement_cost=4, water_cost=2, food_cost=2)
