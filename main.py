import board
import player
import math
import itertools


def welcome():
    print("                    =======================")
    print("                    = Welcome to Blockus! =")
    print("                    =======================")


def initialize_players(current_board):
    red = player.Player(current_board, "R ")
    blue = player.Player(current_board, "B ")
    green = player.Player(current_board, "G ")
    yellow = player.Player(current_board, "Y ")
    all_players = [red, blue, green, yellow]

    return all_players


def main():
    welcome()
    current_board = board.Board()
    all_players = initialize_players(current_board)

    end_game = False
    round_count = 0

    # Continously loops though game and each player's turn until end game
    for current_player in itertools.cycle(all_players):
        current_board.display_board(current_player, all_players, round_count)
        # EXAMPLE: myboard.update_board("R ", (4, 4), "pentominoe6", "north")
        color, index, piece_type, orientation = current_player.prompt(round_count)
        current_board.update_board(color, index, piece_type, orientation)

        if current_player.player_color == "Y ":  # Increment round count each time last player's turn is done.
            round_count += 1

        if end_game:
            break

    # current_board.display_endgame_results(players, round_count)
    print("Goodbye!")


if __name__ == "__main__":
    main()
