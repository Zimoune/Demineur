import graphicalboard as graphic
import minesweeper as ms
import sys

def launch(y,x,b):
    """
    launch a minesweeper game with a graphical board
    :param y: width of the game
    :type y: int
    :param x: height of the game
    :type x: int
    :param b: number of bombs
    :type b: int
    """
    game = ms.make_game(y,x,b)
    graphic.create(game)

if __name__ == '__main__':
    #assert len(sys.argv) == 4
    #launch(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
    launch(30,30,10)
