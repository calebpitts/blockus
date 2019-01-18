import math

# {key - piece name: val - offsets from index (assuming piece oriented east)}
PIECE_TYPES = {"monomino1": [(0, 0)],
               "domino1": [(0, 0), (1, 0)],
               "trominoe1": [(0, 0), (1, 0), (1, 1)],
               "trominoe2": [(0, 0), (1, 0), (2, 0)],
               "tetrominoes1": [(0, 0)],
               "tetrominoes2": [(0, 0)],
               "tetrominoes3": [(0, 0)],
               "tetrominoes4": [(0, 0)],
               "tetrominoes5": [(0, 0)],
               "pentominoe1": [(0, 0)],
               "pentominoe2": [(0, 0)],
               "pentominoe3": [(0, 0)],
               "pentominoe4": [(0, 0)],
               "pentominoe5": [(0, 0)],
               "pentominoe6": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
               "pentominoe7": [(0, 0)],
               "pentominoe8": [(0, 0)],
               "pentominoe9": [(0, 0)],
               "pentominoe10": [(0, 0)],
               "pentominoe11": [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
               "pentominoe12": [(0, 0)]}
# List of all possible orientations piece can be placed
ORIENTATIONS = ["north", "northwest", "south", "southeast", "west", "southwest", "northeast", "east"]


class Board:
    def __init__(self):
        self.reset_board()

    def reset_board(self):
        ''' Creates empty 2-dimensional 20 by 20 array that represents the board.
        '''
        self.board_contents = []
        for _ in range(20):
            row = []
            for _ in range(20):
                row.append(". ")
            self.board_contents.append(row)

    def update_board(self, player_color, index, piece_type, piece_orientation):
        ''' Takes index point and places piece_type on board
            index[0] = x coord
            index[1] = y coord
        '''
        self.player_color = player_color
        for offset in PIECE_TYPES[piece_type]:
            if offset == (0, 0):
                self.place_piece(True, index[0] + offset[0], index[1] + offset[1])  # Orientation doesn't matter since (0, 0) is the reference point
            else:
                new_x, new_y = self.rotate_piece(index, offset, piece_orientation)
                self.place_piece(False, new_x, new_y)

    def rotate_piece(self, index, offset, piece_orientation):
        ''' Orients piece about the index point according to the user/ai-desired orientation
        '''
        x_offset = index[0] + offset[0]
        y_offset = index[1] + offset[1]

        if piece_orientation == "north":
            return self.rotate_by_deg(index, (x_offset, y_offset), math.radians(270))
        elif piece_orientation == "northwest":
            new_x, new_y = self.rotate_by_deg(index, (x_offset, y_offset), math.radians(270))
            return self.flip_piece_x(index, new_x, new_y)
        elif piece_orientation == "south":
            return self.rotate_by_deg(index, (x_offset, y_offset), math.radians(90))
        elif piece_orientation == "southeast":
            new_x, new_y = self.rotate_by_deg(index, (x_offset, y_offset), math.radians(90))
            return self.flip_piece_x(index, new_x, new_y)
        elif piece_orientation == "west":
            return self.rotate_by_deg(index, (x_offset, y_offset), math.radians(180))
        elif piece_orientation == "southwest":
            new_x, new_y = self.rotate_by_deg(index, (x_offset, y_offset), math.radians(180))
            return self.flip_piece_y(index, new_x, new_y)
        elif piece_orientation == "northeast":
            new_x, new_y = self.rotate_by_deg(index, (x_offset, y_offset), math.radians(0))
            return self.flip_piece_y(index, new_x, new_y)
        else:  # Default orientation (East)
            return self.rotate_by_deg(index, (x_offset, y_offset), math.radians(0))

    def rotate_by_deg(self, index, offset_point, angle):
        ''' Rotates offsetted point about the index by the angle provided
        '''
        ox, oy = index
        px, py = offset_point

        new_x = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        new_y = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        return int(round(new_x, 1)), int(round(new_y, 1))

    def flip_piece_x(self, index, x, y):
        ''' Takes the difference between index x and point x, then applies reverse
            difference to the index point. y stays the same
        '''
        return index[0] - (index[0] - x) * -1, y

    def flip_piece_y(self, index, x, y):
        ''' Takes the difference between index y and point y, then applies reverse
            difference to the index point. x stays the same
        '''
        return x, index[0] - (index[0] - y) * -1

    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
    def get_all_valid_moves(self, player_color, player_pieces):
        valid_piece = "domino1"  # get all pieces where there is at least one valid move
        valid_point = (0, 0)
        valid_orientation = "south"
        valid_moves = {valid_piece: [(valid_point, [valid_orientation, "east"])],
                       "pentominoe11": [((7, 7), ["south", "north", "northwest"])]}

        return valid_moves
    ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    def place_piece(self, is_index, x, y):
        '''Sets piece on board
        '''
        if is_index:
            self.board_contents[y][x]= "X "  # For my testing only
        else:
            if self.board_contents[y][x] != ". ":  # Last defence against invalid moves
                                                   # (but it only stops the poiont from being dropped so it will
                                                   # appear overlapped since it doesn't stop the whole piece form being placed)
                print("Couldn't place piece since there was a piece there!")
            else:
                self.board_contents[y][x]= self.player_color

    def display_board(self, current_player, players, round_count):
        ''' Prints out current contents of the board to the console
        '''
        print("\n======================= CURRENT BOARD =======================")
        for count, row in enumerate(self.board_contents):
            if count == 0:
                print("   1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20")
            if count < 9:
                print(count + 1, " ", end="")
                print(*row)
            else:
                print(count + 1, *row)

        print("\n======================================")
        print("ROUND:", str(round_count), "            CURRENT PLAYER:", current_player.player_color)
        print("======================================")
        print("SCORES:  R =", players[0].player_score, "| B =", players[1].player_score, "| G =", players[2].player_score, "| Y =", players[3].player_score)

    #### MINI BOARD SECTION ####
    def reset_mini_board(self, size):
        ''' Resets mini board that's used to help player decide how to orient their
            game piece on the main board
        '''
        self.mini_board= []
        if size * 2 % 2 == 0:
            size= size * 2 + 1
        else:
            size= size * 2

        for _ in range(size):
            row= []
            for _ in range(size):
                row.append(". ")
            self.mini_board.append(row)

    def display_piece(self, piece_type, player_color):
        ''' Displays the piece type without any orientation specified yet.
        '''
        self.player_color= player_color
        self.reset_mini_board(len(PIECE_TYPES[piece_type]))
        index= (len(PIECE_TYPES[piece_type]), len(PIECE_TYPES[piece_type]))

        for offset in PIECE_TYPES[piece_type]:
            self.place_piece_on_mini_board(False, index[0] + offset[0], index[1] + offset[1])

        print("PIECE:", piece_type)
        self.display_mini_board()  # default orientation shown when just displaying the piece before orientation

    def display_possible_orientations(self, piece_type, player_color):
        ''' Displays all the possible orientations the user could choose
            from the selected piece type.
        '''
        self.player_color= player_color
        for piece_orientation in ORIENTATIONS:  # ADD ONLY VALID ORIENTATIONS here.... -> valid(ORIENTATIONS)
            self.reset_mini_board(len(PIECE_TYPES[piece_type]))
            index= (len(PIECE_TYPES[piece_type]), len(PIECE_TYPES[piece_type]))
            for offset in PIECE_TYPES[piece_type]:
                if offset == (0, 0):
                    self.place_piece_on_mini_board(True, index[0] + offset[0], index[1] + offset[1])  # Orientation doesn't matter since (0, 0) is the reference point
                else:
                    new_x, new_y= self.rotate_piece(index, offset, piece_orientation)
                    self.place_piece_on_mini_board(False, new_x, new_y)
            print("ORIENTATION:", piece_orientation.upper().strip())
            self.display_mini_board()

    def place_piece_on_mini_board(self, is_index, x, y):
        ''' Places piece on only mini board. NOT the actual board.
            This is just to help the player visually decide how they
            want their piece placed on the main board.
        '''
        if is_index:
            self.mini_board[y][x]= "X "  # Places X to indicate the connection point/index
        else:
            self.mini_board[y][x]= self.player_color

    def display_mini_board(self):
        ''' Displays piece type only on the mini board
        '''
        for row in self.mini_board:
            print(*row)
        print("\n")

    #### END OF MINI BOARD SECTION ####
