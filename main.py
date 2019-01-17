import board
import player
import math
import itertools


def welcome():
    print("                    =======================")
    print("                    = Welcome to Blockus! =")
    print("                    =======================")


def main():
    welcome()
    current_board = board.Board()
    red = player.Player(current_board, "R ")
    blue = player.Player(current_board, "B ")
    green = player.Player(current_board, "G ")
    yellow = player.Player(current_board, "Y ")

    end_game = False
    round_count = 0
    players = [red, blue, green, yellow]

    # Continously loops though game and each player's turn until end game
    for p in itertools.cycle(players):
        # myboard.update_board("R ", (4, 4), "pentominoe6", "north")
        current_board.display_board()
        print("\n======================================")
        print("ROUND:", str(round_count), "            CURRENT PLAYER:", p.player_color)
        print("======================================")
        print("SCORES:  R =", red.player_score, "| B =", blue.player_score, "| G =", green.player_score, "| Y =", yellow.player_score)
        color, index, piece_type, orientation = p.prompt()

        current_board.update_board(color, index, piece_type, orientation)
        # current_board.display_board()
        if p.player_color == "Y ":
            round_count += 1

        if end_game:
            break


if __name__ == "__main__":
    main()
