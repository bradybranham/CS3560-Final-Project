"""Traders the player can barter with.

PLACEHOLDER: minimal version so map generation can run. The teammate who
owns traders should replace the method bodies with real negotiation logic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from wss.items.item import Item

if TYPE_CHECKING:
    from wss.player.player import Player


class Trader(Item):
    """A person in a square who trades gold, water, and food.

    Traders always repeat, so the player can trade with them every turn.
    """

    def __init__(self) -> None:
        super().__init__(repeating=True)

    def interact(self, player: Player, turn: int) -> bool:
        raise NotImplementedError  # TODO (traders teammate)


class PatientTrader(Trader):
    """Placeholder for the Patient trader type."""


class ImpatientTrader(Trader):
    """Placeholder for the Impatient trader type."""


class GreedyTrader(Trader):
    """Placeholder for the Greedy trader type."""


# The generator picks one of these at random for each trader it places.
TRADER_TYPES: list[type[Trader]] = [PatientTrader, ImpatientTrader, GreedyTrader]
