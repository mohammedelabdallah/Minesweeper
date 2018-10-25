#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`minesweeper` module

:author: KROL Mikolai ; ELABDALLAH Mohammed

:date:  

This module provides functions and a class for minesweeper's game's management.

"""

import random
from enum import Enum
from cell import Cell


################################################
# Type declaration
################################################

class GameState(Enum):
    """
    A class to define an enumerated type with three values :

    * ``winning``
    * ``losing``
    * ``unfinished``

    for the three state of minesweeper game.
    """
    winning = 1
    losing = 2
    unfinished = 3


##############################################
# Function for game's setup and management
##############################################


def neighborhood(x, y, width, height):
    """
    :param x: x-coordinate of a cell
    :type x: int
    :param y: y-coordinate of a cell
    :type y: int
    :param height: height of the grid
    :type height: int
    :param width: widthof the grid
    :type width: int
    :return: the list of coordinates of the neighbors of position (x,y) in a
             grid of size width*height
    :rtype: list of tuple
    :UC: 0 <= x < width and 0 <= y < height
    :Examples:

    >>> neighborhood(3, 3, 10, 10)
    [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]
    >>> neighborhood(0, 3, 10, 10)
    [(0, 2), (0, 4), (1, 2), (1, 3), (1, 4)]
    >>> neighborhood(0, 0, 10, 10)
    [(0, 1), (1, 0), (1, 1)]
    >>> neighborhood(9, 9, 10, 10)
    [(8, 8), (8, 9), (9, 8)]
    >>> neighborhood(3, 9, 10, 10)
    [(2, 8), (2, 9), (3, 8), (4, 8), (4, 9)]
    """
    l=[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
    l2=[]
    for t in l:
        if 0<=t[0]<width and 0<=t[1]<height:
            l2+=[t]
    return l2
    
    
       

class Minesweeper():
    """
    >>> game = Minesweeper(20, 10, 4)
    >>> game.get_width()
    20
    >>> game.get_height()
    10
    >>> game.get_nbombs()
    4
    >>> game.get_state() == GameState.unfinished 
    True
    >>> cel = game.get_cell(1, 2)
    >>> cel.is_revealed()
    False
    >>> 
    """

    def __init__(self, width=30, height=20, nbombs=99):
        """
        build a minesweeper grid of size width*height cells
        with nbombs bombs randomly placed.  

        :param width:[optional] horizontal size of game (default = 30)
        :type width: int
        :param height: [optional] vertical size of game (default = 20)
        :type height: int
        :param nbombs: [optional] number of bombs (default = 99)
        :type nbombs: int
        :return: a fresh grid of  width*height cells with nbombs bombs randomly placed.
        :rtype: Minesweeper
        :UC: width and height must be positive integers, and
             nbombs <= width * height
        :Example:

        >>> game = Minesweeper(20, 10, 4)
        >>> game.get_width()
        20
        >>> game.get_height()
        10
        >>> game.get_nbombs()
        4
        >>> game.get_state() == GameState.unfinished 
        True
        """
        self.height=height
        self.width=width
        self.nbombs=nbombs
        self.grid=[[Cell() for i in range(self.width)] for j in range(self.height)]
        for i in range(self.nbombs):
            rand_width=random.randint(0,width-1)
            rand_height=random.randint(0,height-1)
            if not self.grid[rand_height][rand_width].is_bomb():
                self.grid[rand_height][rand_width].set_bomb()
            else:
                self.nbombs+=1
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].is_bomb():
                    l=neighborhood(x,y,self.width,self.height)
                    for coor in l:
                        self.grid[coor[1]][coor[0]].incr_number_of_bombs_in_neighborhood()
        self.state=GameState.unfinished

    def get_height(self):
        """
        :return: height of the grid in self
        :rtype: int
        :UC: none
        """
        return self.height

    def get_width(self):
        """
        :return: width of the grid in game
        :rtype: int
        :UC: none
            """
        return self.width
    
    def get_nbombs(self):
        """
        :return: number of bombs in game
        :rtype: int
        :UC: none
        """
        return self.nbombs


    def get_cell(self, x, y):
        """
        :param x: x-coordinate of a cell
        :type x: int
        :param y: y-coordinate of a cell
        :type y: int
        :return: the cell of coordinates (x,y) in the game's grid
        :type: cell
        :UC: 0 <= x < width of game and O <= y < height of game
        """
        return self.grid[y][x]


    def get_state(self):
        """
        :return: the state of the game (winning, losing or unfinished)
        :rtype: GameState
        :UC: none
        """
        list_of_cells_with_bomb=[]
        list_of_cells_hypothetic=[]
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].is_bomb():
                    list_of_cells_with_bomb+=[self.grid[y][x]]
                    if self.grid[y][x].is_hypothetic():
                        list_of_cells_hypothetic+=[self.grid[y][x]]
        for c in list_of_cells_hypothetic:
            if not c.is_bomb():
                return self.state
        if len(list_of_cells_with_bomb)==len(list_of_cells_hypothetic):
            self.state=GameState.winning
        return self.state
    
    def reveal_all_cells_from(self, x, y):
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :return: none
        :side effect: reveal all cells of game game from the initial cell (x,y).
        :UC: 0 <= x < width of game and O <= y < height of game
        """
        if self.grid[y][x].is_bomb():
            self.grid[y][x].reveal()
            self.state=GameState.losing
        elif self.grid[y][x].number_of_bombs_in_neighborhood()!=0:
            self.grid[y][x].reveal()
        else:
            if not self.grid[y][x].is_revealed():
                self.grid[y][x].reveal()
                l=neighborhood(x,y,self.width,self.height)
                for coor in l:
                    self.reveal_all_cells_from(coor[0],coor[1])
            
        
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)


