"""Base class for anything that can sit in a map square.

PLACEHOLDER: minimal version so map generation can run. The teammate who
owns items should fill in interact() behavior in the subclasses.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wss.player.player import Player


class Item(ABC):
    """Something in a square that the player can interact with.

    Attributes:
        repeating: If True, the item can be used once per turn forever.
            If False, it is used once and then removed from the square.
        last_collected_turn: The turn it was last used (-1 means never).
    """

    def __init__(self, repeating: bool) -> None:
        self.repeating = repeating
        self.last_collected_turn = -1

    def is_available(self, turn: int) -> bool:
        """Return True if the item can be used on this turn."""
        if self.last_collected_turn == -1:
            return True
        return self.repeating and self.last_collected_turn < turn

    @abstractmethod
    def interact(self, player: Player, turn: int) -> bool:
        """Let the player use this item. Return True if something happened."""
