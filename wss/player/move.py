"""Directions the player can move on the map."""

from enum import Enum


class Move(Enum):
    """One cardinal movement from the current square."""

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    @property
    def dx(self) -> int:
        """Horizontal coordinate change."""
        return self.value[0]

    @property
    def dy(self) -> int:
        """Vertical coordinate change."""
        return self.value[1]