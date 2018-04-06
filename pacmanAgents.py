# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Some modifications were made to this file by Kristina Striegnitz
# (striegnk@union.edu).

from pacman import Directions
from game import Agent
import random

DIRECTION_LIST = [Directions.WEST, Directions.EAST, Directions.NORTH, Directions.SOUTH]


class GoWestAgent(Agent):
    """An agent that goes West until it can't."""

    def getAction(self, game_state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in game_state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


class LeftTurnAgent(Agent):
    """An agent that turns left at every opportunity"""

    def getAction(self, game_state):
        legal = game_state.getLegalPacmanActions()

        current = game_state.getPacmanState().getDirection()
        if current == Directions.STOP:
            current = Directions.NORTH

        if Directions.LEFT[current] in legal:
            return Directions.LEFT[current]
        elif current in legal:
            return current
        elif Directions.RIGHT[current] in legal:
            return Directions.RIGHT[current]
        elif Directions.REVERSE[current] in legal:
            return Directions.REVERSE[current]
        else:
            return Directions.STOP


class RectangularRoomCleaner(Agent):
    """
    A simple-reflex agent that will east an entire rectangular room. Assumes that there are no obstacles.
    """

    def getAction(self, game_state):
        legal = game_state.getLegalPacmanActions()
        current = game_state.getPacmanState().getDirection()
        left = Directions.LEFT[current]
        right = Directions.RIGHT[current]

        if current == Directions.STOP:
            moves = list(filter(lambda move: move in legal, DIRECTION_LIST))
            current = moves[0] if moves else current

        if current == Directions.SOUTH:
            # Turn east after hitting west wall
            if left in legal and right not in legal:
                return left
            # Turn west after hitting east wall
            elif left not in legal and right in legal:
                return right

        if current not in legal:
            # Always turn south when hitting a wall
            if left in legal and right in legal:
                if current == Directions.WEST:
                    return left
                else:
                    return right
            # Turn or reverse when hitting a corner
            elif left in legal:
                return left
            elif right in legal:
                return right
            return Directions.REVERSE[current]
        else:
            # Go straight if possible
            return current


class RandomizedRoomCleaner(Agent):
    """
    A randomized simple-reflex agent. Continues straight with a 50% chance as long as going straight is legal. Else,
    it randomly picks between the remaining legal moves without stopping.
    """

    def getAction(self, game_state):
        legal = game_state.getLegalPacmanActions()
        current = game_state.getPacmanState().getDirection()

        # Stop if we only have one legal move (Stop)
        if len(legal) == 1:
            return Directions.STOP

        # Continue straight with 50% chance as long as it is legal
        if current != Directions.STOP and bool(random.getrandbits(1)) and current in legal:
            return current

        # Randomly choose between legal moves. We will have at least one!
        return random.choice(list(filter(lambda move: move in legal, DIRECTION_LIST)))


class ModelBasedRoomCleaner(Agent):
    """
    A model agent that traverses the room in a depth-first pattern.
    """

    movements_x = {
        Directions.NORTH: 0,
        Directions.SOUTH: 0,
        Directions.EAST: 1,
        Directions.WEST: -1,
        Directions.STOP: 0
    }

    movements_y = {
        Directions.NORTH: 1,
        Directions.SOUTH: -1,
        Directions.EAST: 0,
        Directions.WEST: 0,
        Directions.STOP: 0
    }

    def __init__(self, index=0):
        super().__init__(index)
        self.x = 0
        self.y = 0
        self.explored = set()
        self.moves = []

    def getAction(self, game_state):
        legal = game_state.getLegalPacmanActions()
        legal.remove(Directions.STOP)

        unexplored = list(filter(lambda move: not self.is_explored(move), legal))

        if unexplored:
            action = unexplored.pop()
            self.update_model(action)
            return action
        else:
            action = Directions.REVERSE[self.moves.pop()]
            self.update_model(action, backtrack=True)
            return action

    def update_model(self, action, backtrack=False):
        self.explored.add((self.x, self.y))

        self.x += ModelBasedRoomCleaner.movements_x[action]
        self.y += ModelBasedRoomCleaner.movements_y[action]

        if not backtrack:
            self.moves.append(action)

    def is_explored(self, action):
        x = self.x + ModelBasedRoomCleaner.movements_x[action]
        y = self.y + ModelBasedRoomCleaner.movements_y[action]
        return (x, y) in self.explored
