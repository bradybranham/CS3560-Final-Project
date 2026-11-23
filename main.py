from wss.game import Game
from wss.world.difficulty import Difficulty

# Limits on map size so the map stays playable and fits on screen.
MIN_WIDTH, MAX_WIDTH = 5, 50
MIN_HEIGHT, MAX_HEIGHT = 3, 30


def prompt_int(message: str, low: int, high: int) -> int:
    """Ask the user for a whole number between low and high, inclusive.

    Keeps asking until the user enters a valid number.
    """
    while True:
        answer = input(f"{message} ({low}-{high}): ").strip()
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)
        print(f"  Please enter a whole number from {low} to {high}.")


def prompt_difficulty() -> Difficulty:
    """Ask the user to choose a difficulty from a numbered menu."""
    options = list(Difficulty)
    print("Choose a difficulty:")
    for number, difficulty in enumerate(options, start=1):
        print(f"  {number}. {difficulty.value.capitalize()}")
    choice = prompt_int("Difficulty", 1, len(options))
    return options[choice - 1]


def main() -> None:
    """Ask for the map settings, build the game, and show the map."""
    print("=== Wilderness Survival System ===\n")
    width = prompt_int("Map width", MIN_WIDTH, MAX_WIDTH)
    height = prompt_int("Map height", MIN_HEIGHT, MAX_HEIGHT)
    difficulty = prompt_difficulty()

    game = Game()
    game.setup(width, height, difficulty)

    print(f"\n{width} x {height} map, {difficulty.value} difficulty:\n")
    print(game.game_map.render(player_position=game.start_position))

    # TODO: game.start() once Player, Vision, and Brain are ready.


if __name__ == "__main__":
    main()
