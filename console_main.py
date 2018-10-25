#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`main` module

:author: `KROL Mikolaï ; ELABDALLAH Mohammed`_

:date:  2018, october.

Main module to play the minesweeper's game : console version


"""
import sys
from minesweeper import *

def tour_de_jeu(minesweeper):
    """
    Function called at each turn of play. Asks the player the coordinates of a cell and the type of movement that he wants to do.
    :param minesweeper: minesweeper game
    :minesweeper type: Minesweeper
    :return: None
    :CU: None
    """
    r=input('Your play x,y,C (C=(R)eveal,(S)et,(U)nset):').split(',')
    C=r[2]
    x=int(r[0])
    y=int(r[1])
    if C=='R' or C=='r':
        try:
            if not minesweeper.grid[y][x].is_revealed():
                minesweeper.reveal_all_cells_from(x,y)
            else:
                print('This cell has already been revealed')
        except IndexError:
            print("This cell doesn't exist")
    elif C=='S' or C=='s':
        try:
            minesweeper.grid[y][x].set_hypothetic()
        except IndexError:
            print("This cell doesn't exist")
    elif C=='U' or C=='u':
        try:
            minesweeper.grid[y][x].unset_hypothetic()
        except IndexError:
            print("This cell doesn't exist")
    else:
        print("This choice doesn't exist")
        tour_de_jeu(minesweeper)
        
def affichage(minesweeper):
    """
    Function called at each turn of play. Display the grid of the game.
    :param minesweeper: minesweeper game
    :minesweeper type: Minesweeper
    :return: None
    :CU: None
    """
    premiere_ligne='  '
    for i in range(minesweeper.get_width()):
        if i<10:
            premiere_ligne+='  '+str(i)+' '
        else:
            premiere_ligne+=' '+str(i)+' '
    entre_ligne='  '+'+---'*minesweeper.get_width()+'+'
    print(premiere_ligne)
    print(entre_ligne)
    for line in minesweeper.grid:
        if minesweeper.grid.index(line)<10:
            line=' '+str(minesweeper.grid.index(line))+'|  '+'|  '.join([str(cell) for cell in line])+'|'
        else:
            line=str(minesweeper.grid.index(line))+'|  '+'|  '.join([str(cell) for cell in line])+'|'
        print(line)
        print(entre_ligne)

def main():
    """
    main function for console minesweeper game
    """
    if len(sys.argv) == 4:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        nbombs = int(sys.argv[3])
    else:
        width = 20
        height = 10
        nbombs = 1
    game = Minesweeper(width, height, nbombs)
    while game.get_state()==GameState.unfinished:
        affichage(game)
        tour_de_jeu(game)
    if game.get_state()==GameState.winning:
        affichage(game)
        print('You win !')
    else:
        affichage(game)
        print('You lose..')
        
if __name__ == '__main__':
    main()
