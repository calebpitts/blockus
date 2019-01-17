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
ORIENTATIONS = ["north", "northwest", "south", "southeast", "west", "southwest", "northeast", "east"]
# Bonus +15 points if all pieces played
# Bonus +20 points if last piece played is monomino


class Player:
    def __init__(self, board_state, color):
        self.board_state = board_state
        self.player_color = color
        self.player_score = 0
        self.current_pieces = list(GAME_PIECE_VALUES.keys())  # Gives all piece names to player when game starts

    def get_pieces(self):
        return self.current_pieces

    def get_color(self):
        return self.color

    def prompt(self):
        ''' Asks for the type of piece, where to place that piece (index),
            and what orientation they want that piece in. Returns requested
            update to the board only if all info is valid.
        '''
        piece_type = self.prompt_type()
        index = self.prompt_index(piece_type)
        orientation = self.prompt_orientation(piece_type)

        if self.check_validity(piece_type, index, orientation):
            self.current_pieces.remove(piece_type)  # Removes chosen piece from the player's current available pieces
            self.update_score(piece_type)
            return self.player_color, index, piece_type, orientation

    def prompt_type(self):
        while True:
            piece_type = input("\nWhat piece type you like to place? (enter name of piece or 'SHOW' to show available pieces): ").upper().strip()
            print()
            if piece_type == "SHOW":
                for piece in self.current_pieces:
                    self.board_state.display_piece(piece, self.player_color)  # Displays all the pieces the current player has to console
            elif piece_type.lower() in self.current_pieces:
                return piece_type.lower()
            else:
                print("You selected an invalid piece or piece you don't have! Try again.")

    def prompt_index(self, piece_type):
        while True:
            valid_moves = self.board_state.get_valid_moves(piece_type, self.player_color)
            print("\nCurrent available indexes to choose from with your selected piece: ")
            for count, point in enumerate(valid_moves):
                if count % 7 == 0:
                    print("")
                print("(", point[0], ",", point[1], ")  ", sep="", end="")

            print("\nWhere would you like to place your piece?")
            x = int(input("X Coordinate: ")) - 1  # Subtracting by one because of index 0
            y = int(input("Y Coordinate: ")) - 1

            if (x, y) in valid_moves:
                return (x, y)
            else:
                print("You selected an invalid coordinate. Try again.")

    def prompt_orientation(self, piece_type):
        while True:
            see_orientations = input("Would you like to see the list of valid orientations you can make? Y/[N]: ").upper()
            if see_orientations == "Y":
                self.board_state.display_possible_orientations(piece_type, self.player_color)
            orientation = input("Which orientation do you want your piece? ")

            if orientation in ORIENTATIONS:
                return orientation
            else:
                print("You specified an erronous or invalid orientation. Try again.")

    def check_validity(self, piece_type, index, orientation):
        ''' Checks if requested piece placement is a valid placement on the board.
        '''
        return True

    def update_score(self, piece_type):
        ''' Updates overall player score by amount the piece type is worth
        '''
        self.player_score += GAME_PIECE_VALUES[piece_type]

    # check_validity (parameter: current state of the board and piece you want to place and where)
    # - gather list of valid moves
    # - check if provided piece placement in valid list
    # - if in list, go to next step, otherwise prompt user again

    # return valid coords to main, to be used to place on board

    # record score for this player
