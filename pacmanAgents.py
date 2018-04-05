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

DIRECTION_LIST = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]


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
            for dir in [Directions.WEST, Directions.EAST, Directions.NORTH, Directions.SOUTH]:
                if dir in legal:
                    current = dir
                    break

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
    def getAction(self, game_state):
        legal = game_state.getLegalPacmanActions()

        if len(legal) == 1:
            return Directions.STOP

        current = random.choice(DIRECTION_LIST)
        while current not in legal:
            current = random.choice(DIRECTION_LIST)

        return current
