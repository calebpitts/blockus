import sys
import pygame as pg
clock = pg.time.Clock()


COLORS = {'R': (220, 20, 60),
          'B': (30, 144, 255),
          'G': (50, 205, 50),
          'Y': (255, 255, 102),
          '.': (220, 220, 220)}


def get_cell_color(x, y, board_contents):
    ''' Returns string of the color of the current cell at coords x and y
    '''
    cell = board_contents[y][x]  # color code with turn num
    color = cell[0]  # color code
    return COLORS[color]


def setup_texts(current_player, players, round_count):
    ''' Sets up texts to be displayed on the gui board.
    '''
    player_text = "Player: " + current_player.player_color
    round_text = "Round: " + str(round_count)
    scores_text = "SCORES:  R = " + str(players[0].player_score) + " | B = " + str(players[1].player_score) + " | G = " + str(players[2].player_score) + " | Y = " + str(players[3].player_score)

    titlefont = pg.font.SysFont('Helvetica', 30)
    gamefont = pg.font.SysFont('Helvetica', 20)

    titlesurface = titlefont.render('Blockus', True, (255, 255, 255))
    player_indicator = gamefont.render(player_text, True, (255, 255, 255))
    round_indicator = gamefont.render(round_text, True, (255, 255, 255))
    scores_indicator = gamefont.render(scores_text, True, (255, 255, 255))

    return titlesurface, player_indicator, round_indicator, scores_indicator


def prep_cells(board_contents):
    ''' Preps cells to be drawn on gui board corresponding to the board contents. 
    '''
    rectangles = []
    height = 20
    width = 20
    size = 40

    for y in range(height):
        for x in range(width):
            rect = pg.Rect(x * (size + 1), y * (size + 1) + 55, size, size)
            # The grid will be a list of (rect, color) tuples.
            color = get_cell_color(x, y, board_contents)
            rectangles.append((rect, color))

    return rectangles


def display_board(board_contents, current_player, players, round_count, winners=None):
    ''' Displays board contents and other game-related stats to a gui using pygame.
    '''
    screen = pg.display.set_mode((819, 960))

    titlesurface, player_indicator, round_indicator, scores_indicator = setup_texts(current_player, players, round_count)

    screen.blit(titlesurface, (355, 13))
    screen.blit(player_indicator, (10, 20))
    screen.blit(round_indicator, (700, 20))
    screen.blit(scores_indicator, (10, 895))

    rectangles = prep_cells(board_contents)
    for rect, color in rectangles:
        pg.draw.rect(screen, color, rect)

    winner_indicator = None

    # if winner is not None:  # NOT WORKING
    #     print("FOUND WINNER", winner)
    #     scores_text = "WINNER: " + winner
    #     winner_font = pg.font.SysFont('Helvetica', 20)
    #     winner_indicator = winner_font.render(scores_text, True, (255, 255, 255))
    #     screen.blit(winner_indicator, (10, 920))  # Pop-up block appears when winner determined
    #     pg.display.update()

    pg.display.flip()
    clock.tick(60)

    # pg.display.update()


def start_gui():
    pg.display.init()
    pg.display.set_caption('Blockus Game - Beta')
    pg.font.init()


def terminate_gui():
    pg.display.quit()
    pg.quit()
    print("quit pygame")
    sys.exit(0)

# PIECES FOR LATER?
# elif pg.mouse.get_pressed()[0]:
#     mouse_pos = pg.mouse.get_pos()
#     # Enumerate creates tuples of a number (the index)
#     # and the rect-color tuple, so it looks like:
#     # (0, (<rect(0, 0, 20, 20)>, (255, 255, 255)))
#     # You can unpack them directly in the head of the loop.
#     for index, (rect, color) in enumerate(rectangles):
#         if rect.collidepoint(mouse_pos):
#             # Create a tuple with the new color and assign it.
#             rectangles[index] = (rect, new_color)
