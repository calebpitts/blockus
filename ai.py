# {key - piece name: val - associated piece points}
GAME_PIECE_VALUES = {"monomino1": 1, "domino1": 2,
                     "trominoe1": 3, "trominoe2": 3,
                     "tetrominoes1": 4, "tetrominoes2": 4,
                     "tetrominoes3": 4, "tetrominoes4": 4,
                     "tetrominoes5": 4,
                     "pentominoe1": 5, "pentominoe2": 5,
                     "pentominoe3": 5, "pentominoe4": 5,
                     "pentominoe5": 5, "pentominoe6": 5,
                     "pentominoe7": 5, "pentominoe8": 5,
                     "pentominoe9": 5, "pentominoe10": 5,
                     "pentominoe11": 5, "pentominoe12": 5}


class AI:
    def __init__(self, board_state, color):
        self.board_state = board_state
        self.player_color = color
        self.player_score = 0
        self.current_pieces = list(GAME_PIECE_VALUES.keys())  # Gives all piece names to player when game starts

    def collect_moves(self, round_count):
        return self.board_state.get_all_valid_moves(round_count, self.player_color, self.current_pieces)

    def request_move(self):
        pass

    def update_player(self, piece_type):
        ''' Removes piece from the player's inventory and updates score
        '''
        self.current_pieces.remove(piece_type)  # Remove played piece from player's inventory

        if len(self.current_pieces) == 0 and piece_type == "monomino1":  # Additional 20 points if last piece played is a monomino
            self.player_score += 20
        elif len(self.current_pieces) == 0 and piece_type != "monomino1":  # Additional 15 points if all pieces have been played
            self.player_score += 15

        self.player_score += GAME_PIECE_VALUES[piece_type]  # Continue assignment of corresponding points for played piece regardless of the additional points cases
