import minesweeper as ms
import sys

def launch(width, height, bombs):
    """
    launch the game
    :param width: width of the game
    :type width: int
    :param height: height of the game
    :type height: int
    :param bombs: number of bombs
    :type bombs: int
    """
    game = ms.make_game(width, height, bombs)
    state = ms.get_state(game)
    while state == ms.GameState.unfinished:
        try:
            display_game(game)
            play(game)
            state = ms.get_state(game)
        except KeyboardInterrupt:
            sys.exit()
    display_game(game)
    if state == ms.GameState.losing:
        print("You lose!")
    elif state == ms.GameState.unfinished:
        print("You win!")
    else:
        print("an unexpected error has occured, please contact the developpers")

def play(game):
    """
    require action to the player and execute it
    :param game: game
    :type game: a minesweeper game
    :return: None
    :rtype: NoneType
    :UC: none
    """
    action = keyboard_input(game)
    x = action[0]
    y = action[1]
    a = action[2]
    if a == 'R':
        ms.reveal_all_cells_from(game,x, y)
    elif a == 'S':
        cell = ms.get_cell(game, x, y)
        ms.set_hypothetic(cell)
    elif a == 'U':
        cell = ms.get_cell(game, x, y)
        ms.unset_hypothetic(cell)

def keyboard_input(game):
    """
    :param game: game
    :type game: a minesweeper game
    :return: the player input action
    :rtype: tuple of the action (posX, posY, action)
    :UC: none
    """
    try:
        data_in = input("Your play x,y,C (C=(R)eval,(S)et,(U)nset): ")
        ldata = data_in.split(',')
        x = int(ldata[0])
        y = int(ldata[1])
        c = ldata[2]
        assert x >= 0 and x < ms.get_height(game)
        assert y >= 0 and x < ms.get_width(game)
        c = c.upper()
        assert c == 'R' or c == 'S' or c == 'U'
        return (x, y, c)
    except AssertionError:
        print("Numbers must be in range of the game")
        keyboard_input(game)
    except IndexError:
        print ('There must be two numbers and one letter separated by a comma (,)')
        keyboard_input(game)
    except TypeError:
        print ('There must be two numbers and one letter separated by a comma (,)')
        keyboard_input(game)
    except ValueError:
        print ("x and y must be integers and c must be R or S or U")
        keyboard_input(game)

def display_game(game):
    """
    display the game in stdout
    :param game: game
    :type game: a minesweeper game
    :return: None
    :rType: NoneType
    :UC: none
    """
    display_line = "+---"*ms.get_width(game) 
    display_line += "+"
    print(" ", end="")
    for i in range(ms.get_width(game)-1):
        print("  ", i, end="")
    print("  ",ms.get_width(game)-1)
    for h in range(ms.get_height(game)):
        numerotation = ""
        print(" ",display_line)
        print(h ,"",end="")
        for l in range(ms.get_width(game)):
            character = " "
            cell = ms.get_cell(game, h, l)
            if ms.is_revealed(cell):
                if ms.is_bomb(cell):
                    character = "B"
                else:
                    character = ms.number_of_bombs_in_neighborhood(cell)
            elif ms.is_hypothetic_bomb(cell):
                    character = "?"
            print("| ",character, end="")
        print("|")
    print(" ",display_line)
            

if __name__ == '__main__':
    if len(sys.argv) == 4:
        try:
            w = int(sys.argv[1])
            h = int(sys.argv[2])
            b = int(sys.argv[3])
            launch(w, h, b)
        except ValueError:
            print("arguments must be integers")
        except IndexError:
            print("there must have 3 arguments or no one")
    else:
        launch(width = 10, height = 10, bombs = 10)
