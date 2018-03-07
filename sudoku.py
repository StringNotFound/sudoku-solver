#!/usr/bin/python

import numpy
from datetime import datetime

# Reads in input from a user
def buildSudoku():
    s = numpy.zeros((9,9))
    for i in range(9):
        raw = raw_input()
        str_nums = raw.split(" ")
        if len(str_nums) != 9:
            print("Input must be of length 9")
            return None
        try:
            nums = map(int, str_nums)
        except ValueError:
            print("Invalid number(s)")
            return None
        if len(filter(lambda x: x < 0, nums)) > 0:
            print("Numbers must be be in range: [0, 9]")
            return None
        s[i] = nums
    return s

# solves the given board
def solve(board):
    board = numpy.copy(board)
    empties = getEmpty(board)
    if len(empties) == 0:
        return board
    poses = []
    for e in empties:
        epos = getPossibilities(e[0], e[1], board)
        if len(epos) == 0:
            # cannot solve this square
            return None
        poses.append((e,epos))
    
    # we're going to have to guess
    square = min(poses, key=lambda x: len(x[1]))
    for guess in square[1]:
        board[square[0][0]][square[0][1]] = guess
        res = solve(board)
        if not res is None:
            return res
    # None of the possibilites worked; the square isn't solvable
    return None



def getEmpty(board):
    empty = []
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                empty.append((i, j))
    return empty
            

# returns a set of numbers
def getPossibilities(x, y, board):
    pos = set(range(1,10)) # {1-9}
    for i in range(9):
        try: 
            pos.remove(board[x,i])
        except KeyError: pass
        try: 
            pos.remove(board[i,y])
        except KeyError: pass

    # calculate square
    offsetx = 3*(x/3)
    offsety = 3*(y/3)
    for i in range(3):
        for j in range(3):
            try: 
                pos.remove(board[i+offsetx, j+offsety])
            except KeyError: pass
    return pos

sudoku = numpy.array([
    [0, 6, 4, 9, 3, 0, 0, 2, 0],
    [0, 0, 9, 4, 8, 0, 6, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 3],
    [4, 0, 0, 0, 0, 0, 7, 0, 6],
    [0, 3, 0, 1, 7, 8, 0, 9, 0],
    [9, 0, 7, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 8, 0, 6, 1, 5, 0, 0],
    [0, 4, 0, 0, 9, 7, 3, 1, 0]])

def main():
    s = buildSudoku()
    if s is None:
        return
    sol = solve(s)
    if sol is None:
        print("No solution for given board")
        return
    else: print(sol)

if __name__ == "__main__":
    main()
