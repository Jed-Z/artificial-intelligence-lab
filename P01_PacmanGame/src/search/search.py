# -*- coding: utf-8 -*-
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def graphSearchAlgorithm(problem, frontier):
    """
    通用的图搜索算法，其中第二个参数frontier是util模块中的一种结构，如栈、队列、优先队列等。
    节点node是 (state, actions, cost) 的三元组，各元素如下：
        * state：指一个状态；
        * actions：是路径上每步移动方向的列表；
        * cost：是路径上到当前节点的总代价。
    """
    start_state = problem.getStartState()
    start_node = (start_state, [], 0)  # 初始节点

    explored = set()           # 存储已扩展过的state
    frontier.push(start_node)  # 初始时，边界中只有源节点、空路径

    while not frontier.isEmpty():
        current_state, current_actions, current_cost = frontier.pop()

        if problem.isGoalState(current_state):
            return current_actions  # 返回actions

        if current_state not in explored:
            explored.add(current_state)  # 环检测在【扩展】节点时进行，而不是在【访问】后继处进行
            for succ in problem.getSuccessors(current_state):
                succ_state, succ_action, succ_stepcost = succ
                new_actions = current_actions + [succ_action]
                new_cost = current_cost + succ_stepcost
                frontier.push((succ_state, new_actions, new_cost))  # 将后继加入边界

    return []  # 无解

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** MY CODE HERE ***"
    return graphSearchAlgorithm(problem, util.Stack())
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** MY CODE HERE ***"
    return graphSearchAlgorithm(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** MY CODE HERE ***"
    # 一致代价搜索中，节点按照当前路径上的总代价排序，也就是node三元组的第三个元素
    return graphSearchAlgorithm(problem, util.PriorityQueueWithFunction(lambda node: node[2]))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** MY CODE HERE ***"
    # A*搜索只是通用图搜索算法的一种而已，所以我实现了一个 graphSearchAlgorithm（见本文件
    # 上方）,也不是很麻烦。向它传不同的frontier参数，就能实现DFS、BFS、UCS、A*等算法。这实
    # 现了图搜索算法的统一，我觉得很好。
    def f(node):
        """ f(n) = g(n) + h(n). """
        g_value = node[2]
        h_value = heuristic(node[0], problem)
        return g_value + h_value
    return graphSearchAlgorithm(problem, util.PriorityQueueWithFunction(f))



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
