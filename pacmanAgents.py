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

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, gameState):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in gameState.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP
        
class LeftTurnAgent(Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, gameState):
        legal = gameState.getLegalPacmanActions()
        
        current = gameState.getPacmanState().getDirection()
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


##########################
### Add your code here ###
##########################
