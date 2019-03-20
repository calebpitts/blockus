from spacetimerl.turn_based_environment import turn_based_environment, TurnBasedEnvironment
from spacetimerl.client_environment import ClientEnv
from blockus.board import Board, PIECE_TYPES
from blockus.ai import AI
from blockus import gui
from typing import Tuple, List, Union, Dict
import numpy as np
from copy import deepcopy
import dill
import random

PLAYER_TO_COLOR = {
    0: 1,
    1: 2,
    2: 3,
    3: 4
}

COLOR_TO_PLAYER = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    0: -1
}

PIECE_NAME_TO_INDEX = {piece_name: i for i, piece_name in enumerate(PIECE_TYPES.keys())}


def relative_player_id(current_player: int, absolute_player_num) -> int:
    if absolute_player_num < 0:
        return absolute_player_num

    return (absolute_player_num - current_player) % 4


def action_to_string(piece_type, index, orientation):
    return "{};{};{}".format(piece_type, index, orientation)


def string_to_action(action_str: str):

    piece_type, index, orientation = action_str.split(";")
    index = tuple(map(int, index.replace('(', '').replace(')', '').split(',')))
    return piece_type, index, orientation


def start_gui():
    gui.start_gui()


def terminate_gui():
    gui.terminate_gui()


class BlockusClientEnv(ClientEnv):

    def __init__(self, *args, **kwargs):
        self._gui_is_active = False
        super().__init__(*args, **kwargs)

    def __del__(self):
        if self._gui_is_active:
            terminate_gui()

    @staticmethod
    def _display_board(state: Tuple[int, Tuple[Board, int, List[AI]]], player_num: int, winners: List[int]):
        _, inner_state = state
        board, round_count, players = inner_state
        current_player = players[player_num]
        gui.display_board(board_contents=board.board_contents, current_player=current_player, players=players,
                          round_count=round_count, winners=winners)

    def render(self, state: Tuple[int, Tuple[Board, int, List[AI]]], player_num: int, winners: List[int]):
        if not self._gui_is_active:
            start_gui()
            self._display_board(state, player_num, winners)
        self._display_board(state, player_num, winners)

    @staticmethod
    def random_valid_action_string(state: Tuple[int, Tuple[Board, int, List[AI]]], player_num: int) -> str:
        _, inner_state = state
        board, round_count, players = inner_state
        player = players[player_num]

        all_valid_moves = player.collect_moves(board, round_count)
        print("All possible moves for you: {}".format(all_valid_moves))
        # input('press enter to play random move:')

        if len(all_valid_moves.keys()) != 0:
            random_indexes = random.sample(all_valid_moves.items(), 1)
            piece_type = random_indexes[0][0]
            index = list(all_valid_moves[piece_type].keys())[0]
            orientation = all_valid_moves[piece_type][index][0]

            string_action = action_to_string(piece_type, index, orientation)
        else:
            string_action = ""

        return string_action



@turn_based_environment
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

        return {"board": (20, 20), "pieces": (4, 21), "score": (4,), "player": (1,)}

    @staticmethod
    def observation_names():
        return ["board", "pieces", "score", "player"]

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
        red = AI(board, 1)
        blue = AI(board, 2)
        green = AI(board, 3)
        yellow = AI(board, 4)

        return board, 0, [red, blue, green, yellow]

    # Serialization Methods
    @staticmethod
    def serializable() -> bool:
        return True

    @staticmethod
    def serialize_state(state: object) -> bytes:
        return dill.dumps(state)

    @staticmethod
    def deserialize_state(serialized_state: bytes) -> object:
        # print("serialize state:\n{}".format(serialized_state))
        # exit()
        return dill.loads(serialized_state)

    def next_state(self, state: Tuple[Board, int, List[AI]], player_num: int, action: str) \
            -> Tuple[Tuple[Board, int, List[AI]], float, bool, Union[List[int], None]]:

        board, round_count, players = state

        players = deepcopy(players)
        new_board = Board(board)

        color = PLAYER_TO_COLOR[player_num]

        current_player = players[player_num]

        if len(action) > 0:
            piece_type, index, orientation = string_to_action(action)
            new_board.update_board(color, piece_type, index, orientation, round_count, True)
            current_player.update_player(piece_type)

        if not any(p.check_moves(board, round_count) for p in players):
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

        if player_num == 3:
            round_count += 1

        return (new_board, round_count, players), reward, terminal, winners

    def valid_actions(self, state: Tuple[Board, int, List[AI]], player: int) -> [str]:
        """ Valid actions for a specific state. """
        raise NotImplementedError

    def is_valid_action(self, state: Tuple[Board, int, List[AI]], player_num: int, action: str) -> bool:
        """ Valid actions for a specific state. """

        if len(action) == 0:
            return False

        board, round_count, players = state
        piece_type, index, orientation = string_to_action(action)
        current_player = players[player_num]
        all_valid_moves = current_player.collect_moves(board, round_count)

        is_valid_move = False
        try:
            # print(all_valid_moves[piece_type][index])
            if orientation in all_valid_moves[piece_type][index]:
                is_valid_move = True
        except KeyError:
            pass

        return is_valid_move

    def state_to_observation(self, state: Tuple[Board, int, List[AI]], player: int) -> Dict[str, np.ndarray]:
        """ Convert the raw game state to the observation for the agent.
        The observation must be able to be fed into your predictor.
        This can return different values for the different players. Default implementation is just the identity."""

        pieces = np.zeros((4, 21), dtype=np.uint8)
        board, round_count, players = state
        board = [[relative_player_id(player, COLOR_TO_PLAYER[pos]) for pos in row] for row in board.board_contents]
        board = np.asarray(board)

        for p in players:

            color = p.player_color
            rel_player_id = relative_player_id(current_player=player,
                                               absolute_player_num=COLOR_TO_PLAYER[color])

            for piece in p.current_pieces:
                pieces[rel_player_id, PIECE_NAME_TO_INDEX[piece]] = 1

        score = np.roll(np.array([p.player_score for p in players]), -player)

        return {'board': board, 'pieces': pieces, 'score': score, 'player': np.array([player])}
