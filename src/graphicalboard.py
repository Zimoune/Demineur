#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`graphicalboard` module

:author: `FIL - IEEA - Univ. Lille1.fr <http://portail.fil.univ-lille1.fr>`_

:date:  2015, september

This module implements some functions to draw a minesweeper game. The
graphical board uses buttons to draw each cell and maps the left-click
and right-click events to interact with the minesweeper.

This module uses from :mod:`minesweeper`:

* :func:`minesweeper.get_width`
* :func:`minesweeper.get_height`
* :func:`minesweeper.get_cell`
* :func:`minesweeper.reveal_all_cells_from`
* :func:`minesweeper.get_state`
* :func:`minesweeper.set_hypothetic`
* :func:`minesweeper.unset_hypothetic`
* :func:`minesweeper.is_bomb`
* :func:`minesweeper.is_hypothetic_bomb`
* :func:`minesweeper.is_revealed`

To draw and run a minesweeper game, one has to:

* create a minesweeper game g
* create a graphical board from the minesweeper g

"""

import os
import minesweeper
import tkinter as tk
from functools import partial

# the list of icons
img = []

def create (g):
    """
    This function creates the graphical board from a game. It also
    launches the event loop. Thus, this is the only function to run to
    have a functional graphical board.

    :param g: the minesweeper game
    :type g: game
    :return: None
    """
    global img
    # create a new Tk window
    win = tk.Tk()
    # define the window title
    win.title ('Minesweeper')
    # load images
    iconpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons")
    img = [
        tk.PhotoImage(file=os.path.join(iconpath,"0.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"1.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"2.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"3.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"4.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"5.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"6.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"7.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"8.gif")),
        tk.PhotoImage(file=os.path.join(iconpath,"9.gif")),  # unrevealed
        tk.PhotoImage(file=os.path.join(iconpath,"10.gif")), # bomb explosed
        tk.PhotoImage(file=os.path.join(iconpath,"11.gif")), # bomb discovered
        tk.PhotoImage(file=os.path.join(iconpath,"12.gif")), # flag
        tk.PhotoImage(file=os.path.join(iconpath,"13.gif"))  # question
    ]
    # create the graphical board made of Tk buttons
    width,height = (minesweeper.get_width(g),minesweeper.get_height(g))
    b = []
    for i in range(width):
        b.insert(i,[])
        for j in range(height):
            button = tk.Button(win,padx=0,pady=0, width=19, height=19, image=img[9])
            button.grid(column = i, row = j)
            b[i].insert(j,button)
            # bind the right-click event
            button.bind("<Button-3>",partial(__changeflag,b=b,g=g,i=j,j=i))
            # bind the left-click event
            button.config(command=partial(__changestate,b,g,j,i))

    # event loop
    win.mainloop()

def __test_end (b,g):
    """
    This function tests if the game is finished or not.  In the first
    case, depending on the state of the game, all graphical cells are
    diabled or events are unbinded.

    :param b: the board of buttons
    :type b: list of list of ``button``
    :param g: the minesweeper game
    :type g: game

    """
    state = minesweeper.get_state(g)
    if state == minesweeper.GameState.losing:
        __disable_game (b,g)
    elif state == minesweeper.GameState.winning:
        __block_game(b,g)
    
def __changestate (b,g,i,j):
    """
    This function is called on left-click on a button.

    :param b: the board of buttons
    :type b: list of list of ``button``
    :param g: the minesweeper game
    :type g: game
    :param i: the x-coordinate of the cell
    :type i: int
    :param j: the y-coordinate of the cell
    :type j: int
    """
    minesweeper.reveal_all_cells_from(g,i,j)
    __redraw(b,g,i,j)
    __test_end (b,g)

def __changeflag (evt,b,g,i,j):
    """
    This function is called on right-click on a button.

    :param b: the board of buttons
    :type b: list of list of ``button``
    :param g: the minesweeper game
    :type g: game
    :param i: the x-coordinate of the cell
    :type i: int
    :param j: the y-coordinate of the cell
    :type j: int
    """
    cell = minesweeper.get_cell(g,i,j)
    if not minesweeper.is_hypothetic_bomb(cell):
        minesweeper.set_hypothetic(cell)
    else:
        minesweeper.unset_hypothetic(cell)
    __redraw(b,g,i,j)
    __test_end (b,g)
    
        
def __block_game (b,g):
    """
    This function is called once the player wins. The chosen behavior
    is to let the board as it and to unbind events.

    :param b: the board of buttons
    :type b: list of list of ``button``
    :param g: the minesweeper game
    :type g: game

    """
    width,height = (minesweeper.get_width(g),minesweeper.get_height(g))
    for i in range(width):
        for j in range(height):
            button = b[i][j]
            button.config(command="")
            button.bind("<Button-3>","")       
            
def __disable_game (b,g):
    """
    This function is called once the player looses. The chosen behavior
    is to shade the board and to unbind events.

    :param b: the board of buttons
    :type b: list of list of ``button``
    :param g: the minesweeper game
    :type g: dict

    """
    width,height = (minesweeper.get_width(g),minesweeper.get_height(g))
    for i in range(width):
        for j in range(height):
            button = b[i][j]
            button.config(state=tk.DISABLED)
            button.bind("<Button-3>","")       

            
def __redraw (b,g,x,y):
    """
    This function draws the board. Positions x and y are used to test
    which bomb icon has to be drawn.

    :param b: the board of buttons
    :type b: list of list of ``button``
    :param g: the minesweeper game
    :type g: game
    :param x: the x-coordinate of the cell
    :type x: int
    :param y: the y-coordinate of the cell
    :type y: int

    """
    global img
    width,height = (minesweeper.get_width(g),minesweeper.get_height(g))
    for i in range(width):
        for j in range(height):
            cell = minesweeper.get_cell(g,j,i)
            button = b[i][j]
            if minesweeper.is_revealed(cell):
                if minesweeper.is_bomb(cell):
                    new_img = img[10]
                    if x == j and y == i:
                        new_img = img[11]
                else:
                    new_img = img[minesweeper.number_of_bombs_in_neighborhood(cell)]
                button.config(relief=tk.FLAT,image=new_img, command = "")
            elif minesweeper.is_hypothetic_bomb(cell):
                button.config(image=img[12])
            else:
                button.config(image=img[9])

    

if __name__ == "__main__":
    pass

    
