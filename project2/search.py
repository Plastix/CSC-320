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
    return [s, s, w, s, w, w, s, w]


class SearchNode(object):
    """
    Class which represents a node in a search tree
    """

    def __init__(self, parent, state) -> None:
        super().__init__()
        self.parent = parent
        self.state = state[0]
        self.action = state[1]
        self.stepCost = state[2]

        if parent is None:
            self.pathCost = self.stepCost
        else:
            self.pathCost = parent.pathCost + self.stepCost

    def __eq__(self, o) -> bool:
        return self.state == o.state


def get_start_search_node(problem):
    return SearchNode(None, (problem.getStartState(), None, 0))


def get_path(search_node):
    path = []
    if search_node:
        while search_node:
            if search_node.parent:  # Don't add root node because it doesn't have an action
                path.append(search_node.action)
            search_node = search_node.parent
        path.reverse()
    return path


def graph_search(problem, frontier):
    frontier.push(get_start_search_node(problem))
    explored = set()

    while not frontier.isEmpty():
        leaf = frontier.pop()
        state = leaf.state
        if problem.isGoalState(state):
            return get_path(leaf)

        if state not in explored:
            explored.add(state)
            for successor in problem.getSuccessors(state):
                frontier.push(SearchNode(leaf, successor))

    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    return graph_search(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return graph_search(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return graph_search(problem, util.PriorityQueueWithFunction(lambda node: node.pathCost))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return graph_search(problem, util.PriorityQueueWithFunction(
        lambda node: node.pathCost + heuristic(node.state, problem)))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
