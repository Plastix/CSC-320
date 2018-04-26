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


import random
import sys

import util
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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

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

        # Score, closest food, closest ghost

        "*** YOUR CODE HERE ***"
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


PACMAN_AGENT = 0
MAX_INT = sys.maxsize
MIN_INT = -sys.maxsize - 1


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
        return self.minimax(gameState)

    def minimax(self, state):
        next_agent = 1 % state.getNumAgents()
        legal_actions = state.getLegalActions(PACMAN_AGENT)
        depth = 0
        best_value, best_action = max(
            map(lambda a: (self.value(state.generateSuccessor(PACMAN_AGENT, a), next_agent, depth), a), legal_actions),
            key=lambda item: item[0])
        return best_action

    def is_terminal_state(self, state, depth):
        return depth >= self.depth or state.isWin() or state.isLose()

    def value(self, state, agent, depth):
        if self.is_terminal_state(state, depth):
            return self.evaluationFunction(state)

        if agent == PACMAN_AGENT:
            return self.max_value(state, agent, depth)
        else:
            return self.min_value(state, agent, depth)

    def max_value(self, state, agent, depth):
        v = MIN_INT
        for successor in map(lambda a: state.generateSuccessor(agent, a), state.getLegalActions(agent)):
            next_agent = (agent + 1) % state.getNumAgents()
            v = max(v, self.value(successor, next_agent, depth))
        return v

    def min_value(self, state, agent, depth):
        v = MAX_INT
        for successor in map(lambda a: state.generateSuccessor(agent, a), state.getLegalActions(agent)):
            next_agent = (agent + 1) % state.getNumAgents()
            next_depth = depth + 1 if next_agent == PACMAN_AGENT else depth
            v = min(v, self.value(successor, next_agent, next_depth))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alpha_beta_minimax(gameState)

    def alpha_beta_minimax(self, state):
        best_value, best_action = self.value(state, PACMAN_AGENT, 0, MIN_INT, MAX_INT)

        return best_action

    def is_terminal_state(self, state, depth):
        return depth >= self.depth or state.isWin() or state.isLose()

    def value(self, state, agent, depth, alpha, beta):
        if self.is_terminal_state(state, depth):
            return self.evaluationFunction(state), None

        if agent == PACMAN_AGENT:
            return self.max_value(state, agent, depth, alpha, beta)
        else:
            return self.min_value(state, agent, depth, alpha, beta)

    def max_value(self, state, agent, depth, alpha, beta):
        v = MIN_INT
        a = None
        for successor, action in map(lambda act: (state.generateSuccessor(agent, act), act),
                                     state.getLegalActions(agent)):
            next_agent = (agent + 1) % state.getNumAgents()
            v, a = max((v, a), (self.value(successor, next_agent, depth, alpha, beta)[0], action),
                       key=lambda item: item[0])
            if v > beta:
                return v, a
            alpha = max(alpha, v)
        return v, a

    def min_value(self, state, agent, depth, alpha, beta):
        v = MAX_INT
        a = None
        for successor, action in map(lambda act: (state.generateSuccessor(agent, act), act),
                                     state.getLegalActions(agent)):
            next_agent = (agent + 1) % state.getNumAgents()
            next_depth = depth + 1 if next_agent == PACMAN_AGENT else depth
            v, a = min((v, a), (self.value(successor, next_agent, next_depth, alpha, beta)[0], action),
                       key=lambda item: item[0])
            if v < alpha:
                return v, a
            beta = min(beta, v)
        return v, a


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
        return self.expectimax(gameState)

    def expectimax(self, state):
        next_agent = 1 % state.getNumAgents()
        legal_actions = state.getLegalActions(PACMAN_AGENT)
        depth = 0
        best_value, best_action = max(
            map(lambda a: (self.value(state.generateSuccessor(PACMAN_AGENT, a), next_agent, depth), a), legal_actions),
            key=lambda item: item[0])
        return best_action

    def is_terminal_state(self, state, depth):
        return depth >= self.depth or state.isWin() or state.isLose()

    def value(self, state, agent, depth):
        if self.is_terminal_state(state, depth):
            return self.evaluationFunction(state)

        if agent == PACMAN_AGENT:
            return self.max_value(state, agent, depth)
        else:
            return self.min_value(state, agent, depth)

    def max_value(self, state, agent, depth):
        v = MIN_INT
        for successor in map(lambda a: state.generateSuccessor(agent, a), state.getLegalActions(agent)):
            next_agent = (agent + 1) % state.getNumAgents()
            v = max(v, self.value(successor, next_agent, depth))
        return v

    def min_value(self, state, agent, depth):
        v = 0
        legal_moves = state.getLegalActions(agent)
        num_moves = max(len(legal_moves), 1)
        for successor in map(lambda a: state.generateSuccessor(agent, a), legal_moves):
            next_agent = (agent + 1) % state.getNumAgents()
            next_depth = depth + 1 if next_agent == PACMAN_AGENT else depth
            v += self.value(successor, next_agent, next_depth) * (1 / num_moves)
        return v


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
