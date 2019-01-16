import board
import player
import math


def main():
    myboard = board.Board()
    #myboard.update_board("B ", (1, 2), "monomino", "")
    #myboard.update_board("B ", (0, 0), "domino", "north")
    myboard.update_board("R ", (2, 2), "pentominoe6", "")
    #x, y = myboard.rotate_test((7, 7), (8, 7), math.radians(90))
    #point = (x, y)
    # print(point)
    print("\n\n\n")
    myboard.display_board()


if __name__ == "__main__":
    main()
