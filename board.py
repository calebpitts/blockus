import math

# List of all possible pieces that can be placed on board regardless of player.
PIECE_TYPES = {"monomino": [(0, 0)],
               "domino": [(0, 0), (1, 0)],
               "trominoe1": [(0, 0), (1, 0), (1, 1)],
               "trominoe2": [(0, 0), (1, 0), (2, 0)],
               "pentominoe6": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
               "pentominoe11": [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]}


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

    def place_piece(self, is_index, x, y):
        '''Sets piece on board
        '''
        if is_index:
            self.board_contents[y][x] = "X "  # For my testing only
        else:
            if self.board_contents[y][x] != ". ":  # Last defence against invalid moves
                                                   # (but it only stops the poiont from being dropped so it will
                                                   # appear overlapped since it doesn't stop the whole piece form being placed)
                print("Couldn't place piece since there was a piece there!")
            else:
                self.board_contents[y][x] = self.player_color

    def display_board(self):
        ''' Prints out current contents of the board to the console
        '''
        for row in self.board_contents:
            print(*row)
