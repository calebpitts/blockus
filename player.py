# {key - piece name: val - associated points}
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

# ADD LATER
# Bonus +15 points if all pieces played
# Bonus +20 points if last piece played is monomino


class Player:
    def __init__(self, board_state, color):
        self.board_state = board_state
        self.player_color = color
        self.player_score = 0
        self.current_pieces = list(GAME_PIECE_VALUES.keys())  # Gives all piece names to player when game starts

    def prompt_turn(self, round_count):
        ''' Asks for the type of piece, where to place that piece (index),
            and what orientation they want that piece in. Returns requested
            update to the board only if all info is valid.
        '''
        # if round_count == 0:  # If first round, players must place pieces on corners only.
        #    all_valid_moves = self.board_state.get_initial_valid_moves(self.player_color, self.current_pieces)  # Gets all initial valid moves where only the corners can be played
        # else:
        all_valid_moves = self.board_state.get_all_valid_moves(self.player_color, self.current_pieces)  # Gets master dict of all valid moves including orientations for the current player's color {(x,y):['orientations']}

        ################################################################
        print("VALID MOVES w/ ORIENTATIONS:\n", all_valid_moves, sep="")
        ################################################################

        piece_type = self.prompt_type(all_valid_moves)
        index = self.prompt_index(all_valid_moves, piece_type)
        orientation = self.prompt_orientation(all_valid_moves, piece_type, index)
        self.update_player(piece_type)

        return self.player_color, piece_type, index, orientation

    def prompt_type(self, all_valid_moves):
        ''' Asks user for desired piece type. Loops until valid piece type specified.
        '''
        valid_piece_types = self.board_state.fetch_valid_piece_types(all_valid_moves)

        while True:
            piece_type = input("\nWhat piece type would you like to place? (enter name of piece or 'SHOW' to show your available pieces): ").upper().strip()
            print()
            if piece_type == "SHOW":
                for piece in valid_piece_types:
                    self.board_state.display_piece(piece, self.player_color)  # Displays all the pieces the current player has to console
            elif piece_type.lower() in valid_piece_types:
                return piece_type.lower()
            else:
                print("You selected an invalid piece or piece you don't have! Try again.")

    def prompt_index(self, all_valid_moves, piece_type):
        ''' Asks user for desired index of their piece type. Loops until valid index specified.
        '''
        valid_indexes = self.board_state.fetch_valid_indexes(all_valid_moves, piece_type)

        while True:
            print("\nCurrent available indexes to choose from with your selected piece: ")
            for index in valid_indexes:
                print("(", index[0] + 1, ", ", index[1] + 1, ")  ", sep="", end="")  # Add 1 to exclude 0 index

            print("\nWhere would you like to place your piece?")
            try:
                x = int(input("X Coordinate: ")) - 1  # Subtracting by one because of index 0
                y = int(input("Y Coordinate: ")) - 1

                if (x, y) in valid_indexes:  # Valid indexes holds the raw valid index accounting for zero
                    return (x, y)
            except ValueError:
                pass
            print("You selected an invalid coordinate. Try again.")

    def prompt_orientation(self, all_valid_moves, piece_type, index):
        ''' Asks user for desired orientation of their piece type and index. Loops until valid orientation specified.
        '''
        valid_orientations = self.board_state.fetch_valid_orientations(all_valid_moves, piece_type, index)

        while True:
            see_orientations = input("Would you like to see the list of valid orientations you can make? Y/[N]: ").upper()
            if see_orientations == "Y":
                self.board_state.display_possible_orientations(piece_type, self.player_color, valid_orientations)

            user_orientation = input("Which orientation do you want your piece? ").lower().strip()
            if user_orientation in valid_orientations:
                return user_orientation
            else:
                print("You specified an erronous or invalid orientation. Try again.")

    def update_player(self, piece_type):
        ''' Removes piece from the player's inventory and updates score
        '''
        self.current_pieces.remove(piece_type)
        self.update_score(piece_type)

    def update_score(self, piece_type):
        ''' Updates overall player score by amount the piece type is worth
        '''
        self.player_score += GAME_PIECE_VALUES[piece_type]

    def get_score(self):
        ''' Returns the current player's score
        '''
        return self.player_score
