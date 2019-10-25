# -*- coding: utf-8 -*-
import numpy as np
from queue import Queue
from bfs import bfs
import settings


def makePath(maze_origin, prev, start, end):
    '''
    Make a path presented by list from the prev matrix given.
    '''
    path = []
    current = end
    while current != start:
        path.insert(0, current)  # insert at the head of the path
        current = prev[current[0]][current[1]]
    return path


def makeMazeWithPath(maze_origin, path):
    '''
    Draw the path into the maze.
    '''
    maze = maze_origin.copy()

    for i in range(len(path)-1):
        if path[i][0] + 1 == path[i+1][0]:
            maze[path[i]] = '↓'
        elif path[i][0] - 1 == path[i+1][0]:
            maze[path[i]] = '↑'
        elif path[i][1] - 1 == path[i+1][1]:
            maze[path[i]] = '←'
        elif path[i][1] + 1 == path[i+1][1]:
            maze[path[i]] = '→'
        else:
            exit('[-] Path Error!')

    return maze


if __name__ == '__main__':
    with open(settings.filename) as file:
        maze = []  # list of list
        for i, line in enumerate(file):
            line = line.strip()  # delete EOL
            start_col = line.find(settings.start_char)
            end_col = line.find(settings.end_char)
            if start_col != -1:
                start = (i, start_col)
            if end_col != -1:
                end = (i, end_col)
            maze.append(list(line))  # append current row
    maze = np.array(maze)  # convert to numpy 2D-array

    prev = bfs(maze, start, end)
    path = makePath(maze, prev, start, end)

    # Print the length of the path
    print('[+] Steps:', len(path))
    # Print the path in a list of coordinates
    print('[+] Path (in coordinates):\n', path)
    # Print the figure of the maze and the path
    print('[+] Path (in figure):')
    maze_with_path = makeMazeWithPath(maze, path)
    for line in maze_with_path:
        print(''.join(line))
