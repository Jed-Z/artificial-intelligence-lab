# -*- coding: utf-8 -*-
from queue import Queue
import settings


def bfs(maze_origin, start, end):
    '''
    Find a path in the maze given using BFS.
    '''
    maze = maze_origin.copy()

    rows = len(maze)     # num of rows of the maze
    cols = len(maze[0])  # num of columns of the maze
    prev = [[(-1, -1) for j in range(cols)] for i in range(rows)]  # record the path

    frontier = Queue()
    frontier.put(start)

    while not frontier.empty():
        current = frontier.get()
        if current == end:  # have explored to the end
            break

        row = current[0]
        col = current[1]

        # up
        if row > 0 and maze[row-1][col] != settings.wall_char:
            frontier.put((row-1, col))
            maze[row-1][col] = settings.wall_char
            prev[row-1][col] = (row, col)

        # down
        if row < rows - 1 and maze[row+1][col] != settings.wall_char:
            frontier.put((row+1, col))
            maze[row+1][col] = settings.wall_char
            prev[row+1][col] = (row, col)

        # left
        if col > 0 and maze[row][col-1] != settings.wall_char:
            frontier.put((row, col-1))
            maze[row][col-1] = settings.wall_char
            prev[row][col-1] = (row, col)

        # right
        if col < cols - 1 and maze[row][col+1] != settings.wall_char:
            frontier.put((row, col+1))
            maze[row][col+1] = settings.wall_char
            prev[row][col+1] = (row, col)

    return prev
