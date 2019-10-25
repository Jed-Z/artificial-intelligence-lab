
# -*- coding: utf-8 -*-
import numpy as np
import datetime

def isGoal(node):
    """
    Test if the given node (state) is the goal.
    """
    goal = np.append(range(1, sidelen * sidelen), 0).reshape(sidelen, sidelen)
    return (node == goal).all()


def h1(node):
    """
    Heuristic function 1: using the number of misplaced tiles.
    """
    goal = np.append(range(1, sidelen * sidelen), 0).reshape(sidelen, sidelen)
    return sidelen * sidelen - np.count_nonzero(goal == node) 


def h2(node):
    """
    Heuristic function 2: using Manhattan distance.
    """
    target = {}
    count = 1
    for i in range(sidelen):
        for j in range(sidelen):
            target[count] = (i, j)
            count += 1
    target[0] = (sidelen-1, sidelen-1)

    total_distance = 0
    for i in range(sidelen):
        for j in range(sidelen):
            val = node[i, j]
            total_distance += abs(i - target[val][0]) + abs(j - target[val][1])
    return total_distance


def ida_star(root):
    """
    Do IDA* algorithm from node `root`.
    """
    bound = h2(root)  # initial bound
    path = [root]
    while True:
        ret = search(path, 0, bound)
        if ret == True:
            return path
        if ret == float('inf'):
            return False
        else:
            bound = ret


def search(path, g, bound):
    """
    Do the DFS.
    """
    node = path[-1]  # current node is the last node in the path
    f = g + h2(node)  # heuristic function
    if f > bound:
        return f
    if isGoal(node):
        return True

    temp = np.where(node == 0)  # find the blank
    blank = (temp[0][0], temp[1][0])  # blank's position

    succs = []
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
    for move in moves:
        next_blank = tuple(np.sum([blank, move], axis=0))
        if next_blank[0]>=0 and next_blank[0]<sidelen and next_blank[1]>=0 and next_blank[1]<sidelen:
            succ = node.copy()
            succ[blank], succ[next_blank] = succ[next_blank], succ[blank]
            succs.append(succ)

    _min = float('inf')
    succs.sort(key=lambda x: h2(x))
    for succ in succs:
        if not any((succ == x).all() for x in path):  # special syntax
            path.append(succ)
            t = search(path, g+1, bound)
            if t == True:
                return True
            if t < _min:
                _min = t
            path.pop()
    return _min


def makeActions(path):
    """
    Constuct a list containing numbers to be moved in each step.
    """
    if path == False:
        raise ValueError('No solution!')

    actions = []
    for i, node in enumerate(path[1:]):
        temp = np.where(node == 0)  # find the blank
        blank = (temp[0][0], temp[1][0])  # blank's position
        actions.append(path[i][blank])
    return actions


if __name__ == '__main__':
    print('***STARTING***', datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))

    filename = 'mytest.txt'
    puzzle = np.loadtxt(filename, dtype=np.uint8)  # number 0 indicates the blank
    sidelen = len(puzzle)  # side length of puzzle
    result = makeActions(ida_star(puzzle))
    print(result)
    print('Length:', len(result))

    print('***Finished***', datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
