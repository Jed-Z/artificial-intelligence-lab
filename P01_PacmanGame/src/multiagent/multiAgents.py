# -*- coding=utf-8 -*-
# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # print '-'*20
        # print legalMoves
        # print scores
        # print bestIndices, bestScore

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print '-' * 10
        # print 'successorGameState', successorGameState
        # print 'newPos', newPos
        # print 'newFood', newFood
        # print 'newGhostStates', newGhostStates
        # print 'newScaredTimes', newScaredTimes
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** MY CODE HERE ***"
        # 在本函数getAction中又定义了一个子函数dfMiniMax，该函数通过递归实现MiniMax算
        # 法。本函数仅仅对dfMiniMax做了一次初始调用。
        # 
        # dfMiniMax函数内通过agent_index参数来判断当前节点是MAX节点还是MIN节点。在吃
        # 豆人问题中，MAX节点只有一种，就是pacman；MIN节点可能有多种，取决于ghost的数量。
        # 博弈树的一层包含一个pacman及所有ghost的一次移动，因此在dfMiniMax函数中，depth
        # 的更新仅发生在调用MAX节点前，而调用MIN节点时depth不变。
        # 
        # 注意depth和self.depth的区别：前者是递归变量；后者是MultiAgentSearchAgent类
        # 的成员，在递归调用中不会改变。
        # 
        # A single search ply is considered to be one Pacman move and all the
        # ghosts’ responses, so depth 2 search will involve Pacman and each ghost
        # moving two times.

        def dfMiniMax(state, agent_index, depth):
            """
            MiniMax算法的深度优先实现。
            返回值：二元组(动作, 分数)
            """
            # 终止状态
            if state.isWin() or state.isLose() or depth >= self.depth:
                return 'Stop', self.evaluationFunction(state)

            # 轮到吃豆人（MAX节点）
            if agent_index == 0:
                max_score = -float('inf')
                max_action = 'Stop'  # 初始化
                for action in state.getLegalActions(agent_index):
                    # 注意这里depth的含义，访问MIN节点时depth不变
                    succ_score = dfMiniMax(state.generateSuccessor(agent_index, action), 1, depth)[1]
                    if succ_score > max_score:
                        max_score = succ_score
                        max_action = action
                return max_action, max_score  # (最大分值动作, 最大分值)

            # 轮到幽灵（MIN节点）
            else:
                if agent_index == gameState.getNumAgents() - 1:
                    depth += 1  # 最后一个幽灵的下一次调用将是MAX节点，因此要增加深度

                min_score = float('inf')
                min_action = 'Stop'  # 初始化
                for action in state.getLegalActions(agent_index):
                    succ = state.generateSuccessor(agent_index, action)
                    succ_index = (agent_index + 1) % gameState.getNumAgents()  # 下一个轮到谁
                    succ_score = dfMiniMax(succ, succ_index, depth)[1]
                    if succ_score < min_score:
                        min_score = succ_score
                        min_action = action
                return min_action, min_score  # (最小分值动作, 最小分值)

        return dfMiniMax(gameState, 0, 0)[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** MY CODE HERE ***"
        # 使用的数据结构与MinimaxAgent和dfMiniMax基本相同，maxValue和minValue
        # 两个子函数分别对应α剪枝和β剪枝，算法参考了题目PDF第9页的图片。本函数，也就
        # 是外层函数getAction仅仅对maxValue做了一次初始调用。
        # 
        # 这里同样需要注意深度的问题，子啊dfMiniMax前的注释已有详细说明，此处省略。
        
        def maxValue(state, alpha, beta, depth):
            """
            MAX节点处不需要agent_index参数，因为它必定为0。
            返回值：二元组(动作, 分数)
            """
            agent_index = 0  # pacman的agend_index为0，相当于常量

            if state.isWin() or state.isLose() or depth >= self.depth:
                return 'Stop', self.evaluationFunction(state)

            max_score = -float('inf')
            max_action = 'Stop'  # 初始化
            for action in state.getLegalActions(0):
                succ = state.generateSuccessor(0, action)
                succ_score = minValue(succ, alpha, beta, 1, depth)[1]  # 1表示第一个ghost的序号
                if succ_score > max_score:
                    max_score = succ_score
                    max_action = action
                if max_score > beta:
                    return max_action, max_score  # 剪枝
                alpha = max(alpha, max_score)     # 更新alpha
            return max_action, max_score

        def minValue(state, alpha, beta, agent_index, depth):
            """
            由于MIN节点可能有多个，因此需要agent_index参数来区分。
            返回值：二元组(动作, 分数)
            """
            # MIN节点处无需检查depth
            if state.isWin() or state.isLose():
                return 'Stop', self.evaluationFunction(state)

            min_score = float('inf')
            min_action = 'Stop'  # 初始化
            for action in state.getLegalActions(agent_index):
                succ = state.generateSuccessor(agent_index, action)
                if agent_index == gameState.getNumAgents() - 1:
                    # 下一个轮到pacman，是新的一层，因此深度增加1
                    succ_score = maxValue(succ, alpha, beta, depth + 1)[1]
                else:
                    # 下一个轮到另一个ghost，属于同一层，深度不变
                    succ_score = minValue(succ, alpha, beta, agent_index+1, depth)[1]
                if succ_score < min_score:
                    min_score = succ_score
                    min_action = action
                if min_score < alpha:
                    return min_action, min_score  # 剪枝
                beta = min(beta, min_score)       # 更新beta
            return min_action, min_score
        
        # 初始调用MAX节点，alpha = -inf，beta = +inf，depth = 0
        return maxValue(gameState, -float('inf'), float('inf'), 0)[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

