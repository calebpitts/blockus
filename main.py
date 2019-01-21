import board
import player
import ai
import itertools
import random


def welcome():
    ''' Displays welcome message to console
    '''
    print("                =======================")
    print("                = Welcome to Blockus! =")
    print("                =======================")
    print()


def initialize_human_players(current_board):
    red = player.Player(current_board, "R ")
    blue = player.Player(current_board, "B ")
    green = player.Player(current_board, "G ")
    yellow = player.Player(current_board, "Y ")
    all_players = [red, blue, green, yellow]

    return all_players


def initialize_ai_players(current_board):
    red = ai.AI(current_board, "R ")
    blue = ai.AI(current_board, "B ")
    green = ai.AI(current_board, "G ")
    yellow = ai.AI(current_board, "Y ")
    all_players = [red, blue, green, yellow]

    return all_players


def display_endgame_results(all_players, round_count):
    ''' Displays final round number and final scores for each player
    '''
    print("\n===================")
    print("ENDGAME STATISTICS:")
    print("===================")
    print("ROUNDS:", round_count, "\n")
    max_score = 0
    winner = "NONE"
    for current_player in all_players:
        print(current_player.player_color, ": ", current_player.player_score, sep="")
        if current_player.player_score > max_score:
            winner = current_player.player_color
    print("WINNER:", winner)


def human_game(current_board, all_players):
    ''' Continously loops though game and each player's turn until end game
    '''
    round_count = 0
    players_with_no_moves = 0

    for current_player in itertools.cycle(all_players):
        moves_present = current_player.check_moves(round_count)  # Checks if player can make any moves

        if moves_present:  # If current player can make at least one move..
            current_board.display_board(current_player, all_players, round_count)
            color, piece_type, index, orientation = current_player.prompt_turn()
            current_board.update_board(color, piece_type, index, orientation)
        else:
            players_with_no_moves += 1

        if current_player.player_color == "Y ":  # Increment round count each time last player's turn is done.
            round_count += 1

        if players_with_no_moves == 4:  # If 4 players with no moves, end game
            break

    display_endgame_results(all_players, round_count)


def ai_game(current_board, all_players):
    ''' Runs an AI game that collects all available moves then requests one move to play until all AI instances
        can't make any more moves at which point the game is over.
    '''
    round_count = 0
    players_with_no_moves = 0

    for current_player in itertools.cycle(all_players):
        all_valid_moves = current_player.collect_moves(round_count)

        if len(list(all_valid_moves.keys())) > 0:  # If no valid moves available for this player.
            current_board.display_board(current_player, all_players, round_count)

            # Get all valid moves and ai decides on which one to make
            random_indexes = random.sample(all_valid_moves.items(), 1)
            piece_type = random_indexes[0][0]
            index = list(all_valid_moves[piece_type].keys())[0]
            orientation = all_valid_moves[piece_type][index][0]

            # ai chooses move
            current_board.update_board(current_player.player_color, piece_type, index, orientation)
            current_player.update_player(piece_type)  # Updates ai
        else:
            players_with_no_moves += 1

        if current_player.player_color == "Y ":  # Increment round count each time last player's turn is done.
            round_count += 1

        if players_with_no_moves == 4:  # If 4 players with no moves, end game
            break

    display_endgame_results(all_players, round_count)


def main():
    welcome()

    while True:
        current_board = board.Board()  # New board every loop

        game_type = input("Would you like to run a human or ai game? [human/ai]: ").upper().strip()
        if game_type == "HUMAN":
            all_players = initialize_human_players(current_board)
            human_game(current_board, all_players)
        elif game_type == "AI":
            all_players = initialize_ai_players(current_board)
            ai_game(current_board, all_players)
        else:
            print("You selected an invalid game type. Please try again.")

        quit = input("Would you like to quit or restart? [quit]/restart: ").upper().strip()
        if quit == "QUIT":
            break

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
