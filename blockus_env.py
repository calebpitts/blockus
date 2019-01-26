from spacetimerl.turn_based_environment import TurnBasedEnvironment
from board import Board
from ai import AI
from typing import Tuple, List, Union
import numpy as np
from copy import deepcopy

PLAYER_TO_COLOR = {
    0: 'R ',
    1: 'B ',
    2: 'G ',
    3: 'Y '
}

COLOR_TO_PLAYER = {
    'R ': 0,
    'B ': 1,
    'G ': 2,
    'Y ': 3
}


def action_to_string(piece_type, index, orientation):
    return "{};{};{}".format(piece_type, index, orientation)


def string_to_action(action_str: str):

    piece_type, index, orientation = action_str.split(";")
    index = tuple(map(int, index.replace('(', '').replace(')', '').split(',')))
    return piece_type, index, orientation


class BlockusEnv(TurnBasedEnvironment):

    @property
    def min_players(self) -> int:
        """ Property holding the number of players present required to play game. """
        return 4

    @property
    def max_players(self) -> int:
        """ Property holding the max number of players present for a game. """
        return 4

    @property
    def observation_shape(self) -> tuple:
        """ Property holding the numpy shape of a transformed observation state. """
        raise (20, 20)

    def new_state(self, num_players: int = 4) -> Tuple[Board, int, List[AI]]:
        """ Create a fresh state. This could return a fixed object or randomly initialized on, depending on the game.

        Returns
        -------
        new_state : np.ndarray
            A state for the new game.
        new_players: [int]
            List of players whos turn it is now.
        """
        board = Board()
        red = AI(board, "R ")
        blue = AI(board, "B ")
        green = AI(board, "G ")
        yellow = AI(board, "Y ")

        return board, 0, [red, blue, green, yellow]

    def next_state(self, state: Tuple[Board, int, List[AI]], player: int, action: str) \
            -> Tuple[Tuple[Board, int, List[AI]], float, bool, Union[List[int], None]]:

        board, round_count, players = state
        players = deepcopy(players)
        new_board = Board(board)

        color = PLAYER_TO_COLOR[player]
        piece_type, index, orientation = string_to_action(action)

        current_player = players[player]

        if len(action) > 0:
            new_board.update_board(color, piece_type, index, orientation, round_count, True)
            current_player.update_player(piece_type)

        if not any(p.check_moves(round_count) for p in players):
            terminal = True
            max_score = 0
            scores = []
            winners = []

            for p in players:
                scores.append((p.player_color, p.player_score))
                if p.player_score > max_score:
                    max_score = p.player_score

            for player_color, score in scores:
                if score == max_score:  # Prints all scores equal to the max score (accounts for ties)
                    winners.append(COLOR_TO_PLAYER[player_color])

            sorted_scores = sorted(scores, key=lambda x: x[1])
            reward = sorted_scores.index((current_player.player_color, current_player.player_score))
        else:
            winners = None
            reward = 0
            terminal = False

        if player == 3:
            round_count += 1

        return (new_board, round_count, players), reward, terminal, winners

    def valid_actions(self, state: object, player: int) -> [str]:
        """ Valid actions for a specific state. """
        return NotImplementedError

    def is_valid_action(self, state: object, player: int, action: str) -> bool:
        """ Valid actions for a specific state. """

        if len(action) == 0:
            return False

        board, round_count, players = state
        piece_type, index, orientation = string_to_action(action)
        current_player = players[player]
        all_valid_moves = current_player.collect_moves(round_count)

        is_valid_move = False
        try:
            # print(all_valid_moves[piece_type][index])
            if orientation in all_valid_moves[piece_type][index]:
                is_valid_move = True
        except KeyError:
            pass

        return is_valid_move

    def state_to_observation(self, state: Tuple[Board, int, List[AI]], player: int) -> np.ndarray:
        """ Convert the raw game state to the observation for the agent.
        The observation must be able to be fed into your predictor.

        This can return different values for the different players. Default implementation is just the identity."""
        board, round_count, players = state
        return np.asarray(board.board_contents)
