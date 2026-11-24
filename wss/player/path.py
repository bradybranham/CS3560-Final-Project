"""A planned sequence of moves and its total resource costs."""

from __future__ import annotations

from dataclasses import dataclass, field

from wss.player.move import Move


@dataclass
class Path:
    """Moves that lead to a target, with the costs of entering its squares."""

    moves: list[Move] = field(default_factory=list)
    movement_cost: int = 0
    water_cost: int = 0
    food_cost: int = 0

    @property
    def total_cost(self) -> tuple[int, int, int]:
        """Return costs as (movement, water, food)."""
        return self.movement_cost, self.water_cost, self.food_cost

    @property
    def total_movement_cost(self) -> int:
        """Compatibility-friendly name for the movement cost."""
        return self.movement_cost

    def add(self, move: Move, movement: int, water: int, food: int) -> None:
        """Append one move and add the costs of its destination square."""
        self.moves.append(move)
        self.movement_cost += movement
        self.water_cost += water
        self.food_cost += food
