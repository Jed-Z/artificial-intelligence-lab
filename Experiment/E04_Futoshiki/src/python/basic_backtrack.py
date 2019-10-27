# @Author: Jed Zhang
# @Date: 2019-09-19 16:33:50
# @Last Modified by:   Jed Zhang
# @Last Modified time: 2019-09-19 16:33:50

import numpy as np
import copy

SIZE = -1


def isSolved(puzzle):
    """
    Check whether all cells in the puzzle is filled.
    """
    return puzzle.all()  # test if all values are non-zero


def isValid(puzzle, constraints):
    """
    Check whether all constraints are satisfied.
    """
    s = set()

    # rows
    for i in range(SIZE):
        for j in range(SIZE):
            if puzzle[i, j] != 0 and puzzle[i, j] in s:
                return False  # duplicated in row
            else:
                s.add(puzzle[i, j])
        s.clear()

    # columns
    for j in range(SIZE):
        for i in range(SIZE):
            if puzzle[i, j] != 0 and puzzle[i, j] in s:
                return False  # duplicated in row
            else:
                s.add(puzzle[i, j])
        s.clear()

    # constraints
    for constraint in constraints:
        large = puzzle[constraint[0], constraint[1]]
        small = puzzle[constraint[2], constraint[3]]
        if large != 0 and small != 0 and not large > small:
            return False

    # pass all tests, so it is valid
    return True


def basicBacktrack(puzzle_origin, constraints):
    """
    Basic backtrack (without forward checking).
    If a solution is found, return it; else return None.
    """
    puzzle = puzzle_origin.copy()  # the origin puzzle is not modified

    if isSolved(puzzle):
        return puzzle

    pos = np.where(puzzle == 0)
    pos = pos[0][0], pos[1][0]  # position of the first empty cell

    for i in range(1, SIZE + 1):
        puzzle[pos] = i
        if isValid(puzzle, constraints):
            ret = basicBacktrack(puzzle, constraints)
            if ret is not None:
                return ret

    puzzle[pos] = 0  # restore the assignment
    return None


def loadFutoshiki(puz_filename, con_filename):
    """
    Read the puzzle and constraints from files to numpy matrices,
    and convert the coordinates into 0-indexed (coordinates in the
    file are 1-indexed).
    """
    global SIZE
    puzzle = np.loadtxt(puz_filename, dtype=np.uint8)
    constraints = np.loadtxt(con_filename, dtype=np.uint8) - 1  # index start at 0 instead of 1
    SIZE = len(puzzle)  # the side length of the puzzle
    return puzzle, constraints


if __name__ == '__main__':
    # basic backtrack runs slowly, so we use a small puzzle (5x5) to test it
    puzzle, constraints = loadFutoshiki('smallpuzzle.txt', 'smallconstraints.txt')
    result = basicBacktrack(puzzle, constraints)

    if result is not None:
        print('Solution found:')
        print(result)
    else:
        print('[-] No solution!')
