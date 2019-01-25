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
        self.test_contents = []
        for _ in range(20):
            row = []
            for _ in range(20):
                row.append(". ")
            self.board_contents.append(row)

        for _ in range(20):
            row = []
            for _ in range(20):
                row.append(".  ")
            self.test_contents.append(row)

        #self.board_contents = [['R ', 'R ', 'R ', '. ', '. ', 'R ', 'R ', 'R ', 'R ', 'Y ', 'Y ', 'R ', '. ', 'Y ', '. ', 'B ', 'B ', '. ', '. ', 'B '], ['R ', '. ', 'R ', '. ', 'R ', '. ', 'Y ', 'Y ', 'Y ', 'R ', 'R ', 'Y ', 'Y ', '. ', 'B ', '. ', '. ', 'B ', '. ', 'B '], ['. ', 'R ', '. ', 'R ', 'R ', '. ', 'Y ', '. ', 'R ', 'R ', '. ', 'Y ', '. ', 'B ', 'B ', 'B ', '. ', 'B ', '. ', 'B '], ['G ', 'R ', 'R ', 'G ', 'G ', 'R ', 'Y ', '. ', 'R ', '. ', '. ', 'Y ', '. ', 'B ', '. ', '. ', '. ', 'B ', '. ', 'B '], ['G ', 'R ', 'R ', '. ', 'G ', 'R ', '. ', 'Y ', 'Y ', 'Y ', 'Y ', '. ', 'Y ', '. ', 'B ', 'B ', 'B ', '. ', 'B ', '. '], ['G ', 'G ', '. ', 'R ', 'R ', 'G ', 'R ', 'R ', '. ', '. ', '. ', '. ', 'Y ', '. ', 'B ', '. ', 'B ', '. ', '. ', 'B '], ['G ', '. ', '. ', 'R ', 'R ', '. ', 'G ', 'R ', 'R ', 'R ', '. ', '. ', 'Y ', '. ', '. ', 'B ', '. ', '. ', '. ', 'B '], ['. ', 'G ', 'G ', 'G ', '. ', 'R ', 'G ', '. ', '. ', '. ', '. ', 'Y ', 'Y ', '. ', '. ', 'B ', 'B ', '. ', '. ', 'B '], ['G ', '. ', '. ', 'G ', 'R ', 'R ', 'G ', '. ', 'Y ', 'Y ', 'Y ', '. ', '. ', 'Y ', 'Y ', 'B ', '. ', '. ', '. ', 'B '], ['G ', '. ', '. ', 'G ', '. ', 'R ', 'G ', 'G ', 'Y ', '. ', 'Y ', '. ', '. ', 'Y ', '. ', 'B ', '. ', '. ', '. ', 'B '], ['G ', '. ', 'G ', '. ', 'G ', 'G ', 'R ', '. ', 'G ', '. ', '. ', '. ', 'Y ', 'Y ', '. ', '. ', 'B ', 'B ', 'B ', '. '], ['G ', '. ', 'G ', '. ', 'G ', 'G ', 'R ', 'R ', 'G ', '. ', 'Y ', 'Y ', '. ', 'B ', 'Y ', 'B ', '. ', '. ', 'B ', '. '], ['G ', '. ', 'G ', 'G ', '. ', '. ', 'G ', 'R ', 'G ', 'Y ', '. ', 'Y ', 'Y ', 'B ', 'Y ', 'B ', 'B ', '. ', 'B ', '. '], ['. ', 'G ', '. ', '. ', '. ', 'G ', 'G ', 'Y ', 'G ', 'Y ', 'Y ', '. ', 'Y ', 'B ', 'Y ', 'Y ', 'B ', '. ', '. ', 'B '], ['. ', 'G ', '. ', '. ', '. ', 'G ', 'G ', 'Y ', 'Y ', 'G ', 'Y ', '. ', 'B ', 'B ', '. ', 'Y ', 'B ', '. ', 'B ', 'B '], ['G ', 'G ', '. ', '. ', 'G ', '. ', '. ', '. ', 'G ', 'G ', 'G ', 'B ', '. ', '. ', 'B ', 'B ', 'Y ', 'Y ', '. ', 'B '], ['G ', '. ', '. ', '. ', 'G ', '. ', '. ', '. ', '. ', '. ', 'G ', 'B ', 'B ', '. ', 'B ', 'B ', 'Y ', 'Y ', '. ', '. '], ['. ', 'G ', '. ', '. ', 'G ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', 'B ', '. ', '. ', '. ', '. ', 'Y ', '. ', '. '], ['G ', 'G ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', 'Y ', 'Y '], ['G ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', '. ', 'Y ', 'Y ']]
        #self.test_contents = [['R0 ', '.  ', 'R13', '.  ', '.  ', 'R3 ', 'R3 ', 'R3 ', '.  ', 'R5 ', 'R5 ', '.  ', '.  ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', 'B2 ', '.  ', 'B0 '], ['R0 ', '.  ', '.  ', 'R2 ', 'R2 ', '.  ', 'R3 ', 'R3 ', '.  ', 'R5 ', 'Y6 ', 'Y6 ', 'B3 ', '.  ', '.  ', '.  ', '.  ', '.  ', 'B1 ', '.  '], ['.  ', 'R1 ', 'R1 ', '.  ', 'R2 ', 'R2 ', '.  ', '.  ', 'R4 ', '.  ', '.  ', 'Y6 ', 'B3 ', 'B3 ', '.  ', '.  ', 'B7 ', '.  ', 'B1 ', '.  '], ['.  ', 'R1 ', '.  ', '.  ', 'G6 ', 'G6 ', '.  ', '.  ', 'R4 ', '.  ', 'B4 ', 'B4 ', 'Y5 ', 'B3 ', '.  ', 'B7 ', 'B7 ', '.  ', 'B1 ', 'B1 '], ['R1 ', 'R1 ', '.  ', 'G5 ', '.  ', 'G6 ', 'G6 ', 'G6 ', 'R4 ', 'R4 ', '.  ', 'B4 ', 'Y5 ', 'B3 ', '.  ', 'B7 ', '.  ', 'B5 ', '.  ', '.  '], ['G9 ', '.  ', 'R9 ', 'G5 ', '.  ', 'B12', 'B12', 'R6 ', '.  ', '.  ', 'B4 ', 'B4 ', 'Y5 ', '.  ', 'B6 ', '.  ', '.  ', 'B5 ', '.  ', '.  '], ['G9 ', 'R9 ', 'R9 ', 'G5 ', '.  ', 'B12', 'R6 ', 'R6 ', 'R6 ', 'Y7 ', 'Y7 ', 'Y7 ', 'B9 ', 'Y4 ', 'B6 ', 'Y8 ', '.  ', '.  ', 'B8 ', 'B8 '], ['G9 ', '.  ', 'R9 ', 'G5 ', 'R7 ', 'R7 ', 'B11', 'B11', 'R6 ', 'Y7 ', '.  ', '.  ', 'B9 ', 'Y4 ', 'B6 ', 'Y8 ', 'Y8 ', 'Y8 ', 'B8 ', 'B8 '], ['.  ', 'G4 ', 'G4 ', '.  ', '.  ', 'R7 ', 'R7 ', 'B11', 'B11', 'Y7 ', 'B9 ', 'B9 ', 'B9 ', 'Y4 ', 'Y4 ', '.  ', '.  ', 'Y8 ', '.  ', '.  '], ['.  ', 'G4 ', 'G4 ', '.  ', '.  ', '.  ', 'R7 ', 'B11', '.  ', 'B10', 'Y9 ', '.  ', '.  ', '.  ', 'Y4 ', '.  ', '.  ', '.  ', 'Y14', 'Y14'], ['G3 ', '.  ', '.  ', 'G7 ', 'G7 ', 'G7 ', '.  ', 'R8 ', 'B10', 'B10', 'Y9 ', 'Y9 ', '.  ', 'Y10', '.  ', 'Y3 ', '.  ', '.  ', 'Y14', 'Y14'], ['.  ', 'G2 ', '.  ', 'G7 ', '.  ', 'G7 ', '.  ', 'R8 ', 'R8 ', 'B10', 'Y9 ', 'Y9 ', 'G13', 'Y10', '.  ', 'Y3 ', 'Y3 ', 'Y3 ', '.  ', '.  '], ['.  ', 'G2 ', 'G2 ', '.  ', 'G8 ', '.  ', 'R10', '.  ', 'R8 ', '.  ', '.  ', 'R11', 'G13', 'Y10', 'Y10', '.  ', 'Y3 ', '.  ', '.  ', 'Y13'], ['.  ', '.  ', 'G2 ', '.  ', 'G8 ', 'G8 ', 'R10', '.  ', 'R8 ', '.  ', '.  ', 'R11', 'G13', '.  ', '.  ', 'Y11', '.  ', 'Y2 ', '.  ', 'Y13'], ['G1 ', 'G1 ', '.  ', '.  ', 'G8 ', '.  ', 'R10', '.  ', '.  ', 'R11', 'R11', 'R11', 'G13', 'G13', 'Y11', 'Y11', '.  ', 'Y2 ', '.  ', 'Y13'], ['.  ', 'G1 ', '.  ', '.  ', 'G8 ', '.  ', 'R10', '.  ', '.  ', '.  ', 'G11', 'G11', 'R12', 'Y11', 'Y11', '.  ', 'Y2 ', 'Y2 ', '.  ', 'Y13'], ['.  ', 'G1 ', 'G1 ', '.  ', '.  ', 'G10', 'G10', 'G10', 'G10', 'G10', '.  ', 'G11', 'R12', '.  ', '.  ', 'Y12', '.  ', 'Y2 ', '.  ', 'Y13'], ['G0 ', '.  ', '.  ', '.  ', 'G12', '.  ', '.  ', '.  ', '.  ', '.  ', 'G14', '.  ', 'R12', '.  ', '.  ', 'Y12', 'Y12', '.  ', 'Y1 ', '.  '], ['G0 ', 'G0 ', '.  ', 'G12', 'G12', 'G12', '.  ', '.  ', '.  ', '.  ', 'G14', '.  ', 'R12', '.  ', '.  ', 'Y12', '.  ', '.  ', '.  ', 'Y0 '], ['G0 ', '.  ', '.  ', '.  ', '.  ', 'G12', '.  ', '.  ', '.  ', '.  ', 'G14', 'G14', 'R12', '.  ', '.  ', '.  ', '.  ', '.  ', '.  ', 'Y0 ']]

    def update_board(self, player_color, piece_type, index, piece_orientation, round_count):
        ''' Takes index point and places piece_type on board
            index[0] = x coord
            index[1] = y coord
        '''
        self.player_color = player_color
        for offset in PIECE_TYPES[piece_type]:
            if offset == (0, 0):
                self.place_piece(index[0] + offset[0], index[1] + offset[1], round_count)  # Orientation doesn't matter since (0, 0) is the reference point
            else:
                new_x, new_y = self.rotate_piece(index, offset, piece_orientation)
                self.place_piece(new_x, new_y, round_count)

    def place_piece(self, x, y, round_count):
        ''' Places piece on board by filling board_contents with the current player color
        '''
        self.board_contents[y][x] = self.player_color
        if round_count < 10:
            self.test_contents[y][x] = self.player_color.strip() + str(round_count) + " "  # TESTING ONLY
        else:
            self.test_contents[y][x] = self.player_color.strip() + str(round_count)   # TESTING ONLY

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
        # return x, index[0] - (index[0] - y) * -1
        return x, index[1] + (y - index[1]) * -1

    # VALID MOVE METHODS ####  ->  IN PROGRESS
    def gather_empty_board_corners(self, corners_coords):
        ''' Checks what corners are still available to play in the first round of the game
        '''
        empty_corners = []
        for corner in corners_coords:
            if self.board_contents[corner[1]][corner[0]] == ". ":
                empty_corners.append((corner[0], corner[1]))
        return empty_corners

    def check_valid_corner(self, player_color, row_num, col_num):
        ''' Checks whether all adjacent pieces are a different color to the current player's color.
            Checks if any corner piece is the same color as the current player.
        '''
        if not self.is_valid_adjacents(row_num, col_num, player_color):  # Not a valid corner if adjacents are same color
            return False

        # Exclude top and right edge cases
        if row_num != 0 and col_num != 19:
            if self.board_contents[row_num - 1][col_num + 1] == player_color:
                return True

        # Exclude top and left cases
        if row_num != 0 and col_num != 0:
            if self.board_contents[row_num - 1][col_num - 1] == player_color:
                return True

        # Exclude bottom and right edge cases
        if row_num != 19 and col_num != 19:
            if self.board_contents[row_num + 1][col_num + 1] == player_color:
                return True

        # Exclude bottom and left cases
        if row_num != 19 and col_num != 0:
            if self.board_contents[row_num + 1][col_num - 1] == player_color:
                return True

        return False

    def gather_empty_corner_indexes(self, player_color):
        ''' Returns a list of tuples with the indexes of empty corner cells that connect to the player's color.
            The corner_index is not adjecent/touching any same color tiles on its sides beside its corners.
        '''
        empty_corner_indexes = []
        for row_num, row in enumerate(self.board_contents):
            for col_num, cell in enumerate(row):
                if cell == ". ":                                                       # Check if cell is empty
                    if self.check_valid_corner(player_color, row_num, col_num):        # If cell lines up with any adjacent piece that is the same color, its an invalid move, otherwise valid
                        empty_corner_indexes.append((col_num, row_num))

        return empty_corner_indexes

    def is_valid_adjacents(self, row_num, col_num, player_color):
        # Adjacent Checks (Top, Left, Right, Bottom) - If at least one adjacent piece is same color, then invalid index
        valid_adjacent = True

        # Exclude top edge
        if row_num != 0:
            if self.board_contents[row_num - 1][col_num] == player_color:
                valid_adjacent = False
        # Exclude left edge
        if col_num != 0:
            if self.board_contents[row_num][col_num - 1] == player_color:
                valid_adjacent = False
        # Exclude bottom edge
        if row_num != 19:
            if self.board_contents[row_num + 1][col_num] == player_color:
                valid_adjacent = False
        # Exclude right edge
        if col_num != 19:
            if self.board_contents[row_num][col_num + 1] == player_color:
                valid_adjacent = False

        return valid_adjacent

    def is_valid_cell(self, x, y, player_color):
        ''' Checks if cell is empty, has no adjacent cells that are the same color,
            and whether the given cell is out of bounds of the 20x20 board.
        '''
        if x < 0 or x >= 20 or y < 0 or y >= 20:  # Out of bounds..
            return False
        if (self.board_contents[y][x] == ". " and self.is_valid_adjacents(y, x, player_color)):  # If cell empty and has no adjacent pieces that are the same color, return TRUE
            return True
        return False  # Invalid adjacent or space filled already..

    def is_valid_move(self, player_color, piece_type, index, orientation):
        ''' Takes index point and checks all its offsets to determine if the piece at its given orientation can be placed.
            Does NOT alter the state of the board. Only checks whether piece placement is possible.
            Returns FALSE if ANY offsetted cell is invalid.
        '''
        for offset in PIECE_TYPES[piece_type]:
            if offset == (0, 0):  # No need to rotate coord since its the index and there is no offset
                if not self.is_valid_cell(index[0], index[1], player_color):
                    return False
            else:
                new_x, new_y = self.rotate_piece(index, offset, orientation)
                if not self.is_valid_cell(new_x, new_y, player_color):
                    return False

        return True

    def get_all_valid_moves(self, round_count, player_color, player_pieces):
        ''' Gathers all valid moves on the board that meet the following criteria:
            - Index of selected piece touches same-colored corner of a piece
            - Player piece does not fall outside of the board
            - Player piece does not overlap any of their pieces or other opponent pieces
            - May lay adjacent to another piece as long as its another color
        '''
        if round_count == 0:  # If still first round of game..
            empty_corner_indexes = self.gather_empty_board_corners([(0, 0), (19, 0), (0, 19), (19, 19)])
        else:
            empty_corner_indexes = self.gather_empty_corner_indexes(player_color)

        print("EMPTY CORNER INDEXES:", empty_corner_indexes)  # Remove later... #######################################
        all_valid_moves = {}
        for piece_type in player_pieces:
            all_index_orientations = defaultdict(list)  # Valid indexes with their valid orientations dict created for every piece
            for index in empty_corner_indexes:
                for orientation in ORIENTATIONS:
                    if self.is_valid_move(player_color, piece_type, index, orientation):  # Checks if piece placement for every piece's valid index and all possible orientations is a valid move
                        all_index_orientations[index].append(orientation)
            if len(list(all_index_orientations.keys())) > 0:  # If there are valid indexes for the piece type..
                all_valid_moves[piece_type] = all_index_orientations

        #all_valid_moves = {'pentominoe8': {(14, 13): ['northwest', 'west'], (17, 13): ['north'], (12, 16): ['northwest', 'west', 'southwest', 'northeast'], (12, 19): ['southwest', 'northeast'], (14, 19): ['southwest', 'northeast']}, 'pentominoe11': {(12, 16): ['southwest', 'northeast'], (12, 19): ['southwest', 'northeast'], (14, 19): ['southwest', 'northeast']}, 'pentominoe12': {(14, 13): ['north', 'northwest', 'west', 'southwest'], (17, 13): ['north', 'northwest'], (14, 15): ['southwest'], (19, 15): ['north'], (12, 16): ['north', 'northwest', 'west', 'southwest', 'northeast'], (12, 19): ['southwest', 'northeast'], (14, 19): ['southwest', 'northeast']}}

        return all_valid_moves

    #### UI AND BOARD PREVIEW METHODS ####
    def display_board(self, current_player, players, round_count):
        ''' Prints out current contents of the board to the console
        '''
        # print(self.test_contents)
        print("\n======================= CURRENT BOARD =======================")
        for count, row in enumerate(self.test_contents):
            if count == 0:
                print("   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20")
            if count < 9:
                print(count + 1, " ", end="")
                print(*row)
            else:
                print(count + 1, *row)

        print("\n======================================")
        print("ROUND:", str(round_count), "            CURRENT PLAYER:", current_player.player_color)
        print("======================================")
        print("SCORES:  R =", players[0].player_score, "| B =", players[1].player_score, "| G =", players[2].player_score, "| Y =", players[3].player_score)

    def display_endgame_board(self):
        ''' Prints out contents of board at the end of the game.
        '''
        print("\n======================== FINAL BOARD ========================")
        for count, row in enumerate(self.test_contents):
            if count == 0:
                print("   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20")
            if count < 9:
                print(count + 1, " ", end="")
                print(*row)
            else:
                print(count + 1, *row)
        print("\n=============================================================")

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
