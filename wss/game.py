"""The Game class: owns the map and player, and runs the turns."""

from __future__ import annotations

import random
from typing import Optional

from wss.world.difficulty import Difficulty
from wss.world.game_map import Map


class Game:
    """Top-level controller for one run of WSS.

    Attributes:
        turn_number: How many turns have passed (starts at 0).
        game_map: The generated map.
        start_position: (x, y) where the player begins, on the west edge.
    """

    def __init__(self, rng: Optional[random.Random] = None) -> None:
        self.turn_number = 0
        self.game_map = Map(rng)
        self.start_position: tuple[int, int] = (0, 0)
        # TODO (player teammate): self.player = None

    def setup(self, width: int, height: int, difficulty: Difficulty) -> None:
        """Generate the map and choose the player's starting square.

        The last step of the activity diagram: place the player in a random
        row on the west edge (x = 0).
        """
        self.game_map.generate(width, height, difficulty)
        self.start_position = (0, self.game_map.random_start_row())
        # TODO (player teammate): create the Player here with its Vision
        # and Brain, and place it at self.start_position.

    def start(self) -> None:
        """Run turns until the game is finished."""
        raise NotImplementedError  # TODO: loop run_turn() until is_finished()

    def run_turn(self) -> None:
        """Advance the game by one turn."""
        raise NotImplementedError  # TODO: brain.make_move(), then turn_number += 1

    def is_finished(self) -> bool:
        """Return True when the player has crossed the map or is stuck."""
        raise NotImplementedError  # TODO: player.has_crossed() or player.is_stuck()
