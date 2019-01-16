# List of all possible pieces that can be placed on board regardless of player.
PIECE_TYPES = {"monomino": [(0, 0)], "domino": [(0, 0), (1, 0)]}


class Board:
    def __init__(self, player_color):
        self.player_color = player_color
        self.initialize_board()

    def initialize_board(self):
        ''' Creates empty 2-dimensional 20 by 20 array that represents the board.
        '''
        self.board_contents = []
        i = 0
        while i < 20:
            row = []
            j = 0
            while j < 20:
                row.append(". ")
                j += 1
            self.board_contents.append(row)
            i += 1

    def update_board(self, index, piece_type):
        ''' Takes index point and places piece_type on board
            index[0] = x coord
            index[1] = y coord
        '''
        for offset in PIECE_TYPES[piece_type]:
            self.place_piece(index[0] + offset[0], index[1] + offset[1])

    def place_piece(self, x, y):
        self.board_contents[y][x] = self.player_color

    def display_board(self):
        ''' Prints out current contents of the board to the console
        '''
        for row in self.board_contents:
            print(*row)

    def get_player_color(self):
        ''' Returns the current player color
        '''
        return self.player_color
