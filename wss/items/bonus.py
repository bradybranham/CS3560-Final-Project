"""Food, water, and gold bonuses.

PLACEHOLDER: minimal version so map generation can run. The teammate who
owns items should finish interact() and apply_to().
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from wss.items.item import Item

if TYPE_CHECKING:
    from wss.player.player import Player


class Bonus(Item):
    """An item that adds some amount of a resource to the player.

    Attributes:
        amount: How much of the resource the bonus gives.
    """

    def __init__(self, amount: int, repeating: bool) -> None:
        super().__init__(repeating)
        self.amount = amount

    def interact(self, player: Player, turn: int) -> bool:
        # TODO (items teammate): check is_available, call apply_to,
        # update last_collected_turn, and handle removal of one-time bonuses.
        raise NotImplementedError

    @abstractmethod
    def apply_to(self, player: Player) -> None:
        """Add this bonus's resource to the player."""


class FoodBonus(Bonus):
    """Extra food for the player."""

    def apply_to(self, player: Player) -> None:
        raise NotImplementedError  # TODO (items teammate)


class WaterBonus(Bonus):
    """Extra water for the player, such as a stream."""

    def apply_to(self, player: Player) -> None:
        raise NotImplementedError  # TODO (items teammate)


class GoldBonus(Bonus):
    """Gold coins for the player."""

    def apply_to(self, player: Player) -> None:
        raise NotImplementedError  # TODO (items teammate)
