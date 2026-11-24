"""The player's survival resources and movement rules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wss.player.move import Move

if TYPE_CHECKING:
    from wss.items.item import Item
    from wss.world.game_map import Map


class Player:
    """A player who spends strength, water, and food to cross the map.

    The current values are intentionally public: Brain and Vision can inspect
    them without needing special accessors. Mutating methods clamp values so
    resources never become negative or exceed their maximum.
    """

    def __init__(
        self,
        game_map: Map,
        position: tuple[int, int] = (0, 0),
        max_strength: int = 10,
        max_water: int = 10,
        max_food: int = 10,
    ) -> None:
        if not game_map.in_bounds(*position):
            raise ValueError("Player position must be on the map.")
        if min(max_strength, max_water, max_food) < 0:
            raise ValueError("Maximum resources cannot be negative.")

        self.game_map = game_map
        self.position = position
        self.max_strength = max_strength
        self.max_water = max_water
        self.max_food = max_food
        self.strength = max_strength
        self.water = max_water
        self.food = max_food
        self.gold = 0
        self.turn = 0

    # Common aliases make the class easier to use from Brain/Vision code.
    @property
    def current_strength(self) -> int:
        return self.strength

    @property
    def current_water(self) -> int:
        return self.water

    @property
    def current_food(self) -> int:
        return self.food

    def can_afford(self, square_or_move: object) -> bool:
        """Return whether the player can enter a square or make a move."""
        square = square_or_move
        if isinstance(square_or_move, Move):
            x, y = self.position
            square = self.game_map.get_square(x + square_or_move.dx, y + square_or_move.dy)
        if square is None or not hasattr(square, "terrain"):
            return False
        terrain = square.terrain
        return (
            self.strength >= terrain.movement_cost
            and self.water >= terrain.water_cost
            and self.food >= terrain.food_cost
        )

    def move(self, move: Move, turn: int | None = None) -> bool:
        """Enter an adjacent square, paying its terrain costs.

        After a successful move, all available items on the destination square
        are collected automatically. Returns False when the move is invalid or
        unaffordable.
        """
        collection_turn = self.turn if turn is None else turn
        destination = self.game_map.get_square(
            self.position[0] + move.dx, self.position[1] + move.dy
        )
        if not self.can_afford(destination):
            return False

        terrain = destination.terrain
        self.strength -= terrain.movement_cost
        self.water -= terrain.water_cost
        self.food -= terrain.food_cost
        self.position = (destination.x, destination.y)
        self.collect(destination.items, collection_turn)
        if turn is None:
            self.turn += 1
        return True

    def rest(self) -> None:
        """Recover 2 strength while spending half of current water and food."""
        self.strength = min(self.max_strength, self.strength + 2)
        self.water //= 2
        self.food //= 2

    def collect(self, items: list[Item], turn: int | None = None) -> int:
        """Collect all usable items and return the number collected."""
        if turn is None:
            turn = self.turn
        collected = 0
        for item in list(items):
            if item.interact(self, turn):
                collected += 1
        return collected

    def add_strength(self, amount: int) -> None:
        self.strength = max(0, min(self.max_strength, self.strength + amount))

    def add_water(self, amount: int) -> None:
        self.water = max(0, min(self.max_water, self.water + amount))

    def add_food(self, amount: int) -> None:
        self.food = max(0, min(self.max_food, self.food + amount))

    def add_gold(self, amount: int) -> None:
        self.gold = max(0, self.gold + amount)

    def has_crossed(self) -> bool:
        """Return True when the player reaches the east edge."""
        return self.position[0] == self.game_map.width - 1

    def is_stuck(self) -> bool:
        """Return True when no adjacent square is affordable."""
        return not any(self.can_afford(move) for move in Move)
