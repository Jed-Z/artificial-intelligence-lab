# @Author: Jed Zhang
# @Date: 2019-09-19 16:33:50
# @Last Modified by:   Jed Zhang
# @Last Modified time: 2019-09-19 16:33:50

import numpy as np
import copy
from pprint import pprint

SIZE = -1


def isSolved(puzzle):
    """
    Check whether all cells in the puzzle is filled.
    """
    return puzzle.all()  # test if all values are non-zero


def makeDomains(puzzle, constraints):
    """
    Make a dict as the initial domains of all variables. This function
    should be called only once at the beginning of the program.
    """

    def domainCount(domains):
        """
        Count the total number of values available in the puzzle.
        """
        count = 0
        for domain in domains.values():
            count += len(domain)
        return count

    # initialize
    domains = {}
    for i in range(SIZE):
        for j in range(SIZE):
            if puzzle[i, j] != 0:
                domains[i, j] = {puzzle[i, j]}
            else:
                domains[i, j] = set(range(1, SIZE + 1))

    # remove values that have conflict on rows or columns
    for i in range(SIZE):
        for j in range(SIZE):
            if puzzle[i, j] != 0:
                for i2 in range(SIZE):
                    if i2 != i and puzzle[i, j] in domains[i2, j]:
                        domains[i2, j].remove(puzzle[i, j])
                        if len(domains[i2, j]) == 0:
                            return None  # DWO
                for j2 in range(SIZE):
                    if j2 != j and puzzle[i, j] in domains[i, j2]:
                        domains[i, j2].remove(puzzle[i, j])
                        if len(domains[i, j2]) == 0:
                            return None  # DWO

    # remove values that have conflict with constraints
    old_domain_count = 0
    while True:
        # repeat until total count of all domains cannot decrease anymore
        # I think this procedure can reduce the state space, thus speed up the search
        for constraint in constraints:
            large_pos = (constraint[0], constraint[1])
            small_pos = (constraint[2], constraint[3])
            if puzzle[large_pos] != 0:  # large_pos has been assigned
                for i in range(puzzle[large_pos], SIZE + 1):
                    if i in domains[small_pos]:
                        domains[small_pos].remove(i)
                        if len(domains[small_pos]) == 0:
                            return None  # DWO
            else:  # large_pos has not been assigned
                minimum = min(domains[small_pos])
                if minimum in domains[large_pos]:
                    domains[large_pos].remove(minimum)


            if puzzle[small_pos] != 0:  # small_pos has been assigned
                for i in range(1, puzzle[small_pos] + 1):
                    if i in domains[large_pos]:
                        domains[large_pos].remove(i)
                        if len(domains[large_pos]) == 0:
                            return None  # DWO
            else:  # small_pos has not been assigned
                maximum = max(domains[large_pos])
                if maximum in domains[small_pos]:
                    domains[small_pos].remove(maximum)

        # repeat ends
        new_domain_count = domainCount(domains)
        if new_domain_count == old_domain_count:
            break
        else:
            old_domain_count = new_domain_count


    return domains


def updateDomains(puzzle, constraints, domains_origin, pos):
    """
    In each iteration, we have chosen a pos using MRV, and assign a
    value in its domain to it. After that, we have to update some
    variables' domains by removing some values which has conflict with
    the assignment.
    """
    domains = copy.deepcopy(domains_origin)  # deep copy

    # check the same column
    for i in range(SIZE):
        if i == pos[0]:
            continue
        if puzzle[i, pos[1]] == puzzle[pos]:
            return None
        if puzzle[pos] in domains[i, pos[1]]:
            domains[i, pos[1]].remove(puzzle[pos])
            if len(domains[i, pos[1]]) == 0:
                return None  # DWO

    # check the same row
    for j in range(SIZE):
        if j == pos[1]:
            continue
        if puzzle[pos[0], j] == puzzle[pos]:
            return None
        if puzzle[pos] in domains[pos[0], j]:
            domains[pos[0], j].remove(puzzle[pos])
            if len(domains[pos[0], j]) == 0:
                return None  # DWO

    # check the constraints
    for constraint in constraints:
        large_pos = (constraint[0], constraint[1])
        small_pos = (constraint[2], constraint[3])
        if pos == large_pos:
            for k in range(puzzle[pos], SIZE + 1):
                if k in domains[small_pos]:
                    domains[small_pos].remove(k)
                    if len(domains[small_pos]) == 0:
                        return None  # DWO
        elif pos == small_pos:
            for k in range(1, puzzle[pos] + 1):
                if k in domains[large_pos]:
                    domains[large_pos].remove(k)
                    if len(domains[large_pos]) == 0:
                        return None  # DWO
    return domains


def mrv(puzzle, domains):
    """
    Find the variable with minimum remaining values (MRV),
    and return its position.
    """
    min_val = SIZE * SIZE  # max size of domain
    min_pos = (-1, -1)
    for i in range(SIZE):
        for j in range(SIZE):
            if puzzle[i, j] == 0 and len(domains[i, j]) < min_val:
                min_val = len(domains[i, j])
                min_pos = (i, j)
    return min_pos


def forwardChecking(puzzle_origin, constraints, domains_origin):
    """
    Use forward checking algorithm to solve the CSP problem.
    """
    puzzle = puzzle_origin.copy()
    domains = domains_origin.copy()

    if isSolved(puzzle):
        return puzzle

    pos = mrv(puzzle, domains)  # find a unassigned variable using MRV

    for d in domains[pos]:
        puzzle[pos] = d
        temp_domains = updateDomains(puzzle, constraints, domains, pos)
        if temp_domains is not None:  # not DWO
            ret = forwardChecking(puzzle, constraints, temp_domains)
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
    puzzle, constraints = loadFutoshiki('../puzzle.txt', '../constraints.txt')
    domains = makeDomains(puzzle, constraints)
    result = forwardChecking(puzzle, constraints, domains)

    if result is not None:
        print('Solution found:')
        print(result)
    else:
        print('[-] No solution!')
