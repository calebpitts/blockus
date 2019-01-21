from collections import defaultdict
import math

# {key - piece name: val - offsets from index (assuming piece oriented east)}
# Stores all offsets required to make the game board piece
PIECE_TYPES = {"monomino1": [(0, 0)],
               "domino1": [(0, 0), (1, 0)],
               "trominoe1": [(0, 0), (1, 0), (1, 1)],
               "trominoe2": [(0, 0), (1, 0), (2, 0)],
               "tetrominoes1": [(0, 0), (1, 0), (0, 1), (1, 1)],
               "tetrominoes2": [(0, 0), (1, -1), (1, 0), (2, 0)],
               "tetrominoes3": [(0, 0), (1, 0), (2, 0), (3, 0)],
               "tetrominoes4": [(0, 0), (1, 0), (2, 0), (2, -1)],
               "tetrominoes5": [(0, 0), (1, 0), (1, -1), (2, -1)],
               "pentominoe1": [(0, 0), (0, -1), (1, 0), (2, 0), (3, 0)],
               "pentominoe2": [(0, 0), (0, -1), (0, 1), (1, 0), (2, 0)],
               "pentominoe3": [(0, 0), (0, -1), (0, -2), (1, -2), (2, -2)],
               "pentominoe4": [(0, 0), (1, 0), (1, -1), (2, -1), (3, -1)],
               "pentominoe5": [(0, 0), (0, 1), (1, 0), (2, 0), (2, -1)],
               "pentominoe6": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
               "pentominoe7": [(0, 0), (1, 0), (2, 0), (1, -1), (2, -1)],
               "pentominoe8": [(0, 0), (0, 1), (1, 0), (1, -1), (2, -1)],
               "pentominoe9": [(0, 0), (1, 0), (0, 1), (0, 2), (1, 2)],
               "pentominoe10": [(0, 0), (1, 0), (1, -1), (1, 1), (2, -1)],
               "pentominoe11": [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
               "pentominoe12": [(0, 0), (1, 0), (1, -1), (2, 0), (3, 0)]}

# List of all possible orientations piece can be placed
ORIENTATIONS = ["north", "northwest", "south", "southeast", "west", "southwest", "northeast", "east"]


class Board:
    def __init__(self):
        self.reset_board()

    #### BOARD UPDATE METHODS ####
    def reset_board(self):
        ''' Creates empty 2-dimensional 20 by 20 array that represents a clean board
        '''
        self.board_contents = []
        for _ in range(20):
            row = []
            for _ in range(20):
                row.append(". ")
            self.board_contents.append(row)

    def update_board(self, player_color, piece_type, index, piece_orientation):
        ''' Takes index point and places piece_type on board
            index[0] = x coord
            index[1] = y coord
        '''
        self.player_color = player_color
        for offset in PIECE_TYPES[piece_type]:
            if offset == (0, 0):
                self.place_piece(index[0] + offset[0], index[1] + offset[1])  # Orientation doesn't matter since (0, 0) is the reference point
            else:
                new_x, new_y = self.rotate_piece(index, offset, piece_orientation)
                self.place_piece(new_x, new_y)

    def place_piece(self, x, y):
        ''' Places piece on board by filling board_contents with the current player color
        '''
        self.board_contents[y][x] = self.player_color

    #### PIECE ORIENTATION METHODS ####
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

    #### VALID MOVE METHODS ####
    def fetch_valid_piece_types(self, all_valid_moves):
        ''' Gathers valid piece types from all valid moves
        '''
        return list(all_valid_moves.keys())

    def fetch_valid_indexes(self, all_valid_moves, piece_type):
        ''' Gathers valid indexes associated with a given piece_type from all valid moves
        '''
        # valid_indexes = []
        return list(all_valid_moves[piece_type].keys())

        # return valid_indexes

    def fetch_valid_orientations(self, all_valid_moves, piece_type, index):
        ''' Gathers valid orientations associated with a given piece_type and given index from all valid moves
        '''
        # valid_orientations = []
        return all_valid_moves[piece_type][index]  # Loops through all orientations of the desired piece type and index.

    def check_valid_corner(self, player_color, row_num, col_num):
        ''' Checks if cell lines up with a corner piece that is the same color as the current player.
            Returns True if it satisfies the above conditions, False otherwise.
        '''
        ##############################################################################
        if row_num - 1 < 0 or row_num + 1 > 19 or col_num - 1 < 0 or col_num + 1 > 19:
            return False
        ##############################################################################

        # Adjacent Checks (Top, Left, Right, Bottom) - If at least one adjacent piece is same color, then invalid index
        if (self.board_contents[row_num - 1][col_num] == player_color or
            self.board_contents[row_num][col_num - 1] == player_color or
            self.board_contents[row_num][col_num + 1] == player_color or
                self.board_contents[row_num + 1][col_num] == player_color):
            return False

        # Corner Checks (Topright, Topleft, Bottomright, Bottomleft) - If at least one corner is same color, then valid potential index
        if (self.board_contents[row_num - 1][col_num + 1] == player_color or
            self.board_contents[row_num - 1][col_num - 1] == player_color or
            self.board_contents[row_num + 1][col_num + 1] == player_color or
                self.board_contents[row_num + 1][col_num - 1] == player_color):
            return True

    def gather_empty_corner_indexes(self, player_color):
        ''' Returns a list of tuples with the indexes of empty corner cells that connect to the player's color.
            The corner_index is not adjecent/touching any same color tiles on its sides beside its corners.
        '''
        empty_corner_indexes = []
        for row_num, row in enumerate(self.board_contents):
            for col_num, cell in enumerate(row):
                if self.board_contents[row_num][col_num] == ". ":                      # Check if cell is empty
                    if self.check_valid_corner(player_color, row_num, col_num):        # If cell lines up with any adjacent piece that is the same color, its an invalid move, otherwise valid
                        empty_corner_indexes.append((row_num, col_num))

        return empty_corner_indexes

    def check_cell(self, x, y):
        ''' Checks if cell is empty. If empty return FALSE, otherwise TRUE
            If provided coordinates are out of bounds of the board, return FALSE
        '''
        if x < 0 or x >= 20 or y < 0 or y >= 20:  # If out of bounds..
            return False
        elif self.board_contents[y][x] != ". ":
            return False

        return True

    def check_board(self, player_color, piece_type, index, orientation):
        ''' Takes index point and checks all its offsets to determine if the piece at its given orientation can be placed.
            Does NOT alter the state of the board. Only checks whether piece placement is possible.
            Returns FALSE if ANY offsetted cell is non-empty, returns TRUE otherwise
        '''
        for offset in PIECE_TYPES[piece_type]:
            if offset == (0, 0):  # Don't need to rotate coord since its the index and there is no offset
                if self.check_cell(index[0], index[1]) == False:
                    return False
            else:
                new_x, new_y = self.rotate_piece(index, offset, orientation)
                if self.check_cell(new_x, new_y) == False:
                    return False

        return True

    ####################### IN PROGRESS #############################
    def check_corners(self, corners_coords):
        ''' Checks what corners are still available to play in the first round of the game
        '''
        empty_corners = []
        for corner in corners_coords:
            if self.check_cell(corner[0], corner[1]):
                empty_corners.append((corner[0], corner[1]))
        return empty_corners

    def get_all_valid_moves(self, round_count, player_color, player_pieces):
        ''' Gathers all valid moves on the board that meet the following criteria:
            - Index of selected piece touches same-colored corner of a piece
            - Player piece does not fall outside of the board
            - Player piece does not overlap any of their pieces or other opponent pieces
            - May lay adjacent to another piece as long as its another color
        '''
        if round_count == 0:  # If still first round of game..
            empty_corner_indexes = self.check_corners([(0, 0), (19, 0), (0, 19), (19, 19)])
        else:
            empty_corner_indexes = self.gather_empty_corner_indexes(player_color)

        print("EMPTY CORNER INDEXES:", empty_corner_indexes) ####################################### Remove later...
        all_valid_moves = {}
        for piece_type in player_pieces:
            all_index_orientations = defaultdict(list)  # Valid indexes with their valid orientations dict created for every piece
            for index in empty_corner_indexes:
                for orientation in ORIENTATIONS:
                    if self.check_board(player_color, piece_type, index, orientation):  # Checks piece placement for every piece's valid index and all possible orientations
                        all_index_orientations[index].append(orientation)
            if len(list(all_index_orientations.keys())) > 0:  # If there are valid indexes for the piece type..
                all_valid_moves[piece_type] = all_index_orientations

        return all_valid_moves

    #### UI AND BOARD PREVIEW METHODS ####
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
        ''' Resets mini board that's used to help player decide
            how to orient their game piece on the main board
        '''
        self.mini_board = []
        if size * 2 % 2 == 0:
            size = size * 2 + 1
        else:
            size = size * 2

        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(". ")
            self.mini_board.append(row)

    def display_piece(self, piece_type, player_color):
        ''' Displays the piece type without any orientation specified yet.
        '''
        self.player_color = player_color
        self.reset_mini_board(len(PIECE_TYPES[piece_type]))
        index = (len(PIECE_TYPES[piece_type]), len(PIECE_TYPES[piece_type]))

        for offset in PIECE_TYPES[piece_type]:
            self.place_piece_on_mini_board(False, index[0] + offset[0], index[1] + offset[1])

        print("PIECE:", piece_type)
        self.display_mini_board()  # default orientation shown when just displaying the piece before orientation

    def display_possible_orientations(self, piece_type, player_color, valid_orientations):
        ''' Displays all the possible orientations the user could choose
            from the selected piece type.
        '''
        self.player_color = player_color
        for piece_orientation in valid_orientations:
            self.reset_mini_board(len(PIECE_TYPES[piece_type]))
            index = (len(PIECE_TYPES[piece_type]), len(PIECE_TYPES[piece_type]))
            for offset in PIECE_TYPES[piece_type]:
                if offset == (0, 0):
                    self.place_piece_on_mini_board(True, index[0] + offset[0], index[1] + offset[1])  # Orientation doesn't matter since (0, 0) is the reference point
                else:
                    new_x, new_y = self.rotate_piece(index, offset, piece_orientation)
                    self.place_piece_on_mini_board(False, new_x, new_y)
            print("ORIENTATION:", piece_orientation.upper().strip())
            self.display_mini_board()

    def place_piece_on_mini_board(self, is_index, x, y):
        ''' Places piece on only mini board. **NOT the actual board**
            Helps player visually decide how they want their piece
            to be placed on the main board.
        '''
        if is_index:
            self.mini_board[y][x] = "X "  # Places X to indicate the connection point/index
        else:
            self.mini_board[y][x] = self.player_color

    def display_mini_board(self):
        ''' Displays piece type only on the mini board
        '''
        for row in self.mini_board:
            print(*row)
        print("\n")
