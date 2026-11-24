"""Food, water, and gold bonuses."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from wss.items.item import Item

if TYPE_CHECKING:
    from wss.player.player import Player


class Bonus(Item):
    """An item that adds a resource to the player."""

    def __init__(
        self,
        amount: int,
        repeating: bool,
        required_strength: int = 0,
        required_food: int = 0,
        required_water: int = 0,
    ) -> None:
        super().__init__(repeating)

        if min(
            amount,
            required_strength,
            required_food,
            required_water,
        ) < 0:
            raise ValueError("Bonus amounts and requirements cannot be negative.")

        self.amount = amount
        self.required_strength = required_strength
        self.required_food = required_food
        self.required_water = required_water

    def interact(self, player: Player, turn: int) -> bool:
        """Collect the bonus if it is available and requirements are met."""

        if not self.is_available(turn):
            return False

        if player.strength < self.required_strength:
            return False

        if player.food < self.required_food:
            return False

        if player.water < self.required_water:
            return False

        self.apply_to(player)
        self.last_collected_turn = turn

        if not self.repeating:
            square = player.game_map.get_square(*player.position)
            if square is not None:
                square.remove_item(self)

        return True

    @abstractmethod
    def apply_to(self, player: Player) -> None:
        """Apply the bonus to the player."""


class FoodBonus(Bonus):
    """Adds food to the player."""

    def apply_to(self, player: Player) -> None:
        player.add_food(self.amount)


class WaterBonus(Bonus):
    """Adds water to the player."""

    def apply_to(self, player: Player) -> None:
        player.add_water(self.amount)


class GoldBonus(Bonus):
    """Adds gold to the player."""

    def apply_to(self, player: Player) -> None:
        player.add_gold(self.amount)