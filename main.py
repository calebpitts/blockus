import board
import player


def main():
    myboard = board.Board("B ")
    myboard.display_board()
    myboard.update_board((1, 2), "monomino")
    myboard.update_board((0, 0), "domino")
    print("\n\n\n")
    myboard.display_board()


if __name__ == "__main__":
    main()
